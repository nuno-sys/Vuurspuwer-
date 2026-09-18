# -*- coding: utf-8 -*-
"""Nieuwe blogartikelen die niet uit de WordPress-export komen.

Elk artikel is een gewone post voor build.py (zelfde velden als de export),
plus een eigen FAQ en eigen zoekwoorden. Onderwerpen komen uit de Search
Console-export: zoekopdrachten met veel vertoningen waar de site op pagina
3 tot 9 stond omdat er geen pagina over ging ("vuurspuwen", "vuurwerkshow",
"vrouwelijke vuurspuwer", "workshop vuurspuwen" als teambuilding, "fakirshow"
als uitleg, en België als land met veel vertoningen en weinig klikken).

Artikelen zijn informatief en linken naar de commerciële pagina; ze
concurreren er niet mee. Feiten over Nuno en prijzen komen uitsluitend uit
de bestaande site (zie de controle in de bouw).
"""

DATUM = "2026-09-18"

# velden: slug, title, seo_title, seo_desc, keywords, body (html), faq [(q,a)],
#         img (pad, alt) — pad moet een bestaand WebP-bestand in assets/media zijn
POSTS = []
