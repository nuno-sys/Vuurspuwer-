<?php
/*
Plugin Name: Vuurspuwer SEO Posts
Description: Generates one SEO-optimized post per hour for "vuurspuwer boeken" in 40 Dutch and Belgian cities using the Google Gemini API and Yoast SEO. Posts are automatically added to "City Bookings" and "Shows" categories.
Version: 2.0
Author: Nuno
*/

// Prevent direct access
if (!defined('ABSPATH')) {
    exit;
}

// Plugin activation: Set up cron and initialize options
register_activation_hook(__FILE__, 'vuurspuwer_seo_posts_activate');
function vuurspuwer_seo_posts_activate() {
    // Check for required PHP version and extensions
    if (version_compare(PHP_VERSION, '7.4', '<') || !extension_loaded('curl') || !extension_loaded('json')) {
        wp_die('Vuurspuwer SEO Posts requires PHP 7.4+ with cURL and JSON extensions enabled.');
    }

    // Initialize options if they don't exist
    if (!get_option('vuurspuwer_cities')) {
        $cities = [
            'Amsterdam', 'Rotterdam', 'Utrecht', 'Den Haag', 'Eindhoven', 'Groningen', 'Tilburg', 'Almere', 'Breda', 'Nijmegen',
            'Haarlem', 'Arnhem', 'Amersfoort', 'Maastricht', 'Leiden', 'Dordrecht', 'Zoetermeer', 'Zwolle', 'Enschede', 'Apeldoorn',
            'Antwerpen', 'Gent', 'Brugge', 'Brussel', 'Leuven', 'Liège', 'Charleroi', 'Namur', 'Oostende', 'Mechelen',
            'Mons', 'Kortrijk', 'Hasselt', 'Aalst', 'Sint-Niklaas', 'Genk', 'Knokke-Heist', 'Tournai', 'Seraing', 'Roeselare'
        ];
        update_option('vuurspuwer_cities', $cities);
    }
    if (!get_option('vuurspuwer_generated_cities')) {
        update_option('vuurspuwer_generated_cities', []);
    }
    if (!get_option('vuurspuwer_gemini_model')) {
        update_option('vuurspuwer_gemini_model', 'gemini-1.5-flash-latest');
    }
    if (!get_option('vuurspuwer_debug_mode')) {
        update_option('vuurspuwer_debug_mode', false);
    }

    // Schedule the hourly event if it's not already scheduled
    if (!wp_next_scheduled('vuurspuwer_generate_post_event')) {
        wp_schedule_event(time(), 'hourly', 'vuurspuwer_generate_post_event');
    }

    // Log a warning if WP_CRON is disabled
    if (defined('DISABLE_WP_CRON') && DISABLE_WP_CRON) {
        error_log('Vuurspuwer SEO Posts Warning: WP_CRON is disabled in your wp-config.php. Please set up a server-side cron job to trigger wp-cron.php for the plugin to work.');
    }
}

// Plugin deactivation: Clear scheduled cron job
register_deactivation_hook(__FILE__, 'vuurspuwer_seo_posts_deactivate');
function vuurspuwer_seo_posts_deactivate() {
    wp_clear_scheduled_hook('vuurspuwer_generate_post_event');
}

/**
 * Calls the Google Gemini API.
 *
 * @param string $prompt The prompt to send to the API.
 * @param int $retry_count The current retry attempt number.
 * @return array Associative array with 'content' or 'error'.
 */
