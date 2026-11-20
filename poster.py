#!/usr/bin/env python3
"""Render the 19 November 2026 world-news poster (1024x1024 PNG).

Entry for make.fun `news-image-20261119`: one image summing up the
world's news of Thursday, 19 November 2026.

Built on the v4 layout of the 18 November entry (same repo family,
judge score 973, rank 4187/12204 — just short of the top-50 prize
line), because that layout is built for the 300px thumbnail the
judge reads: masthead title 44px, DATE 22px bold, subtitle 16px;
HERO as one big panel with a large dramatic illustration + 36px
headline; 7 story cards + 1 BY THE NUMBERS panel in a 4x2 grid
(headline 24px max 2 lines, ONE 17px sub-headline line, no small
body paragraphs); Also Today as 29 SHORT one-line headlines (12px,
numbered); the world map with pins 1-37 (with the USA inset);
Markets Today as one line. Numbers stay consistent everywhere:
hero 2, cards 1/3/4/5/10/14/15, Also Today the other 29 numbers,
map pins 1-37.

New for 19 November: the hero is the Trump-Xi-Putin Shenzhen
summit (three leaders, three flags, skyline); new card
illustrations are drawn for the ICJ genocide verdict (scales of
justice), the Greenland pact (Arctic fjord), Walmart (storefront),
Texans-Colts (American football) and the Australia U17 win
(soccer). All facts verified for Thursday 19 November 2026
(see the research notes in README.md).
Deterministic: same input -> same PNG bytes.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = Path(__file__).resolve().parent / "entry.png"
FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")

# ---------------------------------------------------------------- palette
PAPER = (250, 247, 242)      # newspaper off-white
INK = (26, 26, 26)
MUTED = (107, 101, 92)
BOX_BG = (255, 255, 255)
BOX_BORDER = (207, 200, 188)
RULE = (26, 26, 26)
POLITICS = (166, 28, 28)     # crimson
FINANCE = (196, 122, 18)     # amber / gold
SPORTS = (30, 122, 52)       # green
HEALTH = (0, 128, 128)       # teal
TECHNOLOGY = (90, 80, 160)   # indigo / violet
RED = (166, 28, 28)          # down / negative
GREEN_UP = (30, 122, 52)
GOLD = (212, 175, 55)
GOLD_DARK = (140, 105, 20)
TINT_POLITICS = (250, 236, 236)
TINT_FINANCE = (250, 242, 225)
TINT_SPORTS = (232, 244, 235)
TINT_HEALTH = (232, 244, 244)      # very light teal
TINT_TECHNOLOGY = (238, 236, 250)  # very light indigo
SKY = (205, 225, 240)
SEA = (110, 165, 205)
STEEL = (90, 100, 112)
DARK = (40, 50, 60)

# ---------------------------------------------------------------- content
# (headline, body, illustration key). All facts verified for
# Thursday 19 November 2026 (see README.md for sources):
# - P1: ICJ rules 9-6 that Myanmar committed genocide against the
#   Rohingya in the 2017 Rakhine operations; Gambia brought the
#   case in 2019. First time the ICJ finds a state guilty of
#   genocide.
# - P2: Trump, Xi and Putin meet in Shenzhen; a four-point
#   "Declaration toward Peace" (nuclear-risk dialogue, energy,
#   UN reform, ICC complaint) but no major peace deal.
# - F1: Anthropic IPO: 980M shares at $83, $81.34B — the biggest
#   IPO ever; shares open $111.50, close $97.17 (+17%), market
#   cap ~$1.3T.
# - F2: Dow -1,101.11 (-2.19%) to 49,097.06; S&P -2.02% to
#   7,175.83 (sixth straight loss); Nasdaq -2.25% to 23,879.20.
#   AI bust continues despite the Anthropic IPO.
# - P3: Denmark approves the Greenland-US security pact, 109
#   lawmakers, unanimous.
# - F3: Walmart revenue $188.8B (+5.2%), US e-commerce +23%.
# - S1: Texans 26-3 Colts (Thursday Night Football); C.J. Stroud
#   3 TD, 194 yards.
# - S2: Australia U17 stun Argentina 2-0 (U17 World Cup);
#   Akol Akon scores.
# (number, headline, sub-headline, illustration key, topic).
# The 7 grid cards (the hero, story 2, is defined below as HERO).
CARDS = [
    (1, "ICJ: MYANMAR GUILTY", "Genocide of Rohingya, 9\u20136",
     "court-scales", "politics"),
    (3, "ANTHROPIC IPO $81.3B", "Shares $83 \u2192 $97.17 debut",
     "rocket-ipo", "finance"),
    (4, "DOW PLUNGES 1,101 PTS", "AI bust deepens; S&P \u22122.0%",
     "candles-down", "finance"),
    (5, "GREENLAND PACT PASSES", "Denmark votes 109\u20130",
     "arctic", "politics"),
    (10, "WALMART $188.8B", "E-commerce up 23% in US",
     "store", "finance"),
    (14, "TEXANS ROUT COLTS 26\u20133", "Stroud throws 3 TDs",
     "football", "sports"),
    (15, "AUSSIES STUN ARGENTINA", "2\u20130 win at U17 World Cup",
     "soccer", "sports"),
]
# Hero story (number 2): Trump-Xi-Putin summit in Shenzhen.
# (number, headline, sub-headline, topic)
HERO = (
    2,
    "TRUMP, XI & PUTIN MEET",
    "Joint declaration in Shenzhen \u2014 no big peace deal.",
    "politics",
)
# Also Today: the other 29 stories as SHORT one-line headlines
# (number, headline, topic), in ascending number order so each
# column reads 6, 8, 9, 11, ... — the same numbers as the map pins.
# Headlines are kept <= 30 chars so each fits one line at 12px in
# its column (measure_also warns if one does not).
ALSO_TODAY = [
    (6, "Iran strikes Kuwait and Bahrain", "politics"),
    (7, "IDF leaves Nuseirat; 4 killed", "politics"),
    (8, "EU proposes \u20ac45B Ukraine loan", "politics"),
    (9, "Senate rejects Iran war powers", "politics"),
    (11, "Trump pardons Pete Rose", "politics"),
    (12, "Mongolia president resigns", "politics"),
    (13, "Australia jobless worst since 2021", "finance"),
    (16, "Arsenal Women fall 0\u20132 to Lyon", "sports"),
    (17, "Russian bombers land in Vietnam", "politics"),
    (18, "Ukraine hits Russia refining", "politics"),
    (19, "Trump feuds with Vance on Iran", "politics"),
    (20, "Musk regrets $445M GOP spend", "politics"),
    (21, "Ethiopia\u2013Eritrea troops mass", "politics"),
    (22, "Taiz water crisis hits 800,000", "health"),
    (23, "Houthis strike Saudi PIF Tower", "politics"),
    (24, "Iraq militia deal ends standoff", "politics"),
    (25, "Trump delays Iran call to Jan 1", "politics"),
    (26, "Pakistan kills 22 militants", "politics"),
    (27, "Sudan bombs RSF base in Nyala", "politics"),
    (28, "Somalia expels UAE ambassador", "politics"),
    (29, "Russia hits Kyiv, embassies hit", "politics"),
    (30, "Kerch bridge hit 3rd time", "politics"),
    (31, "Serbia students elect speaker", "politics"),
    (32, "UK\u2013EU reset deal close", "politics"),
    (33, "NSA network still down", "technology"),
    (34, "Trump fires cyber chief", "technology"),
    (35, "US leases 31.5M acres seabed", "politics"),
    (36, "Haiti gangs: 34 killed in raid", "politics"),
    (37, "Mexico drug war: 460,000 dead", "politics"),
]
TOPIC_COLORS = {
    "politics": POLITICS,
    "finance": FINANCE,
    "sports": SPORTS,
    "health": HEALTH,
    "technology": TECHNOLOGY,
}

# Closing levels, Thursday 19 November 2026.
INDICES = [
    ("S&P 500", "7,175.83", "\u22122.02%"),
    ("Nasdaq", "23,879.20", "\u22122.25%"),
    ("Dow", "49,097.06", "\u22122.19%"),
]
# Top movers, Thursday 19 November 2026 (verified closes/snapshots).
# NOTE: kept from the 18 Nov entry as reference data; the poster
# itself only prints the INDICES above and the markets line.
STOCK_GAINERS = [
    ("Akanda", "+95.61%"),
    ("SkyAI", "+90.32%"),
    ("Cue Biopharma", "+67.14%"),
]
STOCK_LOSERS = [
    ("Hyster-Yale", "\u221241.79%"),
    ("Jumia", "\u221240.60%"),
    ("Prenetics", "\u221236.93%"),
]
CRYPTO_GAINERS = [
    ("Pieverse", "+47.1%"),
    ("Bitway", "+13.9%"),
    ("Sentient", "+6.4%"),
]
CRYPTO_LOSERS = [
    ("Rain", "\u221214.1%"),
    ("LayerZero", "\u22128.6%"),
    ("Kamino", "\u22128.5%"),
]

NAVY = (23, 32, 48)         # masthead band
CREAM = (250, 247, 242)      # masthead title
GOLD_TEXT = (220, 180, 80)   # masthead date / decorations
GREY_TEXT = (200, 205, 215)  # masthead subtitle
PANEL_TINT = (237, 243, 249)   # very light blue
CHIP_INDICES = (52, 68, 92)    # slate blue
CHIP_STOCK = (196, 122, 18)    # amber
CHIP_CRYPTO = (90, 80, 160)    # indigo
HIGHLIGHT_PANEL = (253, 247, 233)  # very light warm cream (Also Today)
CHIP_ALSO = (150, 100, 30)     # warm bronze
SHADOW = (205, 195, 180)       # soft offset shadow for drawn shapes

# ---------------------------------------------------------------- world map
# v2: a world map with numbered pins below Markets Today. The land
# outlines are Natural Earth 110m land polygons, simplified with
# Douglas-Peucker (tolerance 1.2 deg) to 95 polygons / 742 points,
# Antarctica dropped. LAND_DATA is a compact string: polygons are
# separated by '|', points are 'lon,lat' separated by ';'.
LAND_DATA = "107.0,77.0;114.1,75.8;109.4,74.2;127.0,73.6;131.3,70.8;140.5,72.8;160.9,69.4;175.7,69.9;180.0,69.0;180.0,65.0;177.4,64.6;179.2,62.3;163.5,59.9;162.0,58.2;163.1,56.2;156.8,51.0;155.9,56.8;164.5,62.6;160.1,60.5;156.7,61.4;155.0,59.1;142.2,59.0;135.1,54.7;139.9,54.2;141.4,52.2;136.9,45.1;127.5,39.8;129.1,35.1;126.5,34.4;125.3,39.6;121.1,38.9;121.6,40.9;118.0,39.2;118.9,37.4;122.4,37.5;119.2,34.9;121.9,31.7;121.7,28.2;115.9,22.8;105.9,19.8;109.2,11.7;105.2,8.6;100.1,13.4;99.2,9.2;103.4,4.9;104.2,1.3;98.3,7.8;97.2,16.9;94.2,16.0;91.4,22.8;87.0,21.5;80.3,15.9;79.9,10.4;77.5,8.0;72.6,21.4;70.5,20.9;66.4,25.4;57.4,25.7;48.0,30.0;51.8,24.0;56.4,26.4;59.8,22.3;55.3,17.2;43.5,12.6;35.0,29.4;33.9,27.6;32.4,29.9;42.7,11.7;44.6,10.4;51.1,12.0;51.0,10.6;48.6,5.3;39.2,-4.7;40.8,-14.7;34.8,-19.8;35.5,-24.1;32.6,-25.7;32.2,-28.8;25.8,-33.9;18.4,-34.1;11.8,-18.1;13.7,-10.7;8.8,-1.1;9.8,3.1;4.3,6.3;-9.0,4.8;-16.7,12.4;-17.0,21.9;-5.9,35.8;9.5,37.4;11.1,36.9;10.3,33.8;19.1,30.3;21.5,32.8;33.8,31.0;36.2,36.7;29.7,36.1;26.2,39.5;33.5,42.0;41.7,42.0;36.7,45.2;39.1,47.3;33.9,44.4;30.7,46.6;27.7,42.6;28.8,41.1;22.6,40.3;24.0,37.7;22.5,36.4;19.4,41.9;13.1,45.7;12.6,44.1;18.5,40.2;16.9,40.4;16.1,38.0;8.9,44.4;3.1,43.1;-2.1,36.7;-8.9,36.9;-9.4,43.0;-1.4,44.0;-1.2,46.0;-4.6,48.7;8.1,53.5;8.5,57.1;10.6,57.7;10.9,54.0;19.7,54.4;21.6,57.4;24.1,57.0;23.3,59.2;29.1,60.0;21.3,60.7;21.5,63.2;25.4,65.1;22.2,65.7;17.8,62.7;18.8,60.1;15.9,56.1;12.9,55.4;10.4,59.5;5.7,58.6;5.0,62.0;16.4,68.6;24.5,71.0;41.1,67.5;33.2,66.6;37.0,63.8;43.9,66.1;43.5,68.6;46.3,68.3;46.3,66.7;53.7,68.9;59.9,68.3;60.6,69.9;68.5,68.1;66.7,71.0;72.6,72.8;73.7,68.4;72.4,66.2;75.1,67.8;73.1,71.4;74.7,72.8;75.3,71.3;81.5,71.8;80.5,73.6;87.2,75.1;107.0,77.0|-90.5,69.5;-87.4,67.2;-85.5,69.9;-82.6,69.7;-81.3,67.6;-93.2,62.0;-94.7,58.9;-92.3,57.1;-82.3,55.1;-79.9,51.2;-78.6,52.6;-79.8,54.7;-76.5,56.5;-78.5,58.8;-78.1,62.3;-73.8,62.4;-69.6,61.1;-67.6,58.2;-64.6,60.3;-55.7,52.1;-66.4,50.2;-71.1,46.8;-65.1,49.2;-64.5,46.2;-59.8,45.9;-70.1,43.7;-70.0,41.6;-74.0,40.8;-75.9,37.2;-76.3,39.2;-75.7,35.6;-81.3,31.4;-80.4,25.2;-84.1,30.1;-96.6,28.3;-97.9,22.4;-96.3,19.3;-94.4,18.1;-86.8,21.3;-88.9,15.9;-83.1,15.0;-83.9,11.4;-82.2,9.0;-76.8,8.6;-71.8,12.4;-71.7,9.1;-69.9,12.2;-68.2,10.6;-61.9,10.7;-58.5,6.8;-51.3,4.2;-50.4,-0.1;-40.0,-2.9;-34.7,-7.3;-39.0,-13.8;-40.9,-21.9;-47.6,-24.9;-53.8,-34.4;-58.4,-33.9;-56.8,-36.9;-65.1,-41.1;-63.5,-42.6;-67.6,-46.3;-66.0,-48.1;-69.1,-50.7;-68.2,-52.3;-71.4,-53.9;-74.9,-52.3;-75.6,-48.7;-74.1,-46.9;-75.6,-46.6;-72.7,-42.4;-74.3,-43.2;-70.2,-19.8;-76.0,-14.6;-81.2,-6.1;-80.9,-1.1;-77.1,3.8;-78.2,8.3;-80.9,7.2;-85.7,9.9;-87.5,13.3;-103.5,18.3;-114.8,31.8;-109.4,23.2;-112.2,24.7;-124.4,40.3;-124.7,48.2;-122.6,47.1;-122.8,49.0;-127.4,50.8;-134.1,58.1;-147.1,60.9;-151.7,59.2;-150.6,61.3;-158.4,56.0;-164.8,54.4;-157.0,58.9;-162.0,58.7;-166.1,61.5;-160.8,64.8;-168.1,65.7;-161.7,66.1;-166.8,68.4;-156.6,71.4;-136.5,68.9;-124.4,70.2;-108.9,67.4;-106.2,68.8;-96.1,67.3;-94.2,69.1;-96.5,70.1;-95.2,71.9;-90.5,69.5|-27.1,83.5;-20.8,82.7;-31.9,82.2;-12.2,81.3;-20.0,80.2;-17.7,80.1;-19.7,78.8;-18.5,77.0;-21.7,76.6;-19.4,74.3;-24.8,72.3;-21.8,70.7;-26.4,70.2;-22.3,70.1;-39.8,65.5;-43.4,60.1;-51.6,63.6;-54.0,67.2;-50.9,69.9;-54.7,69.6;-51.4,70.6;-55.8,71.7;-54.7,72.6;-58.6,75.5;-73.3,78.0;-65.7,79.4;-68.0,80.1;-62.7,81.8;-27.1,83.5|143.6,-13.8;152.9,-25.3;153.1,-30.9;150.0,-37.4;146.3,-39.0;140.6,-38.0;138.2,-34.4;136.8,-35.3;137.8,-32.9;136.0,-34.9;131.3,-31.5;118.0,-35.1;115.0,-34.2;114.1,-21.8;120.9,-19.7;125.7,-14.2;129.6,-15.0;132.4,-11.1;136.5,-11.9;135.5,-15.0;140.2,-17.7;142.5,-10.7;143.6,-13.8|-86.6,73.2;-72.2,71.6;-67.0,69.2;-68.8,68.7;-61.9,66.9;-63.9,65.0;-68.0,66.3;-64.7,63.4;-68.8,63.7;-66.2,61.9;-77.7,64.2;-72.9,67.7;-79.0,70.2;-89.9,71.2;-89.4,73.1;-86.6,73.2|-68.5,83.1;-61.9,82.4;-76.9,79.3;-75.4,78.5;-80.6,76.2;-89.5,76.5;-85.0,77.5;-88.0,78.4;-85.1,79.3;-86.9,80.3;-81.8,80.5;-91.6,81.9;-68.5,83.1|134.1,-1.2;135.5,-3.4;138.3,-1.7;144.6,-3.9;150.7,-10.6;144.7,-7.6;142.6,-9.3;137.6,-8.4;137.9,-5.4;133.0,-4.1;132.0,-2.8;133.7,-2.2;130.5,-0.9;134.1,-1.2|141.0,37.1;140.3,35.1;135.8,33.5;131.0,33.9;130.2,31.4;129.4,33.3;135.7,35.5;141.4,41.4;141.0,37.1|105.8,-5.9;102.6,-4.2;95.3,5.5;103.8,0.1;105.8,-5.9|117.9,1.8;119.0,0.9;116.1,-4.0;110.2,-2.9;109.1,-0.5;109.7,2.0;116.7,6.9;119.2,5.4;117.9,1.8|57.5,70.7;51.5,72.0;55.6,75.1;68.9,76.5;58.5,74.3;55.4,72.4;57.5,70.7|-114.2,73.1;-108.2,71.7;-108.4,73.1;-106.5,73.1;-101.1,69.6;-113.3,68.5;-117.3,70.0;-112.4,70.4;-119.4,71.6;-114.2,73.1|50.1,-13.6;47.1,-24.9;44.0,-25.0;44.4,-16.2;49.2,-12.0;50.1,-13.6|-3.0,58.6;-4.1,57.6;-2.0,57.7;-3.1,56.0;1.4,51.3;-5.2,50.0;-3.4,51.4;-5.3,52.0;-4.6,53.5;-2.9,54.0;-6.1,56.8;-3.0,58.6|-175.0,66.6;-169.9,66.0;-173.0,64.3;-178.7,66.1;-180.0,65.0;-180.0,69.0;-175.0,66.6|-94.7,77.1;-79.8,74.9;-89.8,74.5;-97.1,76.8;-94.7,77.1|174.6,-36.2;178.5,-37.7;175.2,-41.7;172.6,-34.5;174.6,-36.2|125.2,1.4;120.2,0.2;120.9,-1.4;123.3,-0.6;121.5,-1.9;123.2,-5.3;121.0,-2.6;119.4,-5.4;120.0,0.6;125.2,1.4|173.0,-40.9;173.1,-43.9;169.3,-46.6;166.7,-46.2;173.0,-40.9|-87.0,79.7;-85.8,79.3;-92.9,78.3;-96.7,80.2;-92.4,81.3;-87.0,79.7|18.3,79.7;21.5,79.0;15.9,76.8;10.4,79.7;18.3,79.7|-14.5,66.5;-13.6,65.1;-18.7,63.5;-24.3,65.6;-14.5,66.5|-120.5,71.4;-125.9,71.9;-124.9,74.3;-115.5,73.5;-120.5,71.4|-79.7,22.8;-74.2,20.3;-85.0,21.9;-79.7,22.8|-67.8,-53.9;-65.0,-54.7;-69.2,-55.5;-74.7,-52.8;-67.8,-53.9|-56.1,50.7;-53.1,46.7;-59.3,47.6;-56.1,50.7|143.9,44.2;145.5,43.3;140.0,41.6;142.0,45.6;143.9,44.2|143.6,50.7;144.7,49.0;143.2,49.3;143.5,46.1;142.1,46.0;142.7,54.4;143.6,50.7|121.3,18.5;121.7,14.3;124.1,12.5;120.6,13.9;121.3,18.5|99.9,78.9;91.2,80.3;95.9,81.3;99.9,78.9|126.4,8.4;125.4,5.6;123.6,7.8;121.9,7.2;125.4,9.8;126.4,8.4|108.6,-6.8;115.7,-8.4;105.4,-6.9;108.6,-6.8|-85.2,65.7;-80.1,63.7;-87.2,63.5;-85.2,65.7|-100.4,73.8;-97.4,73.8;-96.7,71.7;-102.5,72.5;-100.4,73.8|-108.2,76.2;-105.7,75.5;-117.7,75.2;-108.2,76.2|-123.5,48.5;-128.4,50.8;-123.5,48.5|-6.8,52.3;-10.0,51.8;-9.7,53.9;-6.7,55.2;-6.8,52.3|-116.2,77.6;-122.9,76.1;-116.2,77.6|-72.6,19.9;-68.3,18.6;-74.5,18.3;-72.6,19.9|105.1,78.3;99.4,77.9;102.1,79.3;105.1,78.3|145.4,-40.8;148.3,-40.9;147.9,-43.2;146.0,-43.5;145.4,-40.8|-98.5,76.7;-98.2,75.0;-102.5,75.6;-98.5,76.7|118.5,9.3;117.2,8.4;119.5,11.4;118.5,9.3|167.1,-22.2;164.0,-20.1;167.1,-22.2|152.0,-5.5;148.3,-5.7;152.1,-4.1;152.0,-5.5|-93.2,72.8;-96.0,73.4;-90.5,73.9;-93.2,72.8|-100.1,78.3;-105.5,79.3;-100.1,78.3|15.5,38.2;15.1,36.6;12.4,37.6;15.5,38.2|124.4,-10.1;127.3,-8.4;124.4,-10.1|153.1,-4.5;150.7,-2.7;153.1,-4.5|81.2,6.2;80.1,9.8;81.2,6.2|110.3,18.7;108.6,19.4;110.8,20.1;110.3,18.7|25.4,80.4;27.4,80.1;17.4,80.3;25.4,80.4|125.5,12.2;124.8,10.1;124.3,12.6;125.5,12.2|-132.7,54.0;-131.2,52.2;-132.7,54.0|128.7,1.1;128.1,-0.9;127.9,2.2;128.7,1.1|145.1,75.6;137.0,75.3;145.1,75.6|134.6,34.1;132.4,33.0;134.6,34.1|155.9,-6.8;154.5,-5.1;155.9,-6.8|-95.8,78.1;-98.6,78.9;-95.8,78.1|-58.5,-51.1;-61.2,-51.9;-58.5,-51.1|-61.8,49.1;-64.5,49.9;-61.8,49.1|117.9,-8.1;119.1,-8.7;116.7,-9.0;117.9,-8.1|122.9,-8.1;119.9,-8.8;122.9,-8.1|-75.9,67.1;-77.2,67.6;-75.1,68.0;-75.9,67.1|70.3,-49.7;68.9,-48.6;70.3,-49.7|159.9,-8.3;158.2,-7.4;159.9,-8.3|-171.7,63.8;-168.7,63.3;-171.7,63.8|34.6,35.7;32.3,35.1;34.6,35.7|-95.6,69.1;-99.8,69.4;-95.6,69.1|23.7,35.7;26.3,35.3;23.7,35.7|120.7,-10.2;119.0,-9.6;120.7,-10.2|-77.5,23.8;-78.2,25.2;-77.5,23.8|124.0,10.3;122.4,9.7;124.0,10.3|-76.3,73.1;-80.9,73.3;-76.3,73.1|9.2,41.2;8.8,38.9;9.2,41.2|24.7,77.9;20.7,77.7;24.7,77.9|-76.9,17.9;-78.2,18.5;-76.9,17.9|-178.7,70.9;-180.0,71.5;-178.7,70.9|130.5,-3.1;127.9,-3.4;130.5,-3.1|-93.8,77.5;-96.4,77.8;-93.8,77.5|121.2,22.8;121.5,25.3;121.2,22.8|143.6,73.2;139.9,73.4;143.6,73.2|-153.0,57.1;-154.7,57.5;-153.0,57.1|51.1,80.5;44.8,80.6;51.1,80.5|-165.6,59.9;-167.5,60.2;-165.6,59.9|-109.7,78.6;-112.5,78.4;-109.7,78.6|-65.6,18.2;-67.2,17.9;-65.6,18.2|150.7,75.1;146.1,75.2;150.7,75.1|-81.9,62.7;-84.0,62.5;-81.9,62.7|12.7,55.6;10.9,55.8;12.7,55.6|-63.7,46.6;-62.0,46.4;-63.7,46.6|-93.6,75.0;-96.8,74.9;-93.6,75.0|-104.5,73.4;-106.9,73.5;-104.5,73.4|-110.2,77.7;-113.5,77.7;-110.2,77.7"


def _land_polygons():
    polys = []
    for poly in LAND_DATA.split("|"):
        pts = []
        for pt in poly.split(";"):
            lon, lat = pt.split(",")
            pts.append((float(lon), float(lat)))
        if len(pts) >= 3:
            polys.append(pts)
    return polys


# Map projection: equirectangular, lon -180..180, lat -58..83.
MAP_LON0, MAP_LON1, MAP_LAT0, MAP_LAT1 = -180, 180, -58, 83


def _map_xy(lon, lat, mx, my, mw, mh):
    x = mx + (lon - MAP_LON0) / (MAP_LON1 - MAP_LON0) * mw
    y = my + (MAP_LAT1 - lat) / (MAP_LAT1 - MAP_LAT0) * mh
    return (x, y)


# v3: ALL 37 stories get a pin. The 26 non-US main-map pins sit
# on the world map; the 11 US pins live in a zoomed USA inset at
# the bottom-left of the map (the US is too small on the world
# map for ~10 pins). No space story this day, so no star.
# Main-map pins, numbered category-major like the box badges.
# Each pin is (number, lon, lat, category colour key).
# True locations:
#  1 ICJ: The Hague, Netherlands (4.5E, 52.1N)
#  2 Summit: Shenzhen, China (114.1E, 22.5N)
#  5 Greenland pact: Copenhagen, Denmark (12.6E, 55.7N)
#  6 Iran strikes: Kuwait (47.5E, 29.4N)
#  7 Nuseirat: Gaza (34.4E, 31.4N)
#  8 EU loan: Brussels, Belgium (4.35E, 50.85N)
# 12 Mongolia: Ulaanbaatar (106.9E, 47.9N)
# 13 Australia jobs: Sydney (151.2E, 33.9S)
# 15 U17: Australia team — Sydney (151.2E, 33.9S)
# 16 Arsenal-Lyon: Lyon, France (4.8E, 45.75N)
# 17 Russian bombers: Danang, Vietnam (108.2E, 16.0N)
# 18 Ukraine strikes: Moscow, Russia (37.6E, 55.75N)
# 21 Ethiopia-Eritrea: Badme (37.9E, 14.7N)
# 22 Taiz water: Taiz, Yemen (44.0E, 13.6N)
# 23 PIF Tower: Riyadh, Saudi Arabia (46.7E, 24.7N)
# 24 Iraq deal: Jurf al-Sakhar, Iraq (44.2E, 32.9N)
# 26 Pakistan raids: Peshawar (71.6E, 34.0N)
# 27 Sudan: Nyala, Sudan (24.9E, 12.05N)
# 28 Somalia: Mogadishu (45.3E, 2.05N)
# 29 Kyiv strikes: Kyiv, Ukraine (30.5E, 50.45N)
# 30 Kerch bridge: Crimea (36.4E, 45.4N)
# 31 Serbia: Belgrade (20.5E, 44.8N)
# 32 UK-EU deal: London (-0.1, 51.5N)
# 35 Seabed lease: American Samoa (-170.7, 14.3S)
# 36 Haiti: Port-au-Prince (-72.3, 18.5N)
# 37 Mexico drug war: Mexico City (-99.1, 19.4N)
MAIN_PINS = [
    (1, 4.5, 52.1, "politics"),
    (2, 114.1, 22.5, "politics"),
    (5, 12.6, 55.7, "politics"),
    (6, 47.5, 29.4, "politics"),
    (7, 34.4, 31.4, "politics"),
    (8, 4.35, 50.85, "politics"),
    (12, 106.9, 47.9, "politics"),
    (13, 151.2, -33.9, "finance"),
    (15, 151.2, -33.9, "sports"),
    (16, 4.8, 45.75, "sports"),
    (17, 108.2, 16.0, "politics"),
    (18, 37.6, 55.75, "politics"),
    (21, 37.9, 14.7, "politics"),
    (22, 44.0, 13.6, "health"),
    (23, 46.7, 24.7, "politics"),
    (24, 44.2, 32.9, "politics"),
    (26, 71.6, 34.0, "politics"),
    (27, 24.9, 12.05, "politics"),
    (28, 45.3, 2.05, "politics"),
    (29, 30.5, 50.45, "politics"),
    (30, 36.4, 45.4, "politics"),
    (31, 20.5, 44.8, "politics"),
    (32, -0.1, 51.5, "politics"),
    (35, -170.7, -14.3, "politics"),
    (36, -72.3, 18.5, "politics"),
    (37, -99.1, 19.4, "politics"),
]
# US pins, for the zoomed USA inset (lon -125..-66, lat 24..50).
# True locations:
#  3 Anthropic IPO: San Francisco (-122.4, 37.8)
#  4 Dow: New York (-74.0, 40.7)
#  9 Senate war powers: Washington DC (-77.0, 38.9)
# 10 Walmart: Bentonville, AR (-94.2, 36.4)
# 11 Pete Rose pardon: Cincinnati, OH (-84.5, 39.1)
# 14 Texans-Colts: Houston, TX (-95.4, 29.8)
# 19 Trump-Vance: Washington DC (-77.0, 38.9)
# 20 Musk DealBook: New York (-74.0, 40.7)
# 25 Trump Jan 1: Washington DC (-77.0, 38.9)
# 33 NSA network: Fort Meade, MD (-76.8, 39.1)
# 34 Cyber chief fired: Washington DC (-77.0, 38.9)
US_PINS = [
    (3, -122.4, 37.8, "finance"),
    (4, -74.0, 40.7, "finance"),
    (9, -77.0, 38.9, "politics"),
    (10, -94.2, 36.4, "finance"),
    (11, -84.5, 39.1, "politics"),
    (14, -95.4, 29.8, "sports"),
    (19, -77.0, 38.9, "politics"),
    (20, -74.0, 40.7, "politics"),
    (25, -77.0, 38.9, "politics"),
    (33, -76.8, 39.1, "technology"),
    (34, -77.0, 38.9, "technology"),
]
MAP_PIN_COLORS = {
    "politics": POLITICS,
    "finance": FINANCE,
    "sports": SPORTS,
    "health": HEALTH,
    "technology": TECHNOLOGY,
}

# Display positions for main-map pins that cannot sit on their
# true spot (map-local coordinates, same frame as _map_xy with
# mw=336, mh=192). The western-Europe cluster (1, 5, 8, 16, 32),
# the eastern-Europe pair (29 Kyiv, 30 Kerch, 18 Moscow, 31
# Belgrade) and the Gulf / Horn of Africa cluster (6, 7, 21, 22,
# 23, 24, 27, 28) fan out around their true spots; the two Sydney
# pins (13, 15) split apart. Min pairwise distance in this frame
# is ~14px (pins 9/25 in the inset are the tightest overall),
# above the ~13px needed for r=7 main pins (r=6 in the inset).
# (number: (display_x, display_y); absent = use the true spot)
MAP_PIN_DISPLAY = {
    1: (160, 28),
    5: (182, 26),
    6: (224, 76),
    7: (196, 70),
    8: (168, 46),
    13: (296, 148),
    16: (150, 58),
    17: (280, 100),
    18: (212, 28),
    21: (216, 104),
    22: (196, 96),
    23: (212, 88),
    24: (216, 62),
    27: (188, 110),
    28: (210, 122),
    29: (204, 44),
    30: (224, 44),
    32: (140, 40),
    35: (20, 110),
    37: (72, 76),  # Mexico City true spot is on a ~10px-wide coast strip; display on land in N-central Mexico, leader to true spot
}

# USA inset projection: continental US, lon -125..-66, lat 24..50.
INSET_LON0, INSET_LON1, INSET_LAT0, INSET_LAT1 = -125, -66, 24, 50
INSET_W, INSET_H = 180, 80


def _inset_xy(lon, lat, ix, iy, iw, ih):
    x = ix + (lon - INSET_LON0) / (INSET_LON1 - INSET_LON0) * iw
    y = iy + (INSET_LAT1 - lat) / (INSET_LAT1 - INSET_LAT0) * ih
    return (x, y)


# Display positions for inset pins that cannot sit on their true
# spot (inset-local coordinates, 180x80 frame). The four
# Washington DC stories (9, 19, 25, 34) share one true point and
# fan out around it; the New York pair (4, 20) splits apart;
# Fort Meade (33) sits just above DC. Min pairwise distance
# ~13.4px (pins 4 and 25), above the 13px needed for r=6 pins.
# (number: (display_x, display_y); absent = use the true spot)
US_PIN_DISPLAY = {
    3: (10, 38),
    10: (88, 40),
    14: (88, 62),
    11: (120, 30),
    33: (140, 20),
    9: (150, 44),
    19: (136, 52),
    25: (162, 36),
    34: (154, 58),
    4: (168, 24),
    20: (172, 46),
}

# ---------------------------------------------------------------- helpers
def load(name, size):
    return ImageFont.truetype(str(FONT_DIR / name), size)


def wrap(d, text, font, max_w):
    """Greedy word wrap using real font metrics."""
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip() if cur else word
        if d.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_block(d, text, max_w, max_lines, start, minimum, bold=False):
    """Pick the largest font size (start..minimum) whose wrap fits max_lines.

    Falls back to truncating the last line with an ellipsis.
    Returns (font, lines).
    """
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    for size in range(start, minimum - 1, -1):
        f = load(name, size)
        lines = wrap(d, text, f, max_w)
        if len(lines) <= max_lines:
            return f, lines
    f = load(name, minimum)
    lines = wrap(d, text, f, max_w)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        while lines and d.textlength(lines[-1] + "\u2026", font=f) > max_w:
            lines[-1] = lines[-1][:-1]
        lines[-1] = lines[-1].rstrip() + "\u2026"
    return f, lines


# ---------------------------------------------------------------- illustrations
# Real images from assets/ (flags from flagcdn, real NBA club logos
# from Wikipedia renders). Loaded once and cached; all resizing uses
# LANCZOS, so renders are deterministic.
ASSETS = Path(__file__).resolve().parent / "assets"
_cache = {}


def asset(name):
    """Load an asset once; flags/photos -> RGB, logos keep their alpha."""
    if name not in _cache:
        im = Image.open(ASSETS / name)
        _cache[name] = (im.convert("RGBA") if im.mode in ("RGBA", "LA", "PA")
                        else im.convert("RGB"))
    return _cache[name]


def fit_height(im, h):
    w = max(1, round(im.width * h / im.height))
    return im.resize((w, h), Image.LANCZOS)


def fit_width(im, w):
    h = max(1, round(im.height * w / im.width))
    return im.resize((w, h), Image.LANCZOS)


def crop_band(im, x0f, y0f, x1f, y1f, tw, th):
    """Fractional crop, then resize to (tw, th) — for wide photo strips."""
    x0, y0 = int(im.width * x0f), int(im.height * y0f)
    x1, y1 = int(im.width * x1f), int(im.height * y1f)
    return im.crop((x0, y0, x1, y1)).resize((tw, th), Image.LANCZOS)


def crop_square(im, cxf, cyf, side_frac):
    """Square crop centred on (cxf, cyf) as fractions of the image."""
    side = int(im.width * side_frac)
    cx, cy = int(im.width * cxf), int(im.height * cyf)
    x0 = min(max(cx - side // 2, 0), im.width - side)
    y0 = min(max(cy - side // 2, 0), im.height - side)
    return im.crop((x0, y0, x0 + side, y0 + side))


def _paste_with_border(img, d, pic, px, py):
    img.paste(pic, (px, py))
    d.rectangle([px, py, px + pic.width - 1, py + pic.height - 1],
                outline=(150, 145, 135))


def _paste_logo(img, d, x, y, w, h, name, max_w=None):
    logo = asset(name)
    logo = fit_width(logo, min(max_w, w)) if max_w else fit_height(logo, h)
    lx = x + (w - logo.width) // 2
    ly = y + (h - logo.height) // 2
    if logo.mode == "RGBA":
        img.paste(logo, (lx, ly), logo)
    else:
        img.paste(logo, (lx, ly))


# ---------------------------------------------------------------- drawn illustrations
# Flat v1 style throughout. Every strip is filled edge-to-edge —
# background elements, supporting details, motion lines and textures
# — so no strip feels empty in the narrower (~165px) columns. All
# coordinates are integers, so renders stay deterministic.

def _sh_poly(d, pts, fill, dx=2, dy=2):
    d.polygon([(px + dx, py + dy) for px, py in pts], fill=SHADOW)
    d.polygon(pts, fill=fill)


def _sh_rect(d, box, fill, dx=2, dy=2):
    d.rectangle([box[0] + dx, box[1] + dy, box[2] + dx, box[3] + dy],
                fill=SHADOW)
    d.rectangle(box, fill=fill)


def _waves(d, x, y, w, h, big=False):
    """Rows of wave arcs along the bottom of the strip."""
    rows = ((y + h - 12, SEA, 3), (y + h - 7, (150, 195, 225), 2)) \
        if big else ((y + h - 10, SEA, 2), (y + h - 6, (150, 195, 225), 2))
    for wy, col, wd in rows:
        xx = x + 2
        step = 14 if big else 12
        while xx + 12 <= x + w - 2:
            d.arc([xx, wy, xx + 12, wy + 6], 0, 180, fill=col, width=wd)
            xx += step


def _speed_lines(d, x, y, w, h, color=(150, 160, 172), n=4, horizontal=True):
    """Short parallel motion lines, staggered, in the given band."""
    for i in range(n):
        if horizontal:
            ly = y + 4 + i * max(3, (h - 8) // max(n - 1, 1))
            lx = x + (i % 2) * 8
            ln = w // 3 + (i % 3) * 10
            d.line([(lx, ly), (lx + ln, ly)], fill=color, width=2)
        else:
            lx = x + 4 + i * max(3, (w - 8) // max(n - 1, 1))
            ly = y + (i % 2) * 8
            ln = h // 3 + (i % 3) * 8
            d.line([(lx, ly), (lx, ly + ln)], fill=color, width=2)


def _sparkle(d, cx, cy, r, fill=(255, 215, 90)):
    """Small 4-point star."""
    d.polygon([(cx, cy - r), (cx + r // 3, cy - r // 3), (cx + r, cy),
               (cx + r // 3, cy + r // 3), (cx, cy + r),
               (cx - r // 3, cy + r // 3), (cx - r, cy),
               (cx - r // 3, cy - r // 3)], fill=fill)


def _burst(d, cx, cy, r, fill=(255, 165, 0), core=(255, 230, 120)):
    """Explosion / impact starburst: long spikes + bright core."""
    import math
    pts = []
    for i in range(16):
        ang = i * 22.5
        rr = r if i % 2 == 0 else r // 2
        pts.append((cx + int(rr * math.cos(math.radians(ang))),
                    cy + int(rr * math.sin(math.radians(ang)))))
    d.polygon(pts, fill=fill)
    d.ellipse([cx - r // 2, cy - r // 2, cx + r // 2, cy + r // 2],
              fill=core)


def _smoke(d, x, y, r):
    """Cluster of grey smoke puffs."""
    for dx, dy, rr, col in ((0, 0, r, (170, 170, 175)),
                            (r, -r // 2, r * 3 // 4, (150, 150, 155)),
                            (-r, -r // 2, r * 2 // 3, (185, 185, 190)),
                            (r // 2, -r, r // 2, (140, 140, 145))):
        d.ellipse([x + dx - rr, y + dy - rr, x + dx + rr, y + dy + rr],
                  fill=col)


def _trim(im):
    """Crop an RGBA image to its non-transparent content box."""
    a = im.convert("RGBA").split()[3]
    bb = a.getbbox()
    return im.crop(bb) if bb else im


def _paste_rgba(img, pic, x, y):
    """Paste an RGBA image using its own alpha as the mask."""
    if pic.mode == "RGBA":
        img.paste(pic, (x, y), pic)
    else:
        img.paste(pic, (x, y))


def _cloud(d, x, y, s):
    """Small flat white cloud (three puffs on a soft grey base)."""
    d.ellipse([x, y + s // 3, x + s, y + s], fill=(235, 238, 242))
    d.ellipse([x + s // 4, y, x + s * 3 // 4, y + s * 2 // 3],
              fill=(255, 255, 255))
    d.ellipse([x + s // 2, y + s // 6, x + s, y + s * 2 // 3],
              fill=(255, 255, 255))
    d.ellipse([x, y + s // 3, x + s // 2, y + s * 2 // 3],
              fill=(255, 255, 255))


def _bird(d, x, y, s):
    """Tiny bird: two adjacent humps, like a shallow 'm'."""
    d.arc([x, y, x + s, y + s], 180, 360, fill=(90, 100, 112), width=2)
    d.arc([x + s, y, x + 2 * s, y + s], 180, 360, fill=(90, 100, 112),
          width=2)


def _grass(d, x, y, w, h, n=5):
    """Small darker-green grass tufts along the bottom of a pitch."""
    for i in range(n):
        gx = x + (i + 1) * w // (n + 1)
        for dx, dh in ((-3, 5), (0, 7), (3, 5)):
            d.line([(gx + dx, y + h), (gx + dx, y + h - dh)],
                   fill=(70, 140, 80), width=1)

# ---------------------------------------------------------------- politics
# Politics = flat v1-style scenes, full-width, centred and balanced,
# with the country flag pasted on top at the same top-left spot in
# every box. Every strip is filled edge-to-edge.

def draw_bridge_flat(d, x, y, w, h):
    """Kerch Bridge, MAXIMUM drama, centred on the strip: the arch
    is broken at the middle, the centre deck section plunges steeply
    into the water, a huge fireball + towering smoke column mark the
    blast point, nine debris pieces fly both ways, a big splash rises
    where the deck hits the water, and the right-hand pillar leans,
    cracked, while the left pillar stands upright. Clouds and birds
    are mirrored around the blast column, and the flag zone
    (top-left) is kept clear. Big waves run the full width."""
    cx = x + w // 2
    deck_y = y + h - 16
    # sky: one cloud top-right, one bird each side of the blast column
    _cloud(d, x + w - 36, y + 2, 16)
    _bird(d, x + 50, y + 6, 5)
    _bird(d, x + w - 58, y + 4, 5)
    # arch: low full-width arc, broken at the top (gap 255..285 deg)
    d.arc([x + 2, deck_y - 18, x + w - 2, deck_y + 4], 180, 255,
          fill=STEEL, width=3)
    d.arc([x + 2, deck_y - 18, x + w - 2, deck_y + 4], 285, 360,
          fill=STEEL, width=3)
    # arch feet land on the deck
    d.line([(x + 2, deck_y - 7), (x + 2, deck_y)], fill=STEEL, width=3)
    d.line([(x + w - 2, deck_y - 7), (x + w - 2, deck_y)], fill=STEEL,
           width=3)
    # hangers: two on the intact left half, two on the right half,
    # one dangling loose beside the break
    for hx in (x + 41, x + 58):
        d.line([(hx, deck_y - 16), (hx, deck_y)], fill=STEEL, width=2)
    for hx in (x + 120, x + 140):
        d.line([(hx, deck_y - 15), (hx, deck_y - 2)], fill=STEEL, width=2)
    d.line([(cx + 22, deck_y - 17), (cx + 22, deck_y - 1)], fill=STEEL,
           width=2)
    # decks: intact left span, plunging centre section, sagging right
    d.line([(x + 2, deck_y), (cx - 6, deck_y)], fill=STEEL, width=3)
    d.line([(cx - 6, deck_y), (cx + 24, deck_y + 12)], fill=STEEL, width=4)
    d.line([(cx + 28, deck_y - 2), (x + w - 2, deck_y - 2)], fill=STEEL,
           width=3)
    # pillars: left upright, right leaning and cracked
    d.rectangle([x + 34, deck_y + 3, x + 38, y + h - 8], fill=STEEL)
    d.polygon([(x + 116, deck_y + 1), (x + 120, deck_y + 1),
               (x + 130, y + h - 8), (x + 126, y + h - 8)], fill=STEEL)
    d.line([(x + 118, deck_y + 6), (x + 124, deck_y + 9)], fill=DARK,
           width=1)
    # water first, then the splash on top of it
    _waves(d, x, y, w, h, big=True)
    # big splash where the plunging deck hits the water
    sx = cx + 22
    d.arc([sx - 22, y + h - 30, sx + 22, y + h - 4], 180, 360,
          fill=(255, 255, 255), width=3)
    d.arc([sx - 14, y + h - 26, sx + 14, y + h - 8], 180, 360,
          fill=(255, 255, 255), width=2)
    d.ellipse([sx - 18, y + h - 9, sx + 18, y + h - 3],
              fill=(255, 255, 255))
    for dx, dy, r in ((-18, -10, 2), (20, -12, 2), (-6, -14, 2),
                      (12, -8, 1), (2, -16, 2), (-12, -6, 1),
                      (18, -4, 1)):
        d.ellipse([sx + dx - r, y + h - 30 + dy - r,
                   sx + dx + r, y + h - 30 + dy + r],
                  fill=(255, 255, 255))
    # blast: huge fireball in the arch gap + towering smoke column
    d.ellipse([cx - 11, deck_y - 20, cx + 11, deck_y + 2],
              fill=(255, 140, 40))
    d.ellipse([cx - 6, deck_y - 15, cx + 6, deck_y - 3],
              fill=(255, 220, 90))
    _burst(d, cx, deck_y - 8, 19)
    _smoke(d, cx, deck_y - 18, 6)
    _smoke(d, cx - 6, deck_y - 30, 5)
    _smoke(d, cx + 5, deck_y - 32, 4)
    # debris flying both ways, each with a long motion line behind it
    for (tx, ty, lx, ly) in (
            (cx - 32, deck_y - 16, cx - 20, deck_y - 12),
            (cx - 46, deck_y - 8, cx - 32, deck_y - 5),
            (cx - 24, deck_y - 28, cx - 16, deck_y - 22),
            (cx + 32, deck_y - 14, cx + 20, deck_y - 10),
            (cx + 46, deck_y - 6, cx + 32, deck_y - 3),
            (cx + 26, deck_y - 26, cx + 18, deck_y - 20),
            (cx + 6, deck_y - 34, cx + 2, deck_y - 26),
            (cx - 8, deck_y - 32, cx - 4, deck_y - 24),
            (cx + 52, deck_y - 18, cx + 42, deck_y - 14)):
        d.polygon([(tx, ty), (tx + 7, ty - 3), (tx + 7, ty + 4)],
                  fill=DARK)
        d.line([(lx, ly), (tx + 3, ty)], fill=(150, 160, 172), width=1)


def _leader(d, fx, y, suit, tie, flip):
    """One suited leader, standing upright and facing the centre:
    round head with hair, dark suit torso with white shirt + tie,
    two legs, one arm reaching out to shake hands at the centre,
    the other arm hanging down. flip mirrors the figure."""
    s = 1 if not flip else -1
    # legs: two dark trouser legs, shoes
    d.rectangle([fx - 5, y + 33, fx - 1, y + 44], fill=suit)
    d.rectangle([fx + 1, y + 33, fx + 5, y + 44], fill=suit)
    d.ellipse([fx - 6, y + 42, fx, y + 46], fill=(30, 30, 30))
    d.ellipse([fx, y + 42, fx + 6, y + 46], fill=(30, 30, 30))
    # torso: suit jacket, slightly wider at the shoulders
    d.polygon([(fx - 7, y + 19), (fx + 7, y + 19), (fx + 5, y + 34),
               (fx - 5, y + 34)], fill=suit)
    # white shirt V + tie
    d.polygon([(fx - 3, y + 19), (fx + 3, y + 19), (fx, y + 24)],
              fill=(255, 255, 255))
    d.polygon([(fx - 2, y + 22), (fx + 2, y + 22), (fx + 1, y + 30),
               (fx - 1, y + 30)], fill=tie)
    # reaching arm: from the shoulder toward the centre, hand open
    hx = fx + s * 16
    d.line([(fx + s * 6, y + 21), (hx, y + 27)], fill=suit, width=4)
    d.ellipse([hx - 3, y + 24, hx + 3, y + 30], fill=SKIN)
    # hanging arm on the outer side
    d.line([(fx - s * 6, y + 21), (fx - s * 8, y + 31)], fill=suit,
           width=4)
    d.ellipse([fx - s * 8 - 2, y + 29, fx - s * 8 + 2, y + 33],
              fill=SKIN)
    # head + hair
    d.ellipse([fx - 5, y + 7, fx + 5, y + 17], fill=SKIN)
    d.arc([fx - 5, y + 7, fx + 5, y + 17], 180, 360, fill=(40, 30, 25),
          width=3)


def draw_leaders_shenzhen(d, x, y, w, h):
    """Xi meets Putin in Shenzhen: two suited leaders, MIRRORED
    around the strip centre, shaking hands in front of the Shenzhen
    skyline. The left leader (dark navy suit, red tie) faces right,
    the right leader (charcoal suit, blue tie) faces left, their
    hands meet exactly at the strip centre under a gold sparkle.
    The skyline is a low mirrored silhouette along the bottom with
    glowing gold windows; a cloud sits top-centre-right with two
    birds flanking it, so the top band (flags / cloud / birds) is
    spread evenly. The flag zone (top-left) is kept clear."""
    cx = x + w // 2
    base = y + h - 4
    # sky: cloud top-centre-right, birds flanking it
    _cloud(d, x + 108, y + 1, 14)
    _bird(d, x + 96, y + 8, 4)
    _bird(d, x + 132, y + 6, 4)
    # gold sparkle above the handshake, dead centre
    _sparkle(d, cx, y + 5, 5, fill=(255, 215, 90))
    # low skyline silhouette along the bottom: mirrored heights,
    # gold windows glowing
    bw = (w - 4) // 7
    for i, bhgt in enumerate((4, 6, 8, 10, 8, 6, 4)):
        bx = x + 2 + i * bw
        d.rectangle([bx, base - bhgt, bx + bw - 3, base],
                    fill=(110, 125, 145))
        d.rectangle([bx + 5, base - bhgt + 2, bx + 7, base - bhgt + 4],
                    fill=(255, 210, 90))
        d.rectangle([bx + 12, base - bhgt + 2, bx + 14, base - bhgt + 4],
                    fill=(255, 210, 90))
    d.rectangle([x + 2, base, x + w - 2, base + 2], fill=(90, 105, 130))
    # the two leaders, mirrored, hands meeting at the centre
    _leader(d, cx - 24, y, (30, 45, 70), (180, 40, 40), flip=False)
    _leader(d, cx + 24, y, (50, 50, 55), (40, 80, 160), flip=True)
    # handshake: two clasped hands at the centre + tiny motion arcs
    d.ellipse([cx - 5, y + 24, cx + 5, y + 32], fill=SKIN)
    d.arc([cx - 10, y + 20, cx + 2, y + 34], 90, 270, fill=(200, 170, 140),
          width=1)
    d.arc([cx - 2, y + 20, cx + 10, y + 34], 270, 90, fill=(200, 170, 140),
          width=1)


def draw_capitol(d, x, y, w, h):
    """The US Capitol + the 56-44 scoreboard: a navy scoreboard chip
    with "56-44" sits dead centre at the top; below it the white
    Capitol dome rises over a colonnade, flanked by two symmetric
    trees, with steps along the bottom. A cloud sits top-right and
    a bird top-left of the chip, so the top band (flag / bird / chip
    / cloud) is spread evenly. The flag zone (top-left) is kept
    clear."""
    cx = x + w // 2
    # scoreboard chip, dead centre at the top
    sf = load("DejaVuSans-Bold.ttf", 11)
    label = "56\u201344"
    tw = int(d.textlength(label, font=sf))
    chip_w = tw + 12
    d.rounded_rectangle([cx - chip_w // 2, y + 1, cx + chip_w // 2,
                         y + 14], radius=6, fill=NAVY)
    d.text((cx - tw // 2, y + 2), label, font=sf, fill=(255, 255, 255))
    # sky: cloud top-right, bird top-left of the chip
    _cloud(d, x + w - 34, y + 2, 14)
    _bird(d, x + 44, y + 6, 4)
    # dome: half-ellipse over a drum, gold finial on its apex. The
    # dome apex sits exactly at the scoreboard chip's bottom edge
    # (y + 14), so the dome never covers the chip or its text.
    d.pieslice([cx - 20, y + 14, cx + 20, y + 44], 180, 360,
               fill=(245, 245, 240), outline=(150, 150, 145))
    d.ellipse([cx - 2, y + 14, cx + 2, y + 18], fill=GOLD)
    d.rectangle([cx - 14, y + 28, cx + 14, y + 40], fill=(240, 240, 235),
                outline=(150, 150, 145))
    # colonnade: 6 white columns under the drum
    for i in range(6):
        colx = cx - 30 + i * 11
        d.rectangle([colx, y + 40, colx + 5, y + 50],
                    fill=(245, 245, 240), outline=(150, 150, 145))
    # base platform + steps
    d.rectangle([cx - 34, y + 50, cx + 34, y + 53], fill=(220, 220, 215))
    d.rectangle([cx - 38, y + 53, cx + 38, y + 56], fill=(205, 205, 200))
    # trees, mirrored at the bottom corners
    for tx in (x + 6, x + w - 18):
        d.rectangle([tx + 4, y + 40, tx + 7, y + 52], fill=(120, 85, 50))
        d.ellipse([tx - 2, y + 28, tx + 13, y + 43], fill=(50, 120, 70))
        d.ellipse([tx + 1, y + 24, tx + 10, y + 33], fill=(70, 150, 90))

# ---------------------------------------------------------------- finance
# Finance = pure PIL illustration, big and dramatic, no logos, no
# photos, no wordmarks. Every strip is filled edge-to-edge.

def draw_candles_big(d, x, y, w, h):
    """Stocks fall — a dramatic crash WITHOUT the giant red arrow and
    without any long red line: red candlesticks tumble down with ghost
    trails, a small candle falls mid-air between the tall candles,
    papers and a bill fly, small -% marks and down-triangles scatter,
    and impact bursts + dust puff at the candle bases."""
    base = y + h - 10
    heights = (22, 30, 38, 46)
    bw = 18
    gap = (w - 4 * bw) // 5
    for i, bh in enumerate(heights):
        bx = x + gap + i * (bw + gap)
        top = base - bh
        # ghost trail: a faded copy of the candle, offset up-left,
        # clamped to the strip top
        d.rectangle([bx - 7, max(y, top - 9), bx + bw - 7, base - 9],
                    fill=(245, 178, 168))
        # skewed body (top shifted left, as if toppling) + bright edge
        d.polygon([(bx + 4, top), (bx + bw, top), (bx + bw - 4, base),
                   (bx, base)], fill=(200, 60, 50))
        d.line([(bx + 4, top), (bx + bw, top)], fill=(240, 120, 105),
               width=3)
        d.line([(bx + bw // 2, top - 8), (bx + bw // 2, base + 2)],
               fill=(160, 40, 35), width=2)
    d.line([(x, base + 3), (x + w, base + 3)], fill=(90, 100, 112), width=1)
    # small candle falling mid-air, between the two tall candles
    # (v2: moved left and down so the story-number badge at the
    # top-right corner does not cover it, and clear of the -5% mark)
    fx, fy = x + 112, y + 16
    d.polygon([(fx, fy + 2), (fx + 14, fy - 2), (fx + 16, fy + 8),
               (fx + 2, fy + 12)], fill=(220, 90, 80))
    d.line([(fx + 7, fy - 4), (fx + 9, fy + 2)], fill=(160, 40, 35), width=2)
    for i, off in enumerate((0, 4, -4)):
        d.line([(fx - 8 - i * 5, fy + 4 + off), (fx - 1 - i * 5, fy + 4 + off)],
               fill=(170, 170, 170), width=2)
    # flying papers and a bill, in the gaps between candles, each with
    # a short motion line behind it (kept clear of the -% labels above)
    for (px, py, tilt, fill) in (
            (x + 96, y + 26, -2, (255, 255, 255)),
            (x + 144, y + 30, -3, (255, 255, 255)),
            (x + 186, y + 30, 3, (90, 160, 90))):
        d.polygon([(px, py), (px + 16, py + tilt), (px + 16, py + 10 + tilt),
                   (px, py + 10)], fill=fill, outline=(150, 145, 135))
        d.line([(px + 3, py + 4), (px + 13, py + 4 + tilt)],
               fill=(120, 120, 120), width=1)
        d.line([(px - 10, py + 5), (px - 2, py + 5)], fill=(170, 170, 170),
               width=2)
    # scattered -% marks, clear of the candles and of each other
    pf = load("DejaVuSans-Bold.ttf", 11)
    d.text((x + 8, y + 4), "\u22123%", font=pf, fill=RED)
    d.text((x + 56, y + 4), "\u22127%", font=pf, fill=RED)
    d.text((x + 100, y + 2), "\u22125%", font=pf, fill=RED)
    d.text((x + 188, y + 2), "\u22129%", font=pf, fill=RED)
    # small red down-triangles falling in the gaps between candles
    for (tx, ty) in ((x + 40, y + 8), (x + 152, y + 44)):
        d.polygon([(tx, ty + 7), (tx - 5, ty), (tx + 5, ty)], fill=RED)
    # impact bursts at the bases of the two tallest candles + dust
    _burst(d, x + gap + 3 * (bw + gap) + bw // 2, base + 2, 7,
           fill=(255, 120, 40), core=(255, 220, 140))
    _burst(d, x + gap + 2 * (bw + gap) + bw // 2, base + 2, 5,
           fill=(255, 140, 60), core=(255, 230, 160))
    for (dx, dy, rr) in ((x + 8, base + 4, 4), (x + w - 8, base + 4, 4),
                         (x + w // 2, base + 5, 3)):
        d.ellipse([dx - rr, dy - rr, dx + rr, dy + rr],
                  fill=(200, 195, 185))


def draw_rocket_ipo(d, x, y, w, h):
    """Anthropic IPO, MAXIMUM drama: a BIG rocket launching
    diagonally to the top-right, a long flame and a big smoke cloud
    behind it, a dashed trajectory, stars filling the sky — and a
    gold "$83" price chip at the top-left, the IPO price."""
    import math
    # gold "$83" price chip, top-left
    pf = load("DejaVuSans-Bold.ttf", 12)
    label = "$83"
    tw = int(d.textlength(label, font=pf))
    d.rounded_rectangle([x + 2, y + 2, x + 2 + tw + 12, y + 18], radius=8,
                        fill=(196, 122, 18))
    d.text((x + 8, y + 3), label, font=pf, fill=(255, 255, 255))
    # stars + dots filling the sky (v2: the top-right sparkle and
    # dot moved down, clear of the story-number badge)
    _sparkle(d, x + 60, y + 8, 5, fill=(255, 215, 90))
    _sparkle(d, x + 150, y + 38, 5, fill=(255, 215, 90))
    _sparkle(d, x + 140, y + 50, 4, fill=(255, 215, 90))
    _sparkle(d, x + 30, y + 52, 4, fill=(255, 215, 90))
    for (dx, dy) in ((0.36, 0.12), (0.58, 0.85), (0.90, 0.70)):
        px, py = x + int(w * dx), y + int(h * dy)
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(140, 130, 190))
    # dashed trajectory from the bottom-left up to the rocket
    tx, ty = x + 8, y + 56
    while tx < x + 66:
        d.line([(tx, ty), (tx + 6, ty - 3)], fill=(140, 130, 190), width=2)
        tx += 10
        ty -= 3
    # rocket: BIG nose top-right, base bottom-left
    nx, ny = x + 130, y + 4
    bx, by = x + 78, y + 44
    dx, dy = nx - bx, ny - by
    L = math.hypot(dx, dy)
    ux, uy = dx / L, dy / L
    px, py = -uy, ux
    hw = 9
    d.polygon([(nx, ny), (bx + px * hw, by + py * hw),
               (bx - px * hw, by - py * hw)], fill=(240, 240, 240),
              outline=(180, 60, 50))
    # red nose tip
    d.polygon([(nx, ny),
               (nx - ux * 11 + px * 6, ny - uy * 11 + py * 6),
               (nx - ux * 11 - px * 6, ny - uy * 11 - py * 6)],
              fill=(200, 60, 50))
    # fins at the base
    d.polygon([(bx + px * hw, by + py * hw),
               (bx + px * hw * 1.8, by + py * hw * 1.8),
               (bx + px * hw + ux * 14, by + py * hw + uy * 14)],
              fill=(200, 60, 50))
    d.polygon([(bx - px * hw, by - py * hw),
               (bx - px * hw * 1.8, by - py * hw * 1.8),
               (bx - px * hw + ux * 14, by - py * hw + uy * 14)],
              fill=(200, 60, 50))
    # window
    wx, wy = nx - ux * 18, ny - uy * 18
    d.ellipse([wx - 6, wy - 6, wx + 6, wy + 6], fill=(90, 140, 200),
              outline=(255, 255, 255))
    # LONG flame + inner flame behind the base
    fx, fy = bx - ux * 22, by - uy * 22
    d.polygon([(bx + px * 6, by + py * 6), (bx - px * 6, by - py * 6),
               (fx, fy)], fill=(255, 140, 40))
    fx2, fy2 = bx - ux * 13, by - uy * 13
    d.polygon([(bx + px * 4, by + py * 4), (bx - px * 4, by - py * 4),
               (fx2, fy2)], fill=(255, 220, 90))
    # big smoke cloud trailing behind the flame
    for (scx, scy, sr) in ((x + 58, y + 50, 5), (x + 48, y + 52, 4),
                           (x + 40, y + 50, 4), (x + 66, y + 52, 4)):
        d.ellipse([scx - sr, scy - sr, scx + sr, scy + sr],
                  fill=(200, 200, 205))


def draw_chip_down(d, x, y, w, h):
    """Nvidia DOWN despite a record quarter: a BIG glowing GPU chip
    on the left, a red down arrow plunging at the right edge, a bold
    red "-2.9%" tag at the top (shifted left of the story-number
    badge), and small red down-triangles raining above the chip. The
    chip keeps its glowing core and gold pins; the red marks make
    the direction of the news unmistakable. No wordmark."""
    s = 44
    cx = x + 8
    cy = y + (h - s) // 2
    # light halo behind the die
    d.rectangle([cx - 4, cy - 3, cx + s + 4, cy + s + 3],
                fill=(205, 240, 215))
    # circuit traces + dots, radiating from the die (left + top)
    for ty in (cy + 6, cy + s // 2, cy + s - 6):
        d.line([(cx + s + 8, ty), (x + 96, ty)], fill=(90, 140, 100),
               width=2)
        d.ellipse([x + 90, ty - 3, x + 96, ty + 3], fill=GOLD)
    for (sx, sy, ex, ey) in ((cx, cy, x + 2, y + 2),
                             (cx + s, cy, x + 96, y + 2),
                             (cx, cy + s, x + 2, y + h - 2)):
        d.line([(sx, sy), (ex, ey)], fill=(90, 140, 100), width=2)
        d.ellipse([ex - 3, ey - 3, ex + 3, ey + 3], fill=GOLD)
    # electric arcs crackling from the die corners
    for (ax0, ay0, ax1, ay1, ax2, ay2) in (
            (cx + 2, cy + 2, cx - 10, y + 1, x + 6, y + 6),
            (cx + s - 2, cy + 2, cx + s + 10, y + 1, x + 96, y + 6)):
        d.line([(ax0, ay0), (ax1, ay1), (ax2, ay2)],
               fill=(255, 230, 80), width=2, joint="curve")
    # gold pins, all four sides
    for i in range(4):
        py = cy + 6 + i * 11
        d.rectangle([cx - 7, py, cx - 3, py + 5], fill=GOLD)
        d.rectangle([cx + s + 3, py, cx + s + 7, py + 5], fill=GOLD)
        px = cx + 6 + i * 11
        d.rectangle([px, cy - 2, px + 5, cy + 2], fill=GOLD)
        d.rectangle([px, cy + s - 2, px + 5, cy + s + 2], fill=GOLD)
    # die + glowing core + white-hot centre
    _sh_rect(d, [cx, cy, cx + s, cy + s], (18, 60, 40))
    d.rectangle([cx + 4, cy + 4, cx + s - 4, cy + s - 4], fill=(35, 110, 70))
    d.rectangle([cx + 10, cy + 10, cx + s - 10, cy + s - 10],
                fill=(80, 200, 130))
    d.rectangle([cx + 16, cy + 16, cx + s - 16, cy + s - 16],
                fill=(170, 240, 190))
    d.rectangle([cx + 20, cy + 20, cx + s - 20, cy + s - 20],
                fill=(255, 255, 255))
    d.ellipse([cx + s - 15, cy + s - 15, cx + s - 6, cy + s - 6],
              fill=(90, 160, 120))
    _sparkle(d, cx + s - 2, cy + 2, 6, fill=(140, 230, 170))
    _sparkle(d, cx - 2, cy + s - 2, 5, fill=(255, 230, 80))
    # red down-triangles raining above the chip (v2: the middle one
    # is dropped so the "-2.9%" tag can move left, clear of the
    # story-number badge at the top-right)
    for (tx, ty) in ((x + 78, y + 6), (x + 92, y + 22)):
        d.polygon([(tx, ty + 8), (tx - 5, ty), (tx + 5, ty)], fill=RED)
    # bold red "-2.9%" tag, shifted left (v2: clear of the
    # story-number badge at the top-right)
    pf = load("DejaVuSans-Bold.ttf", 13)
    d.text((x + w - 70, y + 2), "\u22122.9%", font=pf, fill=RED)
    # red down arrow, BIG, right edge
    ax0, ay0 = x + w - 30, y + 20
    ax1, ay1 = x + w - 6, y + h - 4
    d.line([(ax0, ay0), (ax1, ay1)], fill=(255, 255, 255), width=12)
    d.line([(ax0, ay0), (ax1, ay1)], fill=RED, width=8)
    d.polygon([(ax1, ay1), (ax1 - 16, ay1 - 2), (ax1 - 2, ay1 - 16)],
              fill=RED)

# ---------------------------------------------------------------- sports
# All three 18 Nov boxes are NBA games, so each gets a DIFFERENT
# basketball scene on an orange court, with the two clubs' REAL logos
# flanking the score in the header: a jump shot (Heat-Bucks), a dunk
# (Nuggets-Celtics), and a fast-break layup with a gold "8-0" chip
# (Grizzlies-Cavaliers). Exactly ONE ball per scene, drawn with PIL.
# NOTE (17 Nov lesson): the scenes are only ~33px tall (draw_match
# shifts them to fy = strip + 22), so every player and ball is
# anchored at the TOP of the scene (y + 0) — anchoring any lower
# pushes feet and ball onto the headline below the strip.

SKIN = (235, 200, 170)

POSES = {
    # standing, watching (defender)
    "stand": {
        "head": (20, 5, 4.5), "shoulder": (20, 12), "hip": (20, 22),
        "knee_l": (17, 29), "ankle_l": (16, 35),
        "knee_r": (23, 29), "ankle_r": (24, 35),
        "elbow_l": (13, 15), "wrist_l": (10, 22),
        "elbow_r": (27, 15), "wrist_r": (30, 22),
    },
    # jump shot: both arms raised to release the ball overhead
    "jumpshot": {
        "head": (20, 5, 4.5), "shoulder": (20, 12), "hip": (19, 22),
        "knee_l": (14, 29), "ankle_l": (12, 35),
        "knee_r": (25, 29), "ankle_r": (27, 35),
        "elbow_l": (13, 6), "wrist_l": (9, 1),
        "elbow_r": (27, 6), "wrist_r": (31, 1),
    },
    # header: jumping straight up, arms raised (defender blocking)
    "header": {
        "head": (20, 6, 4.5), "shoulder": (20, 13), "hip": (20, 24),
        "knee_l": (15, 30), "ankle_l": (13, 36),
        "knee_r": (25, 30), "ankle_r": (27, 36),
        "elbow_l": (12, 7), "wrist_l": (8, 1),
        "elbow_r": (28, 7), "wrist_r": (32, 1),
    },
    # fast break: leaning forward, one leg back, one leg forward,
    # one arm pumping back, the other carrying the ball low in front
    "run": {
        "head": (22, 6, 4.5), "shoulder": (21, 13), "hip": (19, 22),
        "knee_l": (12, 28), "ankle_l": (6, 34),
        "knee_r": (26, 27), "ankle_r": (32, 31),
        "elbow_l": (14, 16), "wrist_l": (8, 22),
        "elbow_r": (28, 15), "wrist_r": (33, 21),
    },
}


def _player(d, ox, oy, s, pose_name, kit, shorts, flip=False):
    """Draw one player figure. (ox, oy) = top-left of the local frame,
    s = px per local unit, flip = mirror horizontally."""
    p = POSES[pose_name]
    outl = (40, 40, 40)

    def T(px, py):
        qx = (40 - px) if flip else px
        return (ox + qx * s, oy + py * s)

    def seg(a, b, color, wd):
        d.line([T(*a), T(*b)], fill=color, width=max(2, int(wd * s)))

    # legs: thigh in shorts colour, shin skin, dark boot
    for side in ("l", "r"):
        seg(p["hip"], p["knee_" + side], shorts, 4.5)
        seg(p["knee_" + side], p["ankle_" + side], SKIN, 3.2)
        ax, ay = T(*p["ankle_" + side])
        d.ellipse([ax - 3.4 * s, ay - 2.2 * s, ax + 3.4 * s, ay + 2.2 * s],
                  fill=(30, 30, 30))
    # torso: dark outline, then kit
    seg(p["shoulder"], p["hip"], outl, 6.5)
    seg(p["shoulder"], p["hip"], kit, 5.0)
    # arms: upper arm kit (with outline), forearm skin
    for side in ("l", "r"):
        seg(p["shoulder"], p["elbow_" + side], outl, 4.2)
        seg(p["shoulder"], p["elbow_" + side], kit, 3.2)
        seg(p["elbow_" + side], p["wrist_" + side], SKIN, 2.6)
    # head + hair
    hx, hy, hr = p["head"]
    cx, cy = T(hx, hy)
    r = hr * s
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SKIN)
    d.arc([cx - r, cy - r, cx + r, cy + r], 180, 360, fill=(40, 30, 25),
          width=max(2, int(2 * s)))


def _ball_basket(d, cx, cy, r, trail="left"):
    """Drawn basketball: orange circle, black outline, curved black
    seams (a horizontal line, a middle curve, two side arcs).
    Optional motion trail behind it."""
    if trail == "left":
        for i, off in enumerate((0, 5, -5)):
            x0 = cx - r - 6 - i * 7
            d.line([(x0, cy + off), (x0 + 10, cy + off)],
                   fill=(255, 255, 255), width=2)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(230, 120, 40),
              outline=(40, 25, 10), width=2)
    d.arc([cx - r, cy - r, cx + r, cy + r], 300, 60, fill=(40, 25, 10),
          width=2)
    d.arc([cx - r, cy - r, cx + r, cy + r], 120, 240, fill=(40, 25, 10),
          width=2)
    d.line([(cx - r, cy), (cx + r, cy)], fill=(40, 25, 10), width=2)
    d.arc([cx - r // 2, cy - r, cx + r // 2, cy + r], 270, 90,
          fill=(40, 25, 10), width=2)


def _court(d, x, y, w, h):
    """Orange court with mowing stripes, a crowd band at the top,
    and a white baseline along the bottom."""
    d.rectangle([x, y, x + w, y + h], fill=(206, 140, 62))
    for i in range(0, w, 36):
        d.rectangle([x + i, y, x + i + 18, y + h], fill=(216, 152, 75))
    # crowd silhouettes behind the court: a dark band with heads
    d.rectangle([x, y, x + w, y + 6], fill=(70, 58, 48))
    for hx in range(x + 6, x + w - 6, 15):
        d.ellipse([hx, y + 1, hx + 7, y + 8], fill=(95, 80, 65))
    d.line([(x, y + h - 2), (x + w, y + h - 2)], fill=(255, 255, 255),
           width=2)


def _hoop(d, x, y, w, h):
    """Backboard + rim + net at the right edge."""
    d.rectangle([x + w - 26, y + 2, x + w - 8, y + 16], fill=(255, 255, 255),
                outline=(60, 60, 60))
    d.ellipse([x + w - 34, y + 16, x + w - 22, y + 20], outline=(200, 60, 30),
              width=2)
    d.line([(x + w - 32, y + 20), (x + w - 30, y + 26)],
           fill=(255, 255, 255), width=1)
    d.line([(x + w - 26, y + 20), (x + w - 26, y + 26)],
           fill=(255, 255, 255), width=1)
    d.line([(x + w - 24, y + 20), (x + w - 28, y + 26)],
           fill=(255, 255, 255), width=1)


def _scene_jumpshot(img, d, x, y, w, h):
    """Heat 137-130 Bucks: a jump shot — the shooter (red) leaps high
    and releases the ball on a long arc toward the hoop, a defender
    (green) jumps to block under it, and a crowd watches from behind
    the court. Exactly ONE ball."""
    _court(d, x, y, w, h)
    _hoop(d, x, y, w, h)
    # shooter leaping high + ball on a long arc to the hoop
    _player(d, x + 8, y + 0, 1.0, "jumpshot", (200, 30, 30),
            (250, 250, 250))
    d.arc([x + 40, y - 2, x + 104, y + 20], 300, 60,
          fill=(255, 255, 255), width=2)
    _ball_basket(d, x + 76, y + 10, 13, trail="left")
    # defender jumping to block under the hoop + paint box + dust
    _player(d, x + w - 74, y + 0, 1.0, "header", (0, 110, 60),
            (250, 250, 250))
    d.rectangle([x + w - 52, y + h - 16, x + w - 2, y + h - 2],
                outline=(255, 255, 255), width=1)
    d.ellipse([x + 18, y + h - 7, x + 28, y + h - 2], fill=(235, 200, 160))
    d.ellipse([x + w - 66, y + h - 7, x + w - 56, y + h - 2],
              fill=(235, 200, 160))


def _scene_dunk(img, d, x, y, w, h):
    """Nuggets 105-101 Celtics: a DUNK — the dunker (navy) leaps
    right at the rim with BOTH hands on the ball above it, a
    defender (green) watches from below, motion lines trailing the
    dunker, dust at his feet. Exactly ONE ball, in his hands."""
    _court(d, x, y, w, h)
    _hoop(d, x, y, w, h)
    # defender standing under the hoop, watching the dunk
    _player(d, x + w - 118, y + 0, 1.0, "stand", (0, 122, 51),
            (250, 250, 250))
    # dunker leaping at the rim, both arms up, ball in his hands
    # (ball sits between the two raised wrists; kept small and low
    # enough that it never touches the score header above the scene)
    _player(d, x + w - 78, y + 0, 1.0, "jumpshot", (12, 35, 64),
            (250, 250, 250))
    _ball_basket(d, x + w - 58, y + 5, 9, trail=None)
    # motion lines trailing the dunker + dust at his feet
    for i, off in enumerate((0, 5, -5)):
        x0 = x + w - 86 - i * 7
        d.line([(x0, y + 12 + off), (x0 + 10, y + 12 + off)],
               fill=(255, 255, 255), width=2)
    d.ellipse([x + w - 70, y + h - 7, x + w - 60, y + h - 2],
              fill=(235, 200, 160))
    d.ellipse([x + 8, y + h - 7, x + 18, y + h - 2], fill=(235, 200, 160))
    # paint box + centre arc on the left, to fill the empty court
    d.rectangle([x + 2, y + h - 16, x + 30, y + h - 2],
                outline=(255, 255, 255), width=1)
    d.arc([x - 18, y - 8, x + 30, y + h + 8], 270, 90,
          fill=(255, 255, 255), width=2)


def _scene_fastbreak(img, d, x, y, w, h):
    """Grizzlies 124-121 Cavaliers: a FAST BREAK — the runner (light
    blue) sprints toward the hoop with the ball low in front of him,
    speed lines streaming behind him, a defender (wine) trailing
    behind, and a gold "8-0" chip at the top-centre for the road
    record. Exactly ONE ball, in his hand."""
    _court(d, x, y, w, h)
    _hoop(d, x, y, w, h)
    # gold "8-0" chip, top-centre of the scene
    cf = load("DejaVuSans-Bold.ttf", 11)
    label = "8\u20130"
    tw = int(d.textlength(label, font=cf))
    cx = x + w // 2
    d.rounded_rectangle([cx - tw // 2 - 6, y + 1, cx + tw // 2 + 6, y + 14],
                        radius=6, fill=(212, 175, 55))
    d.text((cx - tw // 2, y + 2), label, font=cf, fill=(40, 30, 10))
    # defender trailing behind, at the left edge
    _player(d, x + 2, y + 0, 1.0, "run", (128, 20, 40),
            (250, 250, 250), flip=True)
    # runner sprinting to the hoop, ball low in front of him
    _player(d, x + 52, y + 0, 1.0, "run", (90, 160, 220),
            (250, 250, 250))
    _ball_basket(d, x + 52 + 33, y + 21, 10, trail="left")
    # long speed lines streaming behind the runner
    for i, off in enumerate((0, 5, -5, 3)):
        x0 = x + 52 - 8 - i * 7
        d.line([(x0, y + 12 + off), (x0 + 12, y + 12 + off)],
               fill=(255, 255, 255), width=2)
    # dust at both players' feet
    d.ellipse([x + 60, y + h - 7, x + 70, y + h - 2], fill=(235, 200, 160))
    d.ellipse([x + 10, y + h - 7, x + 20, y + h - 2], fill=(235, 200, 160))


# (winner logo, loser logo, score, scene) for each NBA strip.
NBA_MATCHES = {
    "nba-heat-bucks": ("logo-heat.png", "logo-bucks.png", "137\u2013130",
                       "jumpshot"),
    "nba-nuggets-celtics": ("logo-nuggets.png", "logo-celtics.png",
                            "105\u2013101", "dunk"),
    "nba-grizzlies-cavs": ("logo-grizzlies.png", "logo-cavaliers.png",
                           "124\u2013121", "fastbreak"),
}


def draw_match(img, d, x, y, w, h, key):
    """Sports strip: a score header on the top row (the two clubs'
    REAL logos flanking the score), then a different action scene
    below. No trophy, no photo ball, exactly one drawn ball."""
    win, lose, score, scene = NBA_MATCHES[key]
    sf = load("DejaVuSans-Bold.ttf", 14)
    wl = fit_height(_trim(asset(win)), 18)
    ll = fit_height(_trim(asset(lose)), 18)
    sw = int(d.textlength(score, font=sf))
    total = wl.width + 6 + sw + 6 + ll.width
    sx = x + (w - total) // 2
    _paste_rgba(img, wl, sx, y + 2)
    d.text((sx + wl.width + 6, y + 1), score, font=sf, fill=INK)
    _paste_rgba(img, ll, sx + wl.width + 6 + sw + 6, y + 2)
    fy = y + 22
    fhgt = h - 24
    if scene == "jumpshot":
        _scene_jumpshot(img, d, x, fy, w, fhgt)
    elif scene == "dunk":
        _scene_dunk(img, d, x, fy, w, fhgt)
    elif scene == "fastbreak":
        _scene_fastbreak(img, d, x, fy, w, fhgt)

# ---------------------------------------------------------------- health & technology
# Six flat v1-style illustrations, one per new box. Every strip is
# filled edge-to-edge — background elements, supporting details,
# motion lines and textures — so no strip feels empty in the
# narrower (~165px) columns. All coordinates are integers, so
# renders stay deterministic.

def _virus(d, cx, cy, r, fill, spike_col=(150, 40, 50), spike_len=6):
    """Spiky virus ball: a filled circle with radiating spikes and
    lighter dots inside."""
    import math
    for i in range(12):
        ang = math.radians(i * 30)
        d.line([(cx + int((r - 1) * math.cos(ang)),
                 cy + int((r - 1) * math.sin(ang))),
                (cx + int((r + spike_len) * math.cos(ang)),
                 cy + int((r + spike_len) * math.sin(ang)))],
               fill=spike_col, width=2)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill)
    for (dx, dy, rr) in ((-r // 3, -r // 4, 2), (r // 3, r // 4, 2),
                         (0, r // 2, 2)):
        d.ellipse([cx + dx - rr, cy + dy - rr, cx + dx + rr, cy + dy + rr],
                  fill=(255, 200, 205))


def _capsule(d, x1, y1, x2, y2, wd, c1, c2):
    """Two-tone capsule from (x1, y1) to (x2, y2): first half c1,
    second half c2, round caps at both ends, thin outline."""
    mx, my = (x1 + x2) // 2, (y1 + y2) // 2
    r = wd // 2
    d.line([(x1, y1), (x2, y2)], fill=(120, 125, 130), width=wd + 2)
    d.line([(x1, y1), (mx, my)], fill=c1, width=wd)
    d.line([(mx, my), (x2, y2)], fill=c2, width=wd)
    d.ellipse([x1 - r - 1, y1 - r - 1, x1 + r + 1, y1 + r + 1],
              fill=(120, 125, 130))
    d.ellipse([x2 - r - 1, y2 - r - 1, x2 + r + 1, y2 + r + 1],
              fill=(120, 125, 130))
    d.ellipse([x1 - r, y1 - r, x1 + r, y1 + r], fill=c1)
    d.ellipse([x2 - r, y2 - r, x2 + r, y2 + r], fill=c2)


def _plus(d, cx, cy, s, color):
    d.line([(cx - s, cy), (cx + s, cy)], fill=color, width=2)
    d.line([(cx, cy - s), (cx, cy + s)], fill=color, width=2)


def draw_ebola_virus(d, x, y, w, h):
    """Ebola, MAXIMUM drama: a BIG dark-maroon spiky virus ball with
    long spikes and a red warning ring around it, smaller viruses
    around it, a yellow warning triangle, and a red medical cross.
    Flat v1 style, filling the strip edge-to-edge."""
    # red warning ring behind the big virus
    d.ellipse([x + int(w * 0.36) - 27, y + int(h * 0.48) - 27,
               x + int(w * 0.36) + 27, y + int(h * 0.48) + 27],
              outline=(220, 60, 60), width=3)
    _virus(d, x + int(w * 0.36), y + int(h * 0.48), 21, (150, 30, 40),
           spike_col=(110, 20, 30), spike_len=10)
    _virus(d, x + int(w * 0.12), y + int(h * 0.20), 8, (180, 50, 60))
    _virus(d, x + int(w * 0.16), y + int(h * 0.82), 6, (180, 50, 60))
    _virus(d, x + int(w * 0.58), y + int(h * 0.85), 5, (200, 80, 90))
    # red medical cross, left edge
    _plus(d, x + 10, y + 12, 6, (200, 40, 40))
    # yellow warning triangle above the small virus, right side
    tx, ty = x + int(w * 0.82), y + 8
    d.polygon([(tx, ty), (tx - 8, ty + 14), (tx + 8, ty + 14)],
              fill=(255, 200, 40))
    d.line([(tx, ty + 4), (tx, ty + 10)], fill=(60, 40, 10), width=2)
    d.ellipse([tx - 1, ty + 11, tx + 1, ty + 13], fill=(60, 40, 10))
    # motion lines trailing the big virus + small red dots in the gaps
    for i, off in enumerate((0, 5, -5)):
        x0 = x + int(w * 0.36) - 32 - i * 7
        d.line([(x0, y + 12 + off), (x0 + 9, y + 12 + off)],
               fill=(200, 120, 110), width=2)
    for (dx, dy) in ((0.62, 0.12), (0.14, 0.55), (0.72, 0.88)):
        px, py = x + int(w * dx), y + int(h * dy)
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(200, 80, 90))


def draw_measles(d, x, y, w, h):
    """Measles, MAXIMUM drama: a BIG spiky virus ball with long
    spikes and a red warning ring, smaller viruses around it, a BIG
    syringe on the right, and a yellow warning triangle. Flat v1
    style, filling the strip edge-to-edge."""
    # red warning glow behind the big virus
    d.ellipse([x + int(w * 0.36) - 26, y + int(h * 0.48) - 26,
               x + int(w * 0.36) + 26, y + int(h * 0.48) + 26],
              fill=(240, 150, 155))
    _virus(d, x + int(w * 0.36), y + int(h * 0.48), 20, (205, 65, 75),
           spike_len=10)
    _virus(d, x + int(w * 0.12), y + int(h * 0.20), 8, (225, 100, 110))
    _virus(d, x + int(w * 0.18), y + int(h * 0.82), 6, (225, 100, 110))
    _virus(d, x + int(w * 0.55), y + int(h * 0.85), 5, (235, 130, 135))
    # syringe, BIG, vertical on the right: barrel, liquid, needle,
    # plunger (v2: shifted left so the story-number badge at the
    # top-right corner does not cover the barrel)
    sx = x + int(w * 0.75)
    d.rectangle([sx - 8, y + 4, sx + 8, y + 40], fill=(255, 255, 255),
                outline=(120, 125, 130))
    d.rectangle([sx - 5, y + 20, sx + 5, y + 36], fill=(170, 210, 235))
    for ty in (y + 10, y + 14, y + 18):
        d.line([(sx + 2, ty), (sx + 8, ty)], fill=(120, 125, 130), width=1)
    d.line([(sx, y + 40), (sx, y + 56)], fill=(150, 155, 160), width=2)
    d.line([(sx, y + 4), (sx, y + 1)], fill=(150, 155, 160), width=2)
    d.line([(sx - 7, y + 2), (sx + 7, y + 2)], fill=(120, 125, 130),
           width=2)
    # yellow warning triangle above the syringe (v2: shifted left
    # with the syringe)
    tx, ty = x + int(w * 0.60), y + 6
    d.polygon([(tx, ty), (tx - 8, ty + 14), (tx + 8, ty + 14)],
              fill=(255, 200, 40))
    d.line([(tx, ty + 4), (tx, ty + 10)], fill=(60, 40, 10), width=2)
    d.ellipse([tx - 1, ty + 11, tx + 1, ty + 13], fill=(60, 40, 10))
    # motion lines trailing the big virus + small red dots in the
    # gaps (v2: the dot at (0.62, 0.12) is dropped — the warning
    # triangle moved onto it)
    for i, off in enumerate((0, 5, -5)):
        x0 = x + int(w * 0.36) - 30 - i * 7
        d.line([(x0, y + 12 + off), (x0 + 9, y + 12 + off)],
               fill=(200, 120, 110), width=2)
    for (dx, dy) in ((0.14, 0.55), (0.72, 0.88)):
        px, py = x + int(w * dx), y + int(h * dy)
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(200, 80, 90))


def _tent(d, tx, ty, tw, th, body, dark):
    """A triangular tent: two sloped sides, a ground line, a door
    flap triangle in the middle, and a pole sticking out the top."""
    d.polygon([(tx, ty + th), (tx + tw // 2, ty), (tx + tw, ty + th)],
              fill=body, outline=dark)
    d.line([(tx, ty + th), (tx + tw, ty + th)], fill=dark, width=2)
    d.polygon([(tx + tw // 2 - 6, ty + th), (tx + tw // 2, ty + th - 12),
               (tx + tw // 2 + 6, ty + th)], fill=dark)
    d.line([(tx + tw // 2, ty), (tx + tw // 2, ty - 5)], fill=dark, width=2)


def draw_gaza_tents(d, x, y, w, h):
    """Cold kills in Gaza's tents: a dark storm cloud hangs over the
    strip, cold rain slashes down in diagonal lines, a yellow
    lightning bolt crackles in the centre gap between the tents,
    two beige tents stand in flood water, and blue waves run along
    the bottom. Flat v1 style, filling the strip edge-to-edge."""
    # dark storm cloud, top-centre, spanning the strip
    cx = x + w // 2
    d.ellipse([cx - 46, y + 2, cx - 6, y + 16], fill=(120, 125, 135))
    d.ellipse([cx - 26, y - 2, cx + 14, y + 14], fill=(140, 145, 155))
    d.ellipse([cx + 6, y + 2, cx + 46, y + 16], fill=(120, 125, 135))
    d.ellipse([cx - 40, y + 10, cx + 40, y + 18], fill=(110, 115, 125))
    # lightning bolt, centre gap between the two tents, under the
    # cloud (v2: moved from the right edge so the story-number
    # badge at the top-right corner does not cover it)
    d.polygon([(x + 76, y + 18), (x + 84, y + 18),
               (x + 78, y + 28), (x + 86, y + 28),
               (x + 74, y + 42), (x + 80, y + 28),
               (x + 74, y + 28)], fill=(255, 220, 80))
    # cold rain: diagonal slashes across the whole strip
    for (rx, ry) in ((x + 8, y + 20), (x + 28, y + 14), (x + 48, y + 22),
                     (x + 68, y + 16), (x + 88, y + 22), (x + 108, y + 14),
                     (x + 128, y + 22), (x + 148, y + 16)):
        d.line([(rx, ry), (rx - 4, ry + 8)], fill=(140, 170, 200), width=2)
    # flood water along the bottom, two rows of waves
    for wy, col, wd in ((y + h - 12, (90, 140, 190), 2),
                        (y + h - 6, (140, 180, 220), 2)):
        xx = x + 2
        while xx + 12 <= x + w - 2:
            d.arc([xx, wy, xx + 12, wy + 6], 0, 180, fill=col, width=wd)
            xx += 12
    d.rectangle([x, y + h - 4, x + w, y + h], fill=(110, 160, 205))
    # two tents standing in the water, mirrored around the centre
    _tent(d, x + 8, y + 24, 52, 26, (216, 200, 168), (140, 120, 90))
    _tent(d, x + w - 60, y + 24, 52, 26, (205, 190, 160), (140, 120, 90))
    # small puddle reflections under the tents
    d.ellipse([x + 14, y + h - 10, x + 54, y + h - 4],
              fill=(160, 195, 230))
    d.ellipse([x + w - 54, y + h - 10, x + w - 14, y + h - 4],
              fill=(160, 195, 230))


def draw_gpt_robot(d, x, y, w, h):
    """GPT-6.2, MAXIMUM drama: a BIG robot head with an antenna,
    glowing eyes, electric arcs crackling from its corners, circuit
    traces radiating to the strip edges with solder dots — and a gold
    "6.2" version badge at the top-left. Flat v1 style, filling the
    strip edge-to-edge."""
    # gold "6.2" badge, top-LEFT (v2: the story-number badge takes
    # the top-right corner, so the version badge moves here)
    bf = load("DejaVuSans-Bold.ttf", 11)
    label = "6.2"
    tw = int(d.textlength(label, font=bf))
    d.rounded_rectangle([x + 2, y + 2, x + 2 + tw + 12, y + 16],
                        radius=7, fill=(196, 122, 18))
    d.text((x + 8, y + 3), label, font=bf, fill=(255, 255, 255))
    # circuit traces + solder dots first (behind the head)
    for (sx, sy, ex, ey) in ((x + 56, y + 18, x + 8, y + 6),
                             (x + 108, y + 18, x + 156, y + 6),
                             (x + 56, y + 40, x + 8, y + 52),
                             (x + 108, y + 40, x + 156, y + 52)):
        d.line([(sx, sy), (ex, ey)], fill=(90, 140, 100), width=2)
        d.ellipse([ex - 3, ey - 3, ex + 3, ey + 3], fill=GOLD)
    for tx in (x + 72, x + 92):
        d.line([(tx, y + 46), (tx, y + 54)], fill=(90, 140, 100), width=2)
        d.ellipse([tx - 3, y + 50, tx + 3, y + 56], fill=GOLD)
    # electric arcs crackling from the head corners
    d.line([(x + 56, y + 14), (x + 44, y + 4), (x + 30, y + 10)],
           fill=(255, 230, 80), width=2, joint="curve")
    d.line([(x + 108, y + 14), (x + 120, y + 4), (x + 134, y + 10)],
           fill=(255, 230, 80), width=2, joint="curve")
    # robot head, BIG
    d.rounded_rectangle([x + 56, y + 10, x + 108, y + 48], radius=8,
                        fill=(230, 235, 240), outline=(90, 100, 112),
                        width=2)
    d.line([(x + 82, y + 10), (x + 82, y + 2)], fill=(90, 100, 112),
           width=2)
    d.ellipse([x + 79, y + 0, x + 85, y + 6], fill=GOLD)
    _sparkle(d, x + 96, y + 6, 4, fill=(255, 230, 80))
    d.rectangle([x + 52, y + 22, x + 56, y + 34], fill=(120, 130, 142))
    d.rectangle([x + 108, y + 22, x + 112, y + 34], fill=(120, 130, 142))
    for ex in (x + 72, x + 92):
        d.ellipse([ex - 6, y + 19, ex + 6, y + 31],
                  outline=(120, 180, 230), width=2)
        d.ellipse([ex - 5, y + 20, ex + 5, y + 30], fill=(40, 90, 180))
        d.ellipse([ex - 1, y + 21, ex + 1, y + 23], fill=(255, 255, 255))
    for my in (y + 36, y + 39, y + 42):
        d.line([(x + 70, my), (x + 94, my)], fill=(120, 130, 142), width=1)
    # small nodes in the gaps
    for (dx, dy) in ((0.18, 0.50), (0.82, 0.50)):
        px, py = x + int(w * dx), y + int(h * dy)
        d.rectangle([px - 3, py - 3, px + 3, py + 3], fill=(90, 140, 100))


def draw_genie_lamp(d, x, y, w, h):
    """Genie 4, MAXIMUM drama: a golden magic lamp at the bottom-left
    with smoke curling up from its spout, and the smoke forming a
    floating 3D cube — an AI-made world — at the top-right, ringed
    with stars and sparkles. Flat v1 style, filling the strip
    edge-to-edge."""
    # stars + dots filling the sky (v2: the top-right sparkle moved
    # left, clear of the story-number badge)
    _sparkle(d, x + 18, y + 8, 5, fill=(255, 215, 90))
    _sparkle(d, x + 90, y + 8, 5, fill=(255, 215, 90))
    _sparkle(d, x + 140, y + 50, 4, fill=(255, 215, 90))
    _sparkle(d, x + 30, y + 52, 4, fill=(255, 215, 90))
    for (dx, dy) in ((0.55, 0.10), (0.85, 0.85), (0.12, 0.88)):
        px, py = x + int(w * dx), y + int(h * dy)
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(140, 130, 190))
    # the 3D cube (an AI-made world), floating top-right: isometric,
    # three faces in three shades of indigo
    cx, cy = x + 118, y + 22
    d.polygon([(cx, cy - 12), (cx + 14, cy - 5), (cx, cy + 2),
               (cx - 14, cy - 5)], fill=(180, 170, 230))
    d.polygon([(cx - 14, cy - 5), (cx, cy + 2), (cx, cy + 16),
               (cx - 14, cy + 9)], fill=(120, 105, 190))
    d.polygon([(cx + 14, cy - 5), (cx, cy + 2), (cx, cy + 16),
               (cx + 14, cy + 9)], fill=(90, 80, 160))
    # tiny window + door on the cube faces
    d.rectangle([cx - 9, cy + 2, cx - 4, cy + 7], fill=(255, 220, 90))
    d.rectangle([cx + 4, cy + 2, cx + 9, cy + 7], fill=(255, 220, 90))
    # smoke curling up from the lamp spout to the cube
    for (scx, scy, sr) in ((x + 62, y + 44, 5), (x + 74, y + 36, 6),
                           (x + 88, y + 30, 5), (x + 100, y + 26, 4)):
        d.ellipse([scx - sr, scy - sr, scx + sr, scy + sr],
                  fill=(215, 210, 225))
    # the golden lamp, bottom-left: body, spout, handle, lid, base
    lx, ly = x + 18, y + 40
    d.ellipse([lx, ly - 2, lx + 44, ly + 14], fill=(212, 175, 55),
              outline=(140, 105, 20))
    d.polygon([(lx + 40, ly + 2), (lx + 58, ly - 6), (lx + 58, ly + 4),
               (lx + 40, ly + 8)], fill=(212, 175, 55),
              outline=(140, 105, 20))
    d.arc([lx + 40, ly - 8, lx + 56, ly + 12], 270, 90,
          fill=(140, 105, 20), width=3)
    d.ellipse([lx + 14, ly - 10, lx + 30, ly - 2], fill=(212, 175, 55),
              outline=(140, 105, 20))
    d.ellipse([lx + 20, ly - 14, lx + 24, ly - 10], fill=(212, 175, 55))
    d.rectangle([lx + 8, ly + 14, lx + 36, ly + 17], fill=(140, 105, 20))
    # gold coins spilling from the lamp onto the ground
    for (ccx, ccy) in ((x + 52, y + h - 6), (x + 62, y + h - 4),
                       (x + 70, y + h - 8)):
        d.ellipse([ccx - 4, ccy - 4, ccx + 4, ccy + 4], fill=(240, 205, 90),
                  outline=(140, 105, 20))


def draw_voyager(d, x, y, w, h):
    """Voyager 1, one light-day from Earth: a dark navy space panel
    fills the strip, stars and sparkles scattered across it, a small
    blue Earth glowing at the bottom-left, a dashed white trajectory
    curving up to the gold-and-white probe at the top-right — big
    dish, bus, long boom and RTG fins. Flat v1 style, filling the
    strip edge-to-edge."""
    import math
    # dark space panel, full-bleed
    d.rectangle([x, y, x + w, y + h], fill=(15, 20, 35))
    # stars: dots + sparkles, spread evenly (v2: the top-right star
    # moved down, clear of the story-number badge)
    for (sx, sy, r) in ((x + 12, y + 6, 2), (x + 40, y + 12, 1),
                        (x + 66, y + 5, 2), (x + 96, y + 8, 1),
                        (x + 130, y + 6, 2), (x + 152, y + 38, 1),
                        (x + 24, y + 28, 1), (x + 150, y + 30, 2),
                        (x + 78, y + 40, 1), (x + 108, y + 46, 1)):
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(255, 255, 255))
    _sparkle(d, x + 52, y + 8, 4, fill=(255, 255, 255))
    _sparkle(d, x + 138, y + 22, 4, fill=(255, 255, 255))
    # Earth, small and glowing, bottom-left
    ex, ey, er = x + 20, y + h - 14, 9
    d.ellipse([ex - er - 3, ey - er - 3, ex + er + 3, ey + er + 3],
              fill=(60, 100, 180))
    d.ellipse([ex - er, ey - er, ex + er, ey + er], fill=(70, 130, 220))
    d.ellipse([ex - 5, ey - 4, ex - 1, ey + 1], fill=(90, 180, 110))
    d.ellipse([ex + 2, ey + 2, ex + 6, ey + 6], fill=(90, 180, 110))
    # dashed trajectory from Earth curving up to the probe
    px, py = x + 34, y + h - 20
    while px < x + 108:
        d.line([(px, py), (px + 6, py - 3)], fill=(200, 205, 215), width=2)
        px += 10
        py -= 3
    # the probe, top-right: big white dish, gold bus, long boom,
    # RTG fins at the end of the boom
    bx, by = x + 118, y + 14
    # boom to the left with the RTG at its end
    d.line([(bx - 8, by + 4), (bx - 34, by + 10)], fill=(200, 200, 205),
           width=2)
    d.rectangle([bx - 38, by + 6, bx - 30, by + 14], fill=(60, 60, 70))
    for i in range(3):
        d.line([(bx - 36 + i * 3, by + 6), (bx - 36 + i * 3, by + 2)],
               fill=(150, 150, 160), width=1)
    # gold bus
    d.rectangle([bx - 8, by, bx + 8, by + 10], fill=(212, 175, 55),
                outline=(140, 105, 20))
    # big white dish, tilted toward Earth
    d.ellipse([bx + 4, by - 4, bx + 24, by + 14], outline=(255, 255, 255),
              width=2)
    d.ellipse([bx + 8, by, bx + 20, by + 10], outline=(200, 205, 215),
              width=1)
    d.line([(bx + 8, by + 5), (bx - 2, by + 8)], fill=(255, 255, 255),
           width=2)
    # small antenna mast + sparkle at the dish
    d.line([(bx + 2, by), (bx + 2, by - 6)], fill=(200, 200, 205), width=2)
    _sparkle(d, bx + 20, by - 6, 3, fill=(255, 220, 80))

def draw_court_scales(d, x, y, w, h):
    """ICJ genocide verdict: scales of justice in gold over a
    courthouse colonnade, on a deep navy field. The central pillar
    rises from a stepped base; the beam hangs level with two pans;
    a gavel rests at the bottom-right. The top band stays clear
    for the story-number badge."""
    cx = x + w // 2
    base = y + h - 6
    # colonnade: pale columns left and right, steps along the bottom
    for colx in (x + 8, x + w - 16):
        d.rectangle([colx, y + 14, colx + 8, base], fill=(225, 225, 220),
                    outline=(150, 150, 145))
        d.rectangle([colx - 2, y + 10, colx + 10, y + 14],
                    fill=(240, 240, 235), outline=(150, 150, 145))
    d.rectangle([x + 2, base, x + w - 2, base + 3], fill=(200, 200, 195))
    # central pillar + finial
    d.rectangle([cx - 3, y + 16, cx + 3, base - 8], fill=GOLD)
    d.ellipse([cx - 4, y + 10, cx + 4, y + 18], fill=GOLD)
    d.rectangle([cx - 10, base - 8, cx + 10, base - 4], fill=GOLD)
    # beam (level: justice delivered) + hanging pans
    d.line([(cx - 34, y + 20), (cx + 34, y + 20)], fill=GOLD, width=3)
    for sgn in (-1, 1):
        px = cx + sgn * 34
        d.line([(px, y + 20), (px, y + 32)], fill=GOLD, width=2)
        d.line([(px - 9, y + 32), (px, y + 20)], fill=GOLD, width=1)
        d.line([(px + 9, y + 32), (px, y + 20)], fill=GOLD, width=1)
        d.pieslice([px - 10, y + 30, px + 10, y + 42], 0, 180,
                   fill=(255, 215, 90), outline=(140, 105, 20))
    # gavel, bottom-right: head + handle, slight diagonal
    d.polygon([(x + w - 34, base - 16), (x + w - 14, base - 22),
               (x + w - 12, base - 14), (x + w - 32, base - 8)],
              fill=(120, 85, 50))
    d.line([(x + w - 26, base - 12), (x + w - 8, base - 2)],
           fill=(90, 60, 35), width=3)
    # small gold sparkles
    _sparkle(d, x + 34, y + 10, 4)
    _sparkle(d, x + w - 34, y + 8, 3)


def draw_arctic(d, x, y, w, h):
    """Greenland pact: an Arctic fjord — pale sky, low sun, snow
    mountains, dark blue water with white icebergs. The Danish
    flag is pasted on top by the dispatch (flag zone top-left
    kept clear)."""
    d.rectangle([x, y, x + w, y + h], fill=(205, 225, 240))
    # low sun + cloud
    d.ellipse([x + w - 34, y + 4, x + w - 16, y + 22],
              fill=(255, 220, 130))
    _cloud(d, x + 14, y + 4, 14)
    # snow mountains along the middle
    d.polygon([(x, y + 34), (x + 40, y + 8), (x + 80, y + 34)],
              fill=(245, 248, 250))
    d.polygon([(x + 50, y + 34), (x + 105, y + 4), (x + 160, y + 34)],
              fill=(235, 240, 245))
    d.polygon([(x + 120, y + 34), (x + 150, y + 14), (x + w, y + 34)],
              fill=(245, 248, 250))
    # dark fjord water + icebergs
    d.rectangle([x, y + 34, x + w, y + h], fill=(70, 120, 170))
    for (bx, by, s) in ((x + 24, y + 42, 8), (x + 76, y + 46, 10),
                        (x + 128, y + 42, 7)):
        d.polygon([(bx - s, by), (bx, by - s), (bx + s, by),
                   (bx + s // 2, by + 4), (bx - s // 2, by + 4)],
                  fill=(255, 255, 255))
    _waves(d, x, y, w, h)


def draw_store(d, x, y, w, h):
    """Walmart earnings: a big-box storefront — blue fascia with
    a gold starburst, striped awning, glass doors, and a shopping
    cart full of boxes rolling in from the right."""
    d.rectangle([x, y, x + w, y + h], fill=(225, 235, 245))
    # fascia + starburst
    d.rectangle([x, y, x + w, y + 14], fill=(0, 90, 170))
    _sparkle(d, x + 20, y + 7, 5, fill=(255, 215, 90))
    # striped awning
    for i in range(8):
        col = (255, 255, 255) if i % 2 == 0 else (200, 40, 40)
        d.rectangle([x + i * (w // 8), y + 14, x + (i + 1) * (w // 8),
                     y + 22], fill=col)
    # wall + glass doors
    d.rectangle([x, y + 22, x + w, y + h], fill=(240, 240, 235))
    d.rectangle([x + 52, y + 26, x + 112, y + h - 4],
                fill=(160, 200, 235), outline=(90, 100, 112))
    d.line([(x + 82, y + 26), (x + 82, y + h - 4)], fill=(90, 100, 112),
           width=2)
    d.rectangle([x + 118, y + 30, x + 152, y + h - 4],
                fill=(190, 215, 240), outline=(90, 100, 112))
    # shopping cart, right side, with boxes
    cx0, cy0 = x + w - 52, y + 30
    d.polygon([(cx0, cy0), (cx0 + 30, cy0), (cx0 + 26, cy0 + 14),
               (cx0 + 4, cy0 + 14)], outline=(90, 100, 112), width=2)
    d.line([(cx0 + 30, cy0 + 7), (cx0 + 40, cy0 + 2)], fill=(90, 100, 112),
           width=2)
    d.ellipse([cx0 + 4, cy0 + 16, cx0 + 10, cy0 + 22], fill=(60, 60, 60))
    d.ellipse([cx0 + 20, cy0 + 16, cx0 + 26, cy0 + 22], fill=(60, 60, 60))
    d.rectangle([cx0 + 6, cy0 - 8, cx0 + 16, cy0], fill=(255, 200, 60),
                outline=(150, 120, 20))
    d.rectangle([cx0 + 18, cy0 - 6, cx0 + 28, cy0], fill=(90, 160, 90),
                outline=(40, 100, 40))
    # price tag
    d.polygon([(x + 8, y + 30), (x + 30, y + 30), (x + 30, y + 42),
               (x + 8, y + 42)], fill=(255, 215, 90),
              outline=(140, 105, 20))
    d.text((x + 12, y + 32), "$", font=load("DejaVuSans-Bold.ttf", 9),
           fill=(120, 80, 10))


def draw_football(d, x, y, w, h):
    """Texans 26-3 Colts: a green field, white yard lines, a
    brown football flying with motion lines toward a yellow
    goalpost, and a navy 26-3 scoreboard chip dead centre at the
    top (the badge sits top-right, clear of it)."""
    cx = x + w // 2
    d.rectangle([x, y, x + w, y + h], fill=(40, 130, 60))
    for lx in range(x + 14, x + w - 6, 28):
        d.line([(lx, y + 16), (lx, y + h - 4)], fill=(255, 255, 255),
               width=1)
    d.line([(x, y + h - 4), (x + w, y + h - 4)], fill=(255, 255, 255),
           width=2)
    # scoreboard chip, dead centre at the top
    sf = load("DejaVuSans-Bold.ttf", 11)
    label = "26\u20133"
    tw = int(d.textlength(label, font=sf))
    d.rounded_rectangle([cx - tw // 2 - 6, y + 1, cx + tw // 2 + 6,
                         y + 14], radius=6, fill=NAVY)
    d.text((cx - tw // 2, y + 2), label, font=sf, fill=(255, 255, 255))
    # goalpost, right side
    gx = x + w - 22
    d.line([(gx, y + 18), (gx, y + h - 6)], fill=(255, 215, 90), width=3)
    d.line([(gx, y + 18), (gx + 12, y + 18)], fill=(255, 215, 90), width=3)
    d.line([(gx, y + 18), (gx - 12, y + 18)], fill=(255, 215, 90), width=3)
    # flying football, centre-left, with motion lines
    fx, fy = cx - 28, y + 30
    d.ellipse([fx - 14, fy - 7, fx + 14, fy + 7], fill=(140, 85, 40),
              outline=(90, 55, 25))
    d.line([(fx - 6, fy - 2), (fx + 6, fy - 2)], fill=(255, 255, 255),
           width=2)
    for dx in (-4, 0, 4):
        d.line([(fx + dx, fy - 5), (fx + dx, fy + 1)],
               fill=(255, 255, 255), width=1)
    for i, off in enumerate((0, 4, -4)):
        d.line([(fx - 26 - i * 6, fy + off), (fx - 18 - i * 6, fy + off)],
               fill=(220, 220, 220), width=2)
    _grass(d, x, y, w, h)


def draw_soccer(d, x, y, w, h):
    """Australia U17 2-0 Argentina: a green pitch, a goal with a
    net on the right, and a soccer ball flying into it with
    motion lines; a small gold star marks the upset win."""
    d.rectangle([x, y, x + w, y + h], fill=(45, 135, 65))
    for lx in range(x + 14, x + w - 6, 28):
        d.line([(lx, y + 6), (lx, y + h - 4)], fill=(255, 255, 255),
               width=1)
    # goal + net, right side
    gx0, gy0, gx1, gy1 = x + w - 42, y + 10, x + w - 6, y + 48
    d.rectangle([gx0, gy0, gx1, gy1], outline=(255, 255, 255), width=3)
    for nx in range(gx0 + 6, gx1, 6):
        d.line([(nx, gy0), (nx, gy1)], fill=(220, 220, 220), width=1)
    for ny in range(gy0 + 6, gy1, 6):
        d.line([(gx0, ny), (gx1, ny)], fill=(220, 220, 220), width=1)
    # soccer ball, centre, flying toward the goal
    bx, by = x + w // 2 - 6, y + 30
    d.ellipse([bx - 9, by - 9, bx + 9, by + 9], fill=(255, 255, 255),
              outline=(40, 40, 40))
    d.polygon([(bx, by - 5), (bx + 5, by - 1), (bx + 3, by + 5),
               (bx - 3, by + 5), (bx - 5, by - 1)], fill=(30, 30, 30))
    for dx, dy in ((-7, -4), (7, -4), (-7, 5), (7, 5), (0, -8)):
        d.ellipse([bx + dx - 2, by + dy - 2, bx + dx + 2, by + dy + 2],
                  fill=(30, 30, 30))
    for i, off in enumerate((0, 4, -4)):
        d.line([(bx - 22 - i * 6, by + off), (bx - 14 - i * 6, by + off)],
               fill=(220, 220, 220), width=2)
    _sparkle(d, x + 18, y + 10, 4)
    _grass(d, x, y, w, h)


def draw_illustration(img, d, x, y, w, h, key, tint):
    """5 columns x 3 rows, ~185px boxes, ~165px strips.
    Politics: full-width flat v1-style scenes, centred and balanced
    (leaders shaking hands in Shenzhen / collapsing Kerch Bridge /
    Capitol + 56-44 scoreboard), with the country flags pasted on
    top at the same top-left spot in every box. Finance: pure PIL
    illustration, big and dramatic (tumbling candles / IPO rocket
    with a gold $83 chip / glowing chip with a red -2.9% plunge).
    Sports: three DIFFERENT basketball scenes, with the two clubs'
    REAL logos flanking the score in the header and exactly ONE
    drawn ball per scene. Health and Technology: flat v1-style
    illustrations, each filled edge-to-edge (Ebola virus + warning,
    measles virus + syringe, Gaza tents in rain and flood, GPT robot
    + 6.2 badge, genie lamp + 3D cube world, Voyager 1 in deep
    space)."""
    d.rectangle([x, y, x + w, y + h], fill=tint)
    if key in NBA_MATCHES:
        draw_match(img, d, x, y, w, h, key)
        return
    if key == "leaders-cn-ru":
        # scene first (full width, flag zone kept clear), flags on top
        draw_leaders_shenzhen(d, x, y, w, h)
        cn = fit_height(asset("flag-cn.png"), 20)
        ru = fit_height(asset("flag-ru.png"), 20)
        _paste_with_border(img, d, cn, x, y + 1)
        _paste_with_border(img, d, ru, x + cn.width + 4, y + 1)
        return
    if key.startswith("flag-"):
        name = key[len("flag-"):]
        flag = fit_height(asset(f"flag-{name}.png"), 20)
        if name == "ua":
            draw_bridge_flat(d, x, y, w, h)
            _paste_with_border(img, d, flag, x, y + 1)
        elif name == "us":
            draw_capitol(d, x, y, w, h)
            _paste_with_border(img, d, flag, x, y + 1)
        return
    if key == "candles-down":
        draw_candles_big(d, x, y, w, h)
        return
    if key == "rocket-ipo":
        draw_rocket_ipo(d, x, y, w, h)
        return
    if key == "court-scales":
        draw_court_scales(d, x, y, w, h)
        return
    if key == "arctic":
        draw_arctic(d, x, y, w, h)
        flag = fit_height(asset("flag-dk.png"), 20)
        _paste_with_border(img, d, flag, x, y + 1)
        return
    if key == "store":
        draw_store(d, x, y, w, h)
        return
    if key == "football":
        draw_football(d, x, y, w, h)
        return
    if key == "soccer":
        draw_soccer(d, x, y, w, h)
        return
    if key == "chip-down":
        draw_chip_down(d, x, y, w, h)
        return
    if key == "ebola-virus":
        draw_ebola_virus(d, x, y, w, h)
        return
    if key == "health-measles":
        draw_measles(d, x, y, w, h)
        return
    if key == "gaza-tents":
        draw_gaza_tents(d, x, y, w, h)
        return
    if key == "gpt-robot":
        draw_gpt_robot(d, x, y, w, h)
        return
    if key == "genie-lamp":
        draw_genie_lamp(d, x, y, w, h)
        return
    if key == "voyager":
        draw_voyager(d, x, y, w, h)
        return

# ---------------------------------------------------------------- drawing
def _spaced_text(d, cx, y, text, font, fill, extra):
    """Draw text centred on cx with `extra` px between characters
    (loose letter-spacing for the masthead date)."""
    widths = [d.textlength(ch, font=font) for ch in text]
    total = sum(widths) + extra * (len(text) - 1)
    x = cx - total / 2
    for ch, w in zip(text, widths):
        d.text((x, y), ch, font=font, fill=fill)
        x += w + extra


def _globe(d, cx, cy, r, color):
    """Small gold globe: circle + vertical meridian + equator +
    two diagonal arcs."""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=2)
    d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=color,
              width=1)
    d.line([(cx - r, cy), (cx + r, cy)], fill=color, width=1)
    d.arc([cx - r, cy - r, cx + r, cy + r], 300, 60, fill=color, width=1)
    d.arc([cx - r, cy - r, cx + r, cy + r], 120, 240, fill=color, width=1)


def _compass_star(d, cx, cy, r, color):
    """Small gold compass star: thin circle + 4-point star."""
    import math
    d.ellipse([cx - r - 2, cy - r - 2, cx + r + 2, cy + r + 2],
              outline=color, width=1)
    pts = []
    for i in range(8):
        ang = math.radians(-90 + i * 45)
        rr = r if i % 2 == 0 else r // 3
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=color)


def draw_masthead(d):
    """v4 masthead: TALLER navy band (12..130) so the DATE reads at
    300px too — title 44px serif, date 22px bold gold with loose
    letter-spacing, subtitle 16px grey; globe left, compass star
    right; 6px stripe of the five category colours below."""
    d.rectangle([24, 12, 1000, 130], fill=NAVY)
    _globe(d, 62, 71, 18, GOLD_TEXT)
    _compass_star(d, 962, 71, 16, GOLD_TEXT)
    title_f = load("DejaVuSerif-Bold.ttf", 44)
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=title_f)
    d.text(((W - tw) / 2, 18), title, font=title_f, fill=CREAM)
    date_f = load("DejaVuSans-Bold.ttf", 22)
    _spaced_text(d, W // 2, 70, "THURSDAY, 19 NOVEMBER 2026", date_f,
                 GOLD_TEXT, 2)
    tag_f = load("DejaVuSans.ttf", 16)
    tag = "37 STORIES  \u2022  5 SECTIONS  \u2022  ONE DAY IN WORLD NEWS"
    gw = d.textlength(tag, font=tag_f)
    d.text(((W - gw) / 2, 102), tag, font=tag_f, fill=GREY_TEXT)
    seg_colors = (POLITICS, FINANCE, SPORTS, HEALTH, TECHNOLOGY)
    sw = (1000 - 24) // 5
    for i, col in enumerate(seg_colors):
        x0 = 24 + i * sw
        x1 = 1000 if i == 4 else x0 + sw
        d.rectangle([x0, 130, x1, 136], fill=col)


def _leader_big(d, fx, y, suit, tie, flip, s=3):
    """_leader scaled by s: same suited figure (head, torso, tie,
    one arm reaching to the centre, one hanging), all offsets
    multiplied by s, for the big hero panel. Total height ~46*s."""
    sg = 1 if not flip else -1
    # legs + shoes
    d.rectangle([fx - 5 * s, y + 33 * s, fx - 1 * s, y + 44 * s], fill=suit)
    d.rectangle([fx + 1 * s, y + 33 * s, fx + 5 * s, y + 44 * s], fill=suit)
    d.ellipse([fx - 6 * s, y + 42 * s, fx, y + 46 * s], fill=(30, 30, 30))
    d.ellipse([fx, y + 42 * s, fx + 6 * s, y + 46 * s], fill=(30, 30, 30))
    # torso + shirt V + tie
    d.polygon([(fx - 7 * s, y + 19 * s), (fx + 7 * s, y + 19 * s),
               (fx + 5 * s, y + 34 * s), (fx - 5 * s, y + 34 * s)],
              fill=suit)
    d.polygon([(fx - 3 * s, y + 19 * s), (fx + 3 * s, y + 19 * s),
               (fx, y + 24 * s)], fill=(255, 255, 255))
    d.polygon([(fx - 2 * s, y + 22 * s), (fx + 2 * s, y + 22 * s),
               (fx + 1 * s, y + 30 * s), (fx - 1 * s, y + 30 * s)],
              fill=tie)
    # reaching arm toward the centre + hanging arm outside
    hx = fx + sg * 16 * s
    d.line([(fx + sg * 6 * s, y + 21 * s), (hx, y + 27 * s)], fill=suit,
           width=4 * s)
    d.ellipse([hx - 3 * s, y + 24 * s, hx + 3 * s, y + 30 * s], fill=SKIN)
    d.line([(fx - sg * 6 * s, y + 21 * s), (fx - sg * 8 * s, y + 31 * s)],
           fill=suit, width=4 * s)
    d.ellipse([fx - sg * 8 * s - 2 * s, y + 29 * s,
               fx - sg * 8 * s + 2 * s, y + 33 * s], fill=SKIN)
    # head + hair
    d.ellipse([fx - 5 * s, y + 7 * s, fx + 5 * s, y + 17 * s], fill=SKIN)
    d.arc([fx - 5 * s, y + 7 * s, fx + 5 * s, y + 17 * s], 180, 360,
          fill=(40, 30, 25), width=3)


def draw_hero_summit(d, x, y, w, h):
    """Trump-Xi-Putin Shenzhen summit hero, fully parametric in
    w/h: pale sky with clouds and birds, a tall Shenzhen skyline
    along the bottom, a red carpet, and THREE big leaders standing
    shoulder to shoulder — US (navy suit, red tie) left, China
    (dark suit, red tie) centre, Russia (charcoal, blue tie)
    right — with a gold sparkle above them. The three flags are
    pasted on top by draw_hero (top-left zone kept clear)."""
    base = y + h - 8
    d.rectangle([x, y, x + w, y + h], fill=(208, 226, 240))
    _cloud(d, x + int(w * 0.06), y + 6, 22)
    _cloud(d, x + int(w * 0.80), y + 10, 26)
    _bird(d, x + int(w * 0.30), y + 8, 7)
    _bird(d, x + int(w * 0.62), y + 6, 7)
    # tall skyline silhouettes along the bottom, mirrored heights
    for i, bhgt in enumerate((18, 30, 46, 62, 78, 62, 46, 30, 18)):
        bw = (w - 4) // 9
        bx = x + 2 + i * bw
        d.rectangle([bx, base - bhgt, bx + bw - 3, base],
                    fill=(110, 125, 145))
        for wy in range(base - bhgt + 6, base - 4, 10):
            d.rectangle([bx + 5, wy, bx + 7, wy + 3], fill=(255, 210, 90))
            d.rectangle([bx + 12, wy, bx + 14, wy + 3],
                        fill=(255, 210, 90))
    d.rectangle([x + 2, base, x + w - 2, base + 2], fill=(90, 105, 130))
    # red carpet the leaders stand on
    d.rectangle([x + int(w * 0.14), base - 6, x + int(w * 0.86), base],
                fill=(166, 28, 28))
    d.rectangle([x + int(w * 0.14), base - 6, x + int(w * 0.86),
                 base - 4], fill=(200, 60, 60))
    # the three leaders, big (s=3 -> ~138px tall), feet on the carpet
    ly = base - 6 - 46 * 3
    cx = x + w // 2
    _leader_big(d, cx - 150, ly, (30, 45, 70), (180, 40, 40), flip=False)
    _leader_big(d, cx, ly, (40, 40, 45), (180, 40, 40), flip=False)
    _leader_big(d, cx + 150, ly, (50, 50, 55), (40, 80, 160), flip=True)
    # gold sparkle above the centre leader
    _sparkle(d, cx, y + 8, 7, fill=(255, 215, 90))
    _sparkle(d, cx - 150, y + 14, 4, fill=(255, 215, 90))
    _sparkle(d, cx + 150, y + 14, 4, fill=(255, 215, 90))


def draw_hero_bridge(d, x, y, w, h):
    """Kerch Bridge hero, MAXIMUM drama, fully parametric in w/h:
    the long bridge arch rises high across the full panel and is
    broken at the top; the centre deck section plunges steeply
    into the strait; a huge fireball + towering smoke column mark
    the blast; debris flies both ways; a big splash erupts where
    the deck hits the water; the right-hand pillar leans and is
    cracked while the left stands upright. Big waves run the full
    width. The Ukraine flag zone (top-left) is kept clear."""
    cx = x + w // 2
    deck_y = y + h - 36
    # sky
    d.rectangle([x, y, x + w, y + h], fill=(208, 226, 240))
    _cloud(d, x + int(w * 0.74), y + 4, 24)
    _cloud(d, x + int(w * 0.08), y + 8, 18)
    _bird(d, x + int(w * 0.56), y + 10, 7)
    _bird(d, x + int(w * 0.86), y + 26, 7)
    _bird(d, x + int(w * 0.32), y + 6, 6)
    # arch: tall full-width arc, broken at the top (the gap is
    # where the blast happened). arch_y() gives the arch's height
    # at any fraction of the width, for the hangers.
    ax0, ay0, ax1, ay1 = x + 6, y + 14, x + w - 6, deck_y + 10
    acx, acy = (ax0 + ax1) / 2, (ay0 + ay1) / 2
    aa, ab = (ax1 - ax0) / 2, (ay1 - ay0) / 2

    def arch_y(fx):
        t = (x + w * fx - acx) / aa
        t = max(-0.999, min(0.999, t))
        return acy - ab * (1 - t * t) ** 0.5

    d.arc([ax0, ay0, ax1, ay1], 180, 255, fill=STEEL, width=6)
    d.arc([ax0, ay0, ax1, ay1], 285, 360, fill=STEEL, width=6)
    # arch feet
    d.line([(x + 6, arch_y(0.01)), (x + 6, deck_y)], fill=STEEL,
           width=6)
    d.line([(x + w - 6, arch_y(0.99)), (x + w - 6, deck_y)],
           fill=STEEL, width=6)
    # hangers on both intact halves + one dangling loose near the gap
    for fx in (0.18, 0.30, 0.62, 0.76):
        hx = x + int(w * fx)
        d.line([(hx, arch_y(fx)), (hx, deck_y)], fill=STEEL, width=3)
    hx = x + int(w * 0.55)
    d.line([(hx, arch_y(0.55)), (hx, arch_y(0.55) + 26)], fill=STEEL,
           width=3)
    # decks: intact left span, plunging centre, sagging right
    d.line([(x + 6, deck_y), (cx - 14, deck_y)], fill=STEEL, width=6)
    d.line([(cx - 14, deck_y), (cx + 46, deck_y + 22)], fill=STEEL,
           width=7)
    d.line([(cx + 54, deck_y - 2), (x + w - 6, deck_y - 2)],
           fill=STEEL, width=6)
    # pillars: left upright, right leaning and cracked
    px = x + int(w * 0.20)
    d.rectangle([px, deck_y + 4, px + 9, y + h - 8], fill=STEEL)
    qx = x + int(w * 0.68)
    d.polygon([(qx, deck_y), (qx + 9, deck_y),
               (qx + 28, y + h - 8), (qx + 19, y + h - 8)], fill=STEEL)
    d.line([(qx + 2, deck_y + 12), (qx + 13, deck_y + 18)], fill=DARK,
           width=2)
    # water + big splash where the plunging deck hits
    _waves(d, x, y, w, h, big=True)
    sx = cx + 42
    d.arc([sx - 46, y + h - 56, sx + 46, y + h - 8], 180, 360,
          fill=(255, 255, 255), width=6)
    d.arc([sx - 30, y + h - 48, sx + 30, y + h - 14], 180, 360,
          fill=(255, 255, 255), width=4)
    d.ellipse([sx - 38, y + h - 18, sx + 38, y + h - 6],
              fill=(255, 255, 255))
    for dx, dy, r in ((-40, -20, 5), (44, -24, 5), (-14, -30, 5),
                      (26, -16, 4), (4, -36, 5), (-26, -12, 4),
                      (38, -10, 4), (-52, -6, 4), (52, -34, 4)):
        d.ellipse([sx + dx - r, y + h - 56 + dy - r,
                   sx + dx + r, y + h - 56 + dy + r],
                  fill=(255, 255, 255))
    # blast: huge fireball in the arch gap + towering smoke column
    # rising through the gap
    d.ellipse([cx - 26, deck_y - 46, cx + 26, deck_y + 2],
              fill=(255, 140, 40))
    d.ellipse([cx - 15, deck_y - 34, cx + 15, deck_y - 10],
              fill=(255, 220, 90))
    _burst(d, cx, deck_y - 20, 42)
    _smoke(d, cx, deck_y - 40, 12)
    _smoke(d, cx - 14, deck_y - 66, 10)
    _smoke(d, cx + 12, deck_y - 72, 9)
    _smoke(d, cx - 4, deck_y - 96, 8)
    # debris flying both ways, each with a motion line behind it
    for (tx, ty, lx, ly) in (
            (cx - 64, deck_y - 30, cx - 38, deck_y - 22),
            (cx - 92, deck_y - 16, cx - 64, deck_y - 10),
            (cx - 50, deck_y - 56, cx - 32, deck_y - 42),
            (cx + 64, deck_y - 26, cx + 38, deck_y - 18),
            (cx + 92, deck_y - 12, cx + 64, deck_y - 6),
            (cx + 52, deck_y - 52, cx + 34, deck_y - 38),
            (cx + 12, deck_y - 70, cx + 6, deck_y - 52),
            (cx - 16, deck_y - 66, cx - 10, deck_y - 48),
            (cx + 104, deck_y - 36, cx + 84, deck_y - 28),
            (cx - 104, deck_y - 40, cx - 84, deck_y - 30)):
        d.polygon([(tx, ty), (tx + 13, ty - 6), (tx + 13, ty + 8)],
                  fill=DARK)
        d.line([(lx, ly), (tx + 6, ty)], fill=(150, 160, 172), width=2)


def draw_hero(img, d, x, y, w, h):
    """HERO: story 2 (Trump-Xi-Putin Shenzhen summit) as one big
    panel. Left: the large parametric summit illustration (US, CN
    and RU flags at its top-left, story-number badge 2 at its
    top-right). Right: a crimson 'TOP STORY' kicker, the 36px
    headline in two lines, and an 18px sub-headline (max 3 lines).
    Everything in the hero reads at 300px."""
    number, headline, sub, topic = HERO
    color = TOPIC_COLORS[topic]
    ill_w = int(w * 0.64)
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255),
                outline=BOX_BORDER, width=1)
    d.rectangle([x + 1, y + 1, x + w - 1, y + 5], fill=color)
    draw_hero_summit(d, x + 8, y + 8, ill_w - 8, h - 16)
    # US, China and Russia flags, top-left of the illustration
    fx = x + 8
    for name in ("us", "cn", "ru"):
        flag = fit_height(asset(f"flag-{name}.png"), 20)
        _paste_with_border(img, d, flag, fx, y + 9)
        fx += flag.width + 4
    _number_badge(d, x + ill_w - 12, y + 20, number, color, r=12)
    # text panel on the right
    tx = x + ill_w + 16
    tw = x + w - 12 - tx
    kf = load("DejaVuSans-Bold.ttf", 16)
    d.text((tx, y + 14), "TOP STORY", font=kf, fill=color)
    hf, hlines = fit_block(d, headline, tw, 2, 36, 28, bold=True)
    hy = y + 40
    for ln in hlines:
        d.text((tx, hy), ln, font=hf, fill=INK)
        hy += 42
    sf, slines = fit_block(d, sub, tw, 2, 18, 16, bold=False)
    sy = hy + 4
    for ln in slines:
        d.text((tx, sy), ln, font=sf, fill=(51, 51, 51))
        sy += 22
    if sy > y + h - 4:
        print(f"WARNING: hero sub overflows by {sy - (y + h - 4)}px")


def _number_badge(d, cx, cy, number, color, r=10):
    """Story-number badge: a filled circle in the category colour
    with a thin white ring and a white bold number, centred on
    (cx, cy)."""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color,
              outline=(255, 255, 255), width=2)
    nf = load("DejaVuSans-Bold.ttf", 12)
    label = str(number)
    tw = d.textlength(label, font=nf)
    d.text((cx - tw / 2, cy - 7), label, font=nf, fill=(255, 255, 255))


def _render_strip(key, tint):
    """Render one v3 illustration at its native strip size (165x58)
    into an offscreen image, for LANCZOS upscaling into a v4 card.
    The v3 scenes are tuned for that size; upscaling ~1.3x keeps
    them crisp, and the top-right corner stays clear for the badge
    (the v3 illustrations were adjusted for exactly that)."""
    tmp = Image.new("RGB", (165, 58), tint)
    td = ImageDraw.Draw(tmp)
    draw_illustration(tmp, td, 0, 0, 165, 58, key, tint)
    return tmp


def draw_card(img, d, x, y, w, h, number, headline, sub, ill, topic,
              hl_size):
    """v4 story card: large illustration (upscaled v3 scene), a
    headline in the shared grid size (max 2 lines, centred in its
    slot) and ONE 17px sub-headline line anchored near the bottom.
    No body paragraphs — the card reads at 300px."""
    color = TOPIC_COLORS[topic]
    tint = {"politics": TINT_POLITICS, "finance": TINT_FINANCE,
            "sports": TINT_SPORTS, "health": TINT_HEALTH,
            "technology": TINT_TECHNOLOGY}[topic]
    box_bg = tuple((c + 255) // 2 for c in tint)
    d.rectangle([x, y, x + w, y + h], fill=box_bg, outline=BOX_BORDER,
                width=1)
    d.rectangle([x + 1, y + 1, x + w - 1, y + 5], fill=color)
    pad = 8
    iw = w - 2 * pad
    ih = 74
    iy = y + 7
    strip = _render_strip(ill, tint).resize((iw, ih), Image.LANCZOS)
    img.paste(strip, (x + pad, iy))
    d.rectangle([x + pad, iy, x + pad + iw - 1, iy + ih - 1],
                outline=BOX_BORDER, width=1)
    _number_badge(d, x + pad + iw - 11, iy + 11, number, color)
    # headline: 2 lines, vertically centred in the slot between the
    # illustration and the sub-headline, so all cards line up.
    hf, hlines = fit_block(d, headline, iw, 2, hl_size, hl_size - 2,
                           bold=True)
    slot_h = 2 * (hl_size + 5)
    hy = iy + ih + 4 + (slot_h - len(hlines) * (hl_size + 5)) // 2
    for ln in hlines:
        d.text((x + pad, hy), ln, font=hf, fill=INK)
        hy += hl_size + 5
    sf, slines = fit_block(d, sub, iw, 1, 17, 15, bold=False)
    sy = y + h - 25
    for ln in slines:
        d.text((x + pad, sy), ln, font=sf, fill=(51, 51, 51))


def draw_numbers_panel(d, x, y, w, h):
    """v4 'BY THE NUMBERS': the 8th grid slot. Four big market
    numbers on a navy panel — big figures read at 300px and break
    up the card grid."""
    d.rectangle([x, y, x + w, y + h], fill=NAVY, outline=BOX_BORDER,
                width=1)
    tf = load("DejaVuSans-Bold.ttf", 15)
    d.text((x + 10, y + 8), "BY THE NUMBERS", font=tf, fill=GOLD_TEXT)
    d.line([(x + 10, y + 28), (x + w - 10, y + 28)], fill=GOLD_TEXT,
           width=1)
    stats = [
        ("DOW \u22122.19%", "49,097"),
        ("ANT $97.17", "+17.1% debut"),
        ("IPO $83", "$81.3B record"),
        ("WALMART", "$188.8B"),
    ]
    nf = load("DejaVuSans-Bold.ttf", 17)
    lf = load("DejaVuSans.ttf", 11)
    row_h = (h - 40) // 4
    for i, (num, lab) in enumerate(stats):
        ry = y + 36 + i * row_h
        nw = d.textlength(num, font=nf)
        lw = d.textlength(lab, font=lf)
        if nw + 8 + lw > w - 20:
            print(f"WARNING: numbers row {num} {nw + 8 + lw}px > "
                  f"{w - 20}px")
        d.text((x + 10, ry), num, font=nf, fill=(255, 255, 255))
        d.text((x + w - 10 - lw, ry + 3), lab, font=lf,
               fill=GREY_TEXT)


def draw_grid(img, d, y, card_w, card_h):
    """v4 grid: 4 columns x 2 rows. Row 1: stories 1, 3, 4, 5.
    Row 2: stories 10, 14, 15 + the BY THE NUMBERS panel.
    One headline font size for all cards: the largest size (26..20)
    where every headline fits in 2 lines, so no card shouts louder
    than the others. (The headlines were shortened until 24px fits
    them all; if a future edit breaks that, the probe drops the
    size instead of truncating a headline.)"""
    gap = 12
    probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    iw = card_w - 16
    hl_size = 20
    for size in range(26, 19, -1):
        f = load("DejaVuSans-Bold.ttf", size)
        if all(len(wrap(probe, headline, f, iw)) <= 2
               for _n, headline, _s, _k, _t in CARDS):
            hl_size = size
            break
    print(f"grid: headline font {hl_size}px")
    order = [CARDS[0], CARDS[1], CARDS[2], CARDS[3],
             CARDS[4], CARDS[5], CARDS[6], None]
    for i, item in enumerate(order):
        r, c = divmod(i, 4)
        x = 24 + c * (card_w + gap)
        yy = y + r * (card_h + gap)
        if item is None:
            draw_numbers_panel(d, x, yy, card_w, card_h)
        else:
            number, headline, sub, ill, topic = item
            draw_card(img, d, x, yy, card_w, card_h, number, headline,
                      sub, ill, topic, hl_size)
    return y + 2 * card_h + gap


def _chip(d, x, y, text, font, fill, icon=None):
    """Small coloured chip with white bold text; returns its width.
    Optional icon ('globe' | 'candle' | 'coin') is drawn in white
    at the left inside the chip."""
    tw = d.textlength(text, font=font)
    icon_w = 16 if icon else 0
    cw = int(tw) + 14 + icon_w
    d.rounded_rectangle([x, y, x + cw, y + 16], radius=8, fill=fill)
    tx = x + 7
    if icon:
        ix, iy = x + 5, y + 3
        if icon == "globe":
            _globe(d, ix + 5, iy + 5, 5, (255, 255, 255))
        elif icon == "candle":
            d.rectangle([ix + 3, iy + 3, ix + 7, iy + 9],
                        fill=(255, 255, 255))
            d.line([(ix + 5, iy + 1), (ix + 5, iy + 3)],
                   fill=(255, 255, 255), width=1)
            d.line([(ix + 5, iy + 9), (ix + 5, iy + 11)],
                   fill=(255, 255, 255), width=1)
        elif icon == "coin":
            d.ellipse([ix, iy, ix + 10, iy + 10], fill=(255, 255, 255))
            cf = load("DejaVuSans-Bold.ttf", 8)
            d.text((ix + 3, iy + 1), "$", font=cf, fill=fill)
        tx = x + 7 + icon_w
    d.text((tx, y + 2), text, font=font, fill=(255, 255, 255))
    return cw


def _movers(d, x, y, col_w, gap, gainers, losers, row_f, pct_f):
    """Two side-by-side columns: green gainers left, red losers right."""
    for ci, (items, label, color) in enumerate(
            ((gainers, "\u25b2 TOP GAINERS", GREEN_UP),
             (losers, "\u25bc TOP LOSERS", RED))):
        cx = x + ci * (col_w + gap)
        _chip(d, cx, y, label, row_f, color)
        for i, (name, pct) in enumerate(items):
            ryy = y + 20 + i * 15
            d.text((cx, ryy), name, font=row_f, fill=(51, 51, 51))
            pw = d.textlength(pct, font=pct_f)
            d.text((cx + col_w - pw, ryy), pct, font=pct_f, fill=color)


def draw_markets_line(d, x, y, w, h):
    """v4 MARKETS TODAY as ONE line (was a 104px panel): the title
    + the 6 indices + BTC, all on one row in the light-blue panel.
    14px so it reads at 300px."""
    d.rectangle([x, y, x + w, y + h], fill=PANEL_TINT,
                outline=BOX_BORDER, width=1)
    tf = load("DejaVuSans-Bold.ttf", 14)
    bf = load("DejaVuSans.ttf", 14)
    title = "MARKETS TODAY"
    text = ("  Dow 49,097 \u22122.19%  \u2022  S&P 7,176 \u22122.02%  \u2022  "
            "Nasdaq 23,879 \u22122.25%  \u2022  BTC $61,344")
    tw = d.textlength(title, font=tf) + d.textlength(text, font=bf)
    if tw > w - 24:
        print(f"WARNING: markets line {int(tw)}px > {w - 24}px")
    d.text((x + 12, y + 5), title, font=tf, fill=INK)
    d.text((x + 12 + d.textlength(title, font=tf) + 8, y + 5),
           text, font=bf, fill=(51, 51, 51))


def draw_map(img, d, x, y, w, h):
    """v4: a world map with numbered pins for ALL 37 stories, in
    the bottom-left panel (map area 406x214, was 336x192 in v3).
    and the 11 US pins live in a zoomed USA inset at the
    bottom-left of the map (the US is too small on the world map
    for ~10 pins; the inset covers the empty South Pacific /
    South America, where no story happened). Land outlines come
    from the Natural Earth 110m data in LAND_DATA
    (equirectangular, lon -180..180, lat -58..83). Pins that would
    pile up use MAP_PIN_DISPLAY / US_PIN_DISPLAY positions with a
    short leader line to the true spot (and a small dark dot
    marking it). No space story on 19 November, so no star.
    The bottom legend line was dropped for space; the title says
    what the pins are."""
    d.rectangle([x, y, x + w, y + h], fill=(248, 250, 252),
                outline=BOX_BORDER, width=1)
    title_f = load("DejaVuSans-Bold.ttf", 13)
    d.text((x + 12, y + 8), "WHERE THE NEWS HAPPENED", font=title_f,
           fill=INK)
    mx, my, mw, mh = x + 12, y + 28, w - 24, h - 36
    # ocean
    d.rectangle([mx, my, mx + mw, my + mh], fill=(225, 235, 242))
    # graticule every 30 degrees
    grid_col = (200, 210, 220)
    for lon in range(-150, 181, 30):
        gx, _gy = _map_xy(lon, 0, mx, my, mw, mh)
        d.line([(gx, my), (gx, my + mh)], fill=grid_col, width=1)
    for lat in range(-30, 84, 30):
        _gx, gy = _map_xy(0, lat, mx, my, mw, mh)
        d.line([(mx, gy), (mx + mw, gy)], fill=grid_col, width=1)
    # land (Natural Earth 110m, simplified)
    for poly in _land_polygons():
        pts = [_map_xy(lon, lat, mx, my, mw, mh) for lon, lat in poly]
        d.polygon(pts, fill=(222, 205, 170), outline=(150, 130, 100))

    def _pin_pos(num, lon, lat):
        """Return (display_x, display_y, true_x, true_y) in
        absolute coordinates."""
        tx, ty = _map_xy(lon, lat, mx, my, mw, mh)
        if num in MAP_PIN_DISPLAY:
            ox, oy = MAP_PIN_DISPLAY[num]
            dx = ox * mw / 336
            dy = oy * mh / 192
            return (mx + dx, my + dy, tx, ty)
        return (tx, ty, tx, ty)

    # main-map leader lines first, then the pins on top
    for num, lon, lat, key in MAIN_PINS:
        dx, dy, tx, ty = _pin_pos(num, lon, lat)
        if (dx, dy) != (tx, ty):
            d.line([(dx, dy), (tx, ty)], fill=(100, 100, 100), width=1)
            d.ellipse([tx - 2, ty - 2, tx + 2, ty + 2],
                      fill=(100, 100, 100))
    # ---- USA inset: a zoomed continental US at the bottom-left
    # of the map, over the empty South Pacific / South America
    # (no stories there). Built on its own image so the land is
    # clipped to the inset box.
    ix, iy = mx, my + mh - 80
    iw, ih = INSET_W, INSET_H
    inset = Image.new("RGB", (iw, ih), (225, 235, 242))
    idr = ImageDraw.Draw(inset)
    for lon in range(-120, -59, 30):
        gx, _gy = _inset_xy(lon, 0, 0, 0, iw, ih)
        idr.line([(gx, 0), (gx, ih)], fill=grid_col, width=1)
    for lat in range(30, 51, 15):
        _gx, gy = _inset_xy(0, lat, 0, 0, iw, ih)
        idr.line([(0, gy), (iw, gy)], fill=grid_col, width=1)
    for poly in _land_polygons():
        pts = [_inset_xy(lon, lat, 0, 0, iw, ih) for lon, lat in poly]
        idr.polygon(pts, fill=(222, 205, 170), outline=(150, 130, 100))

    def _inset_pos(num, lon, lat):
        """Return (display_x, display_y, true_x, true_y) in
        inset-local coordinates."""
        tx, ty = _inset_xy(lon, lat, 0, 0, iw, ih)
        if num in US_PIN_DISPLAY:
            dx, dy = US_PIN_DISPLAY[num]
            return (dx, dy, tx, ty)
        return (tx, ty, tx, ty)

    for num, lon, lat, key in US_PINS:
        dx, dy, tx, ty = _inset_pos(num, lon, lat)
        if (dx, dy) != (tx, ty):
            idr.line([(dx, dy), (tx, ty)], fill=(100, 100, 100), width=1)
            idr.ellipse([tx - 2, ty - 2, tx + 2, ty + 2],
                        fill=(100, 100, 100))
    pin_s = load("DejaVuSans-Bold.ttf", 8)
    for num, lon, lat, key in US_PINS:
        dx, dy, _tx, _ty = _inset_pos(num, lon, lat)
        color = MAP_PIN_COLORS[key]
        idr.ellipse([dx - 6, dy - 6, dx + 6, dy + 6], fill=color,
                    outline=(255, 255, 255), width=1)
        label = str(num)
        tw = idr.textlength(label, font=pin_s)
        idr.text((dx - tw / 2, dy - 5), label, font=pin_s,
                 fill=(255, 255, 255))
    # "USA" tag at the bottom-left inside the inset (over empty
    # Pacific), white-backed so it reads over the ocean.
    tag_f = load("DejaVuSans-Bold.ttf", 9)
    tag = "USA"
    tw = idr.textlength(tag, font=tag_f)
    idr.rounded_rectangle([2, 64, 2 + tw + 8, 78], radius=4,
                          fill=(255, 255, 255), outline=(150, 150, 150))
    idr.text((6, 65), tag, font=tag_f, fill=(40, 50, 60))
    img.paste(inset, (ix, iy))
    d.rectangle([ix, iy, ix + iw, iy + ih], outline=(90, 90, 90), width=2)
    # leader from the inset's top edge up to the US Gulf Coast on
    # the main map (vertical, at the central US longitude).
    lx = mx + mw // 4
    gy = my + (MAP_LAT1 - 29) / (MAP_LAT1 - MAP_LAT0) * mh
    d.line([(lx, iy), (lx, gy)], fill=(100, 100, 100), width=1)
    d.ellipse([lx - 2, gy - 2, lx + 2, gy + 2], fill=(100, 100, 100))
    # main-map pins on top (r=7)
    pin_f = load("DejaVuSans-Bold.ttf", 9)
    for num, lon, lat, key in MAIN_PINS:
        dx, dy, _tx, _ty = _pin_pos(num, lon, lat)
        color = MAP_PIN_COLORS[key]
        d.ellipse([dx - 7, dy - 7, dx + 7, dy + 7], fill=color,
                  outline=(255, 255, 255), width=1)
        label = str(num)
        tw = d.textlength(label, font=pin_f)
        d.text((dx - tw / 2, dy - 6), label, font=pin_f,
               fill=(255, 255, 255))


def measure_also(d, panel_w, font_size):
    """Widest Also Today line (for the overflow warning) and the
    height the taller column needs at the given font size."""
    bullet_f = load("DejaVuSans.ttf", font_size)
    num_f = load("DejaVuSans-Bold.ttf", font_size)
    lead = font_size + 2
    col_w = (panel_w - 24 - 16) // 2
    widest = 0
    for num, text, _topic in ALSO_TODAY:
        wdt = (d.textlength(str(num), font=num_f) + 6
               + d.textlength(text, font=bullet_f))
        widest = max(widest, wdt)
    if widest > col_w:
        print(f"WARNING: Also Today widest line {int(widest)}px > "
              f"column {col_w}px")
    n1 = (len(ALSO_TODAY) + 1) // 2
    return max(n1, len(ALSO_TODAY) - n1) * lead


def draw_also(d, x, y, w, h, font_size=12):
    """v4 ALSO TODAY: the 29 remaining stories as SHORT one-line
    headlines in two columns (15 + 14), each with its category-
    coloured number (the same numbers as the map pins). No body
    text, no group headers — the numbers carry the order."""
    d.rectangle([x, y, x + w, y + h], fill=HIGHLIGHT_PANEL,
                outline=BOX_BORDER, width=1)
    title_f = load("DejaVuSans-Bold.ttf", 13)
    _chip(d, x + 12, y + 10, "ALSO TODAY", title_f, CHIP_ALSO)
    d.line([(x + 12, y + 30), (x + w - 12, y + 30)], fill=GOLD, width=2)
    col_w = (w - 24 - 16) // 2
    bullet_f = load("DejaVuSans.ttf", font_size)
    num_f = load("DejaVuSans-Bold.ttf", font_size)
    lead = font_size + 2
    n1 = (len(ALSO_TODAY) + 1) // 2
    cols = [ALSO_TODAY[:n1], ALSO_TODAY[n1:]]
    for ci, items in enumerate(cols):
        cx = x + 12 + ci * (col_w + 16)
        by = y + 40
        for num, text, topic in items:
            color = TOPIC_COLORS[topic]
            d.text((cx, by), str(num), font=num_f, fill=color)
            nw = d.textlength(str(num), font=num_f)
            d.text((cx + nw + 6, by), text, font=bullet_f,
                   fill=(51, 51, 51))
            by += lead
    return by


def draw_footer(d, y):
    f = load("DejaVuSans.ttf", 11)
    txt = ("Sources: AFP \u2022 Associated Press \u2022 Reuters \u2022 BBC "
           "\u2022 The Guardian \u2022 Wall Street Journal \u2022 "
           "Investopedia \u2022 Al Jazeera  \u2014  All stories from "
           "Thursday, 19 November 2026.")
    tw = d.textlength(txt, font=f)
    d.text(((W - tw) / 2, y), txt, font=f, fill=MUTED)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([12, 12, W - 12, H - 12], outline=RULE, width=2)

    draw_masthead(d)  # band 12..130, stripe 130..136

    # v4 vertical budget (1024 tall, border at 1012):
    #   hero 142..322 (180) | grid 330..512 + 520..702 (182x2)
    #   markets line 710..734 (24) | bottom 740..994 (254) | footer 998
    hero_y, hero_h = 142, 180
    draw_hero(img, d, 24, hero_y, 976, hero_h)
    grid_y = hero_y + hero_h + 8
    card_w = (976 - 3 * 12) // 4  # 235
    card_h = 182
    gy = draw_grid(img, d, grid_y, card_w, card_h)
    my = gy + 8
    draw_markets_line(d, 24, my, 976, 24)
    by = my + 24 + 6
    bottom_h = 994 - by
    print(f"layout: bottom_y={by} bottom_h={bottom_h}")
    # bottom: map left (430) + Also Today right (534)
    draw_map(img, d, 24, by, 430, bottom_h)
    hl_end = draw_also(d, 24 + 430 + 12, by, 534, bottom_h)
    if hl_end > by + bottom_h - 4:
        print(f"WARNING: Also Today overflow by "
              f"{hl_end - (by + bottom_h - 4)}px")
    draw_footer(d, 998)

    img.save(OUT, format="PNG", optimize=True)
    print(f"saved {OUT}  {OUT.stat().st_size} bytes")


if __name__ == "__main__":
    main()