function vuurspuwer_call_gemini_api($prompt, $retry_count = 0) {
    $api_key = get_option('vuurspuwer_gemini_api_key', '');
    $model = get_option('vuurspuwer_gemini_model', 'gemini-1.5-flash-latest');

    if (empty($api_key) || !preg_match('/^AIzaSy[0-9A-Za-z_-]{33,}$/', $api_key)) {
        $error_msg = 'Invalid or missing Gemini API key. The key must start with "AIzaSy" and be at least 39 characters long.';
        error_log('Vuurspuwer SEO Posts: ' . $error_msg);
        return ['error' => $error_msg];
    }

    // Use a transient to cache API responses for 24 hours
    $cache_key = 'vuurspuwer_gemini_' . md5($prompt . $model);
    $cached = get_transient($cache_key);
    if ($cached !== false) {
        return ['content' => $cached];
    }

    $url = 'https://generativelanguage.googleapis.com/v1beta/models/' . $model . ':generateContent?key=' . $api_key;
    $data = [
        'contents' => [
            ['parts' => [['text' => $prompt]]]
        ],
        'generationConfig' => [
            'temperature' => 0.7,
            'maxOutputTokens' => 1600
        ]
    ];

    $response = wp_remote_post($url, [
        'headers' => ['Content-Type' => 'application/json'],
        'body' => json_encode($data),
        'timeout' => 45
    ]);

    if (is_wp_error($response)) {
        $error_msg = 'Gemini API network error: ' . $response->get_error_message();
        error_log('Vuurspuwer SEO Posts: ' . $error_msg);
        return ['error' => $error_msg];
    }

    $response_code = wp_remote_retrieve_response_code($response);
    $body = json_decode(wp_remote_retrieve_body($response), true);

    if ($response_code !== 200 || !isset($body['candidates'][0]['content']['parts'][0]['text'])) {
        $error_message = isset($body['error']['message']) ? $body['error']['message'] : 'Unknown API error';
        
        // Retry on rate limit (429) error, up to 3 times
        if ($response_code === 429 && $retry_count < 3) {
            sleep(10); // Wait for 10 seconds before retrying
            return vuurspuwer_call_gemini_api($prompt, $retry_count + 1);
        }

        error_log('Vuurspuwer SEO Posts: Gemini API error - Code ' . $response_code . ': ' . $error_message);
        return ['error' => 'API Error: ' . $error_message, 'response' => $body];
    }

    $content = $body['candidates'][0]['content']['parts'][0]['text'];
    set_transient($cache_key, $content, 24 * HOUR_IN_SECONDS);
    return ['content' => $content];
}

/**
 * Generates the post content for a given city.
 *
 * @param string $city The city name.
 * @return string|false The generated HTML content or false on failure.
 */
function vuurspuwer_generate_post_content($city) {
    $prompt = "Generate a 500–800-word SEO-optimized article in Dutch for 'vuurspuwer boeken $city' with a professional tone. The article must be unique, engaging, and ready for a WordPress post.
- Main Title: Use an <h1> tag for 'Vuurspuwer Boeken in $city: Een Spectaculaire Ervaring'.
- Subheadings: Use <h2> tags for 'Waarom Kiezen voor Vuurspuwer Nuno?', 'Perfect voor Elk Evenement in $city', and 'Hoe U Kunt Boeken'.
- Local Context: Mention a well-known local event or venue in $city (e.g., 'Koningsdag' for Amsterdam, 'Gentse Feesten' for Gent) and suggest how a fire show would enhance it.
- Artist Info: Highlight Nuno's expertise, mentioning over 10 years of experience with fire and fakir shows and his high customer satisfaction.
- CTA: Include a clear call to action: 'Neem vandaag nog contact op via +31 6 20020723 of nuno@hotmail.nl voor een onvergetelijke show.'
- FAQs: Add a section with two FAQs: 'Wat zijn de kosten van een vuurshow in $city?' and 'Voor welke soorten evenementen is een vuurspuwer geschikt?'.
- SEO: Ensure the text uses variations of the main keyword and demonstrates expertise, authority, and trustworthiness (E-E-A-T).
- Formatting: Output the entire article in clean HTML, using <p> tags for paragraphs. Do not use Markdown.";
    
    $result = vuurspuwer_call_gemini_api($prompt);
    if (isset($result['error'])) {
        error_log("Vuurspuwer SEO Posts: Failed to generate content for $city due to API error: " . $result['error']);
        return false;
    }

    // Sanitize the generated HTML content for posting
    $html_content = wp_kses_post($result['content']);

    return $html_content;
}

/**
 * Sets the featured image for a post.
 *
 * @param int $post_id The ID of the post.
 * @param string $city The city name for the alt text.
 * @return int|false The attachment ID or false on failure.
 */
function vuurspuwer_set_featured_image($post_id, $city) {
    // Ensure the required WordPress media functions are available
    require_once(ABSPATH . 'wp-admin/includes/image.php');
    require_once(ABSPATH . 'wp-admin/includes/file.php');
    require_once(ABSPATH . 'wp-admin/includes/media.php');

    $image_url = 'https://fakirshow.nl/wp-content/uploads/2023/10/mentalist-nuno.jpeg';
    $image_alt_text = 'Vuurspuwer Nuno boeken voor een spectaculaire vuurshow in ' . esc_attr($city);
    $image_description = 'Een professionele vuurspuwer voor uw evenement in ' . esc_attr($city) . '.';
    
    // Use media_sideload_image to handle the download and attachment creation
    // The fourth argument 'id' returns the attachment ID, which is what we need
    $attach_id = media_sideload_image($image_url, $post_id, $image_description, 'id');

    if (is_wp_error($attach_id)) {
        error_log('Vuurspuwer SEO Posts: Failed to download featured image for post ' . $post_id . ': ' . $attach_id->get_error_message());
        return false;
    }
    
    // Set the alt text for the newly created attachment
    update_post_meta($attach_id, '_wp_attachment_image_alt', $image_alt_text);
    
    // Set the attachment as the featured image
    set_post_thumbnail($post_id, $attach_id);
    
    return $attach_id;
}


/**
 * The main function that generates a single post. Triggered by cron or manually.
 */
function vuurspuwer_generate_post() {
    $cities = get_option('vuurspuwer_cities', []);
    $generated_cities = get_option('vuurspuwer_generated_cities', []);
    $remaining_cities = array_diff($cities, $generated_cities);

    if (empty($remaining_cities)) {
        error_log('Vuurspuwer SEO Posts: All cities processed. Deactivating cron job.');
        wp_clear_scheduled_hook('vuurspuwer_generate_post_event');
        wp_mail(get_option('admin_email'), 'Vuurspuwer SEO Posts: Campagne voltooid', 'Alle geplande stadsposts zijn succesvol aangemaakt. De cron job is nu gedeactiveerd.');
        return;
    }

    $city = reset($remaining_cities);
    
    $content = vuurspuwer_generate_post_content($city);
    if (!$content) {
        $error_message = 'Kon geen content genereren voor ' . $city . '. Controleer de API-sleutel en het debug-logboek voor meer details.';
        wp_mail(get_option('admin_email'), 'Vuurspuwer SEO Posts: Fout bij contentgeneratie', $error_message);
        return;
    }
    
    // Ensure categories exist
    $city_cat_name = 'City Bookings';
    $shows_cat_name = 'Shows';
    $city_cat_id = get_cat_ID($city_cat_name) ?: wp_create_category($city_cat_name);
    $shows_cat_id = get_cat_ID($shows_cat_name) ?: wp_create_category($shows_cat_name);

    $post_data = [
        'post_title'    => 'Vuurspuwer Boeken in ' . esc_html($city),
        'post_content'  => $content,
        'post_status'   => 'publish',
        'post_author'   => 1, // Assumes admin user with ID 1
        'post_category' => [$city_cat_id, $shows_cat_id],
        'tags_input'    => ['vuurshow', 'fakirshow', strtolower($city)]
    ];

    $post_id = wp_insert_post($post_data, true);
    if (is_wp_error($post_id)) {
        $error_message = 'Kon geen post aanmaken voor ' . $city . ': ' . $post_id->get_error_message();
        error_log('Vuurspuwer SEO Posts: ' . $error_message);
        wp_mail(get_option('admin_email'), 'Vuurspuwer SEO Posts: Fout bij aanmaken van post', $error_message);
        return;
    }

    // Set featured image
    vuurspuwer_set_featured_image($post_id, $city);

    // Yoast SEO integration
    if (defined('WPSEO_VERSION')) {
        $focus_keyword = 'vuurspuwer boeken ' . strtolower($city);
        $seo_title = 'Vuurspuwer Boeken in ' . esc_html($city) . ' | Spectaculaire Shows van Nuno';
        $meta_desc = 'Boek Vuurspuwer Nuno voor een onvergetelijk evenement in ' . esc_html($city) . '! Ervaar een spectaculaire vuur- en fakirshow. Professioneel en ervaren. Bel +31 6 20020723.';
        
        update_post_meta($post_id, '_yoast_wpseo_focuskw', $focus_keyword);
        update_post_meta($post_id, '_yoast_wpseo_title', $seo_title);
        update_post_meta($post_id, '_yoast_wpseo_metadesc', $meta_desc);
    }

    // Add city to the list of generated cities
    $generated_cities[] = $city;
    update_option('vuurspuwer_generated_cities', $generated_cities);

    $success_message = 'Nieuwe post succesvol aangemaakt voor ' . $city . ' (ID: ' . $post_id . ').';
    error_log('Vuurspuwer SEO Posts: ' . $success_message);
    // Optional: Email notification on success can be disabled if not needed
    // wp_mail(get_option('admin_email'), 'Vuurspuwer SEO Posts: Nieuwe post aangemaakt', $success_message);
}
add_action('vuurspuwer_generate_post_event', 'vuurspuwer_generate_post');


// Admin menu and settings page
add_action('admin_menu', 'vuurspuwer_seo_posts_menu');
function vuurspuwer_seo_posts_menu() {
    add_options_page(
        'Vuurspuwer SEO Settings',
        'Vuurspuwer SEO',
        'manage_options',
        'vuurspuwer-seo-posts',
        'vuurspuwer_seo_posts_settings_page'
    );
}

function vuurspuwer_seo_posts_settings_page() {
    if (!current_user_can('manage_options')) {
        wp_die('You do not have sufficient permissions to access this page.');
    }

    // Handle form submissions
    if (isset($_POST['action'])) {
        check_admin_referer('vuurspuwer_actions');

        if ($_POST['action'] === 'save_settings') {
            // Sanitize and save API key
            $api_key = sanitize_text_field($_POST['vuurspuwer_gemini_api_key']);
            update_option('vuurspuwer_gemini_api_key', $api_key);

            // Sanitize and save model
            $model = sanitize_text_field($_POST['vuurspuwer_gemini_model']);
            if (in_array($model, ['gemini-1.5-pro-latest', 'gemini-1.5-flash-latest', 'gemini-pro'])) {
                update_option('vuurspuwer_gemini_model', $model);
            }
            
            update_option('vuurspuwer_debug_mode', isset($_POST['vuurspuwer_debug_mode']) ? 1 : 0);
            
            add_settings_error('vuurspuwer_settings', 'settings_updated', 'Settings saved.', 'updated');

        } elseif ($_POST['action'] === 'test_api') {
            $test_result = vuurspuwer_call_gemini_api('Test prompt: respond with "OK"');
            if (isset($test_result['content']) && strpos($test_result['content'], 'OK') !== false) {
                add_settings_error('vuurspuwer_settings', 'api_test_success', 'API key test successful!', 'updated');
            } else {
                $error = $test_result['error'] ?? 'Unknown error during API test.';
                add_settings_error('vuurspuwer_settings', 'api_test_error', 'API test failed: ' . esc_html($error), 'error');
            }
        } elseif ($_POST['action'] === 'generate_manual') {
            vuurspuwer_generate_post();
            add_settings_error('vuurspuwer_settings', 'manual_post_triggered', 'Manual post generation has been triggered. Check your email and posts list in a few minutes.', 'updated');
        } elseif ($_POST['action'] === 'reset_cities') {
            update_option('vuurspuwer_generated_cities', []);
            if (!wp_next_scheduled('vuurspuwer_generate_post_event')) {
                wp_schedule_event(time(), 'hourly', 'vuurspuwer_generate_post_event');
            }
            add_settings_error('vuurspuwer_settings', 'cities_reset', 'Generated city list has been reset. The campaign will start over.', 'updated');
        } elseif ($_POST['action'] === 'clear_cache') {
            global $wpdb;
            $wpdb->query("DELETE FROM {$wpdb->options} WHERE option_name LIKE '_transient_vuurspuwer_gemini_%'");
            add_settings_error('vuurspuwer_settings', 'cache_cleared', 'API cache (transients) cleared.', 'updated');
        }
    }

    // Display settings errors/messages
    settings_errors('vuurspuwer_settings');

    $generated_count = count(get_option('vuurspuwer_generated_cities', []));
    $total_cities = count(get_option('vuurspuwer_cities', []));
    ?>
    <div class="wrap">
        <h1>Vuurspuwer SEO Posts Settings</h1>
        <p>This plugin automatically generates one SEO-optimized post per hour for different cities.</p>

        <div id="dashboard-widgets-wrap">
            <div id="dashboard-widgets" class="metabox-holder">
                <div class="postbox-container" style="width:100%;">
                    <div class="meta-box-sortables">
                        <!-- Status Dashboard -->
                        <div class="postbox">
                            <h2 class="hndle"><span>Status Dashboard</span></h2>
                            <div class="inside">
                                <p><strong>Campaign Progress:</strong> <?php printf('%d / %d cities posted.', $generated_count, $total_cities); ?></p>
                                <p><strong>Cron Status:</strong> <?php echo wp_next_scheduled('vuurspuwer_generate_post_event') ? '✅ Active (Next run: ' . get_date_from_gmt(date('Y-m-d H:i:s', wp_next_scheduled('vuurspuwer_generate_post_event')), 'F j, Y H:i:s') . ')' : '❌ Inactive (All posts may be generated or cron is disabled).'; ?></p>
                                <p><strong>PHP Environment:</strong> <?php echo 'PHP ' . phpversion(); ?> | <?php echo extension_loaded('curl') ? 'cURL: ✅' : 'cURL: ❌'; ?> | <?php echo extension_loaded('json') ? 'JSON: ✅' : 'JSON: ❌'; ?></p>
                            </div>
                        </div>
                        <!-- Settings Form -->
                        <div class="postbox">
                             <h2 class="hndle"><span>Configuration</span></h2>
                             <div class="inside">
                                <form method="post">
                                    <input type="hidden" name="action" value="save_settings">
                                    <?php wp_nonce_field('vuurspuwer_actions'); ?>
                                    <table class="form-table">
                                        <tr>
                                            <th><label for="vuurspuwer_gemini_api_key">Gemini API Key</label></th>
                                            <td>
                                                <input type="password" id="vuurspuwer_gemini_api_key" name="vuurspuwer_gemini_api_key" value="<?php echo esc_attr(get_option('vuurspuwer_gemini_api_key')); ?>" class="regular-text">
                                                <p class="description">Get your API key from <a href="https://aistudio.google.com/apikey" target="_blank">Google AI Studio</a>.</p>
                                            </td>
                                        </tr>
                                        <tr>
                                            <th><label for="vuurspuwer_gemini_model">Gemini Model</label></th>
                                            <td>
                                                <select id="vuurspuwer_gemini_model" name="vuurspuwer_gemini_model">
                                                    <option value="gemini-1.5-flash-latest" <?php selected(get_option('vuurspuwer_gemini_model'), 'gemini-1.5-flash-latest'); ?>>Gemini 1.5 Flash (Fast & Cost-Effective)</option>
                                                    <option value="gemini-1.5-pro-latest" <?php selected(get_option('vuurspuwer_gemini_model'), 'gemini-1.5-pro-latest'); ?>>Gemini 1.5 Pro (Advanced Reasoning)</option>
                                                    <option value="gemini-pro" <?php selected(get_option('vuurspuwer_gemini_model'), 'gemini-pro'); ?>>Gemini Pro (Stable)</option>
                                                </select>
                                            </td>
                                        </tr>
                                         <tr>
                                            <th><label for="vuurspuwer_debug_mode">Debug Mode</label></th>
                                            <td>
                                                <input type="checkbox" id="vuurspuwer_debug_mode" name="vuurspuwer_debug_mode" value="1" <?php checked(get_option('vuurspuwer_debug_mode', 0), 1); ?>>
                                                <span class="description">Enables detailed error logging to <code>wp-content/debug.log</code>. Requires <code>WP_DEBUG</code> and <code>WP_DEBUG_LOG</code> to be enabled in <code>wp-config.php</code>.</span>
                                            </td>
                                        </tr>
                                    </table>
                                    <?php submit_button('Save Settings'); ?>
                                </form>
                             </div>
                        </div>
                        <!-- Actions -->
                        <div class="postbox">
                             <h2 class="hndle"><span>Actions</span></h2>
                             <div class="inside">
                                <p>Use these actions for testing and management.</p>
                                <form method="post" style="display:inline-block; margin-right: 10px;">
                                    <input type="hidden" name="action" value="test_api">
                                    <?php wp_nonce_field('vuurspuwer_actions'); ?>
                                    <?php submit_button('Test API Key', 'secondary', 'submit', false); ?>
                                </form>
                                <form method="post" style="display:inline-block; margin-right: 10px;">
                                    <input type="hidden" name="action" value="generate_manual">
                                    <?php wp_nonce_field('vuurspuwer_actions'); ?>
                                    <?php submit_button('Generate 1 Post Now', 'secondary', 'submit', false); ?>
                                </form>
                                <form method="post" style="display:inline-block; margin-right: 10px;">
                                    <input type="hidden" name="action" value="clear_cache">
                                    <?php wp_nonce_field('vuurspuwer_actions'); ?>
                                    <?php submit_button('Clear API Cache', 'secondary', 'submit', false); ?>
                                </form>
                                <form method="post" onsubmit="return confirm('Are you sure you want to reset the campaign? This will allow the plugin to start generating posts from the beginning.');" style="display:inline-block;">
                                    <input type="hidden" name="action" value="reset_cities">
                                    <?php wp_nonce_field('vuurspuwer_actions'); ?>
                                    <?php submit_button('Reset Campaign', 'delete', 'submit', false); ?>
                                </form>
                             </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <?php
}
?>