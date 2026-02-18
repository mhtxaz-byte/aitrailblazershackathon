"""
Basketball Lineup Analyzer — Multi-Game Edition
2025-26 Season
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# ═══════════════════════════════════════════════════════════════════════════
# GAME CONFIGURATIONS
# Each game defines two teams with rosters, stats, and brand colors.
#   team1 = the team whose lineup the user selects
#   team2 = the team the engine suggests a counter-lineup for
# ═══════════════════════════════════════════════════════════════════════════

GAMES = {}

# ---- Game 1: BYU vs Arizona ----
GAMES["BYU Cougars vs Arizona Wildcats"] = {
    "team1_name": "BYU Cougars",
    "team1_short": "BYU",
    "team1_color": "#002E5D",
    "team1_color_rgb": "0,46,93",
    "team2_name": "Arizona Wildcats",
    "team2_short": "Arizona",
    "team2_color": "#CC0033",
    "team2_color_rgb": "204,0,51",
    "team1_players": {
        "AJ Dybantsa": {"number": 3, "pos": "F", "height": "6'9\"", "weight": "—", "class": "FR", "hometown": "Brockton, MA", "gp": 25, "min": 33.2, "pts": 24.4, "reb": 6.6, "ast": 3.8, "stl": 1.2, "blk": 0.4, "to": 2.9, "fg_pct": 53.6, "three_pct": 35.9, "ft_pct": 75.1},
        "Robert Wright III": {"number": 1, "pos": "G", "height": "6'1\"", "weight": "183 lbs", "class": "SO", "hometown": "Wilmington, DE", "gp": 25, "min": 34.4, "pts": 18.7, "reb": 3.7, "ast": 4.9, "stl": 1.2, "blk": 0.0, "to": 2.3, "fg_pct": 48.8, "three_pct": 46.1, "ft_pct": 80.2},
        "Richie Saunders": {"number": 15, "pos": "G", "height": "6'5\"", "weight": "200 lbs", "class": "SR", "hometown": "Riverton, UT", "gp": 25, "min": 31.4, "pts": 18.0, "reb": 5.8, "ast": 2.1, "stl": 1.7, "blk": 0.3, "to": 1.6, "fg_pct": 48.9, "three_pct": 37.6, "ft_pct": 81.7},
        "Dawson Baker": {"number": 25, "pos": "G", "height": "6'4\"", "weight": "190 lbs", "class": "SR", "hometown": "Coto De Caza, CA", "gp": 6, "min": 19.8, "pts": 7.5, "reb": 1.7, "ast": 0.5, "stl": 0.5, "blk": 0.0, "to": 0.8, "fg_pct": 45.2, "three_pct": 47.4, "ft_pct": 88.9},
        "Kennard Davis Jr.": {"number": 30, "pos": "F", "height": "6'6\"", "weight": "215 lbs", "class": "JR", "hometown": "St. Louis, MO", "gp": 22, "min": 28.3, "pts": 7.2, "reb": 2.7, "ast": 1.3, "stl": 1.2, "blk": 0.1, "to": 0.8, "fg_pct": 36.5, "three_pct": 28.8, "ft_pct": 76.5},
        "Keba Keita": {"number": 13, "pos": "F", "height": "6'8\"", "weight": "231 lbs", "class": "SR", "hometown": "Bamako, Mali", "gp": 23, "min": 21.3, "pts": 6.4, "reb": 7.1, "ast": 0.3, "stl": 1.0, "blk": 1.8, "to": 0.7, "fg_pct": 63.9, "three_pct": 0.0, "ft_pct": 54.5},
        "Mihailo Bošković": {"number": 5, "pos": "F", "height": "6'10\"", "weight": "—", "class": "SR", "hometown": "Uzice, Serbia", "gp": 24, "min": 12.3, "pts": 3.3, "reb": 2.0, "ast": 0.8, "stl": 0.2, "blk": 0.5, "to": 0.6, "fg_pct": 45.3, "three_pct": 33.3, "ft_pct": 75.0},
        "Aleksej Kostić": {"number": 6, "pos": "G", "height": "6'4\"", "weight": "—", "class": "FR", "hometown": "Pfaffstätten, Austria", "gp": 17, "min": 7.7, "pts": 2.5, "reb": 0.6, "ast": 0.4, "stl": 0.2, "blk": 0.0, "to": 0.4, "fg_pct": 37.8, "three_pct": 35.3, "ft_pct": 100.0},
        "Khadim Mboup": {"number": 7, "pos": "F", "height": "6'9\"", "weight": "—", "class": "FR", "hometown": "Dakar, Senegal", "gp": 24, "min": 15.1, "pts": 2.3, "reb": 5.0, "ast": 0.5, "stl": 0.6, "blk": 0.7, "to": 0.7, "fg_pct": 44.4, "three_pct": 22.2, "ft_pct": 33.3},
        "Tyler Mrus": {"number": 2, "pos": "F", "height": "6'7\"", "weight": "205 lbs", "class": "JR", "hometown": "Bothell, WA", "gp": 21, "min": 10.1, "pts": 2.2, "reb": 1.0, "ast": 0.3, "stl": 0.2, "blk": 0.0, "to": 0.2, "fg_pct": 32.6, "three_pct": 31.0, "ft_pct": 85.7},
        "Abdullah Ahmed": {"number": 34, "pos": "C", "height": "6'10\"", "weight": "220 lbs", "class": "SO", "hometown": "Cairo, Egypt", "gp": 12, "min": 14.0, "pts": 1.9, "reb": 3.8, "ast": 0.6, "stl": 0.2, "blk": 2.0, "to": 0.5, "fg_pct": 56.3, "three_pct": 0.0, "ft_pct": 50.0},
        "Dominique Diomande": {"number": 24, "pos": "F", "height": "6'7\"", "weight": "190 lbs", "class": "FR", "hometown": "Paris, France", "gp": 16, "min": 5.8, "pts": 1.9, "reb": 0.9, "ast": 0.2, "stl": 0.3, "blk": 0.0, "to": 0.1, "fg_pct": 39.1, "three_pct": 16.7, "ft_pct": 62.5},
        "Xavion Staton": {"number": 33, "pos": "C", "height": "6'11\"", "weight": "—", "class": "FR", "hometown": "Las Vegas, NV", "gp": 9, "min": 4.9, "pts": 0.6, "reb": 0.4, "ast": 0.3, "stl": 0.0, "blk": 0.6, "to": 0.1, "fg_pct": 50.0, "three_pct": 0.0, "ft_pct": 50.0},
        "Brody Kozlowski": {"number": 4, "pos": "F", "height": "6'8\"", "weight": "—", "class": "SO", "hometown": "Draper, UT", "gp": 0, "min": 0.0, "pts": 0.0, "reb": 0.0, "ast": 0.0, "stl": 0.0, "blk": 0.0, "to": 0.0, "fg_pct": 0.0, "three_pct": 0.0, "ft_pct": 0.0},
        "Nate Pickens": {"number": 12, "pos": "G", "height": "6'3\"", "weight": "—", "class": "SR", "hometown": "El Mirage, AZ", "gp": 0, "min": 0.0, "pts": 0.0, "reb": 0.0, "ast": 0.0, "stl": 0.0, "blk": 0.0, "to": 0.0, "fg_pct": 0.0, "three_pct": 0.0, "ft_pct": 0.0},
        "Jared McGregor": {"number": 51, "pos": "G", "height": "6'3\"", "weight": "180 lbs", "class": "SR", "hometown": "Saratoga Springs, UT", "gp": 6, "min": 1.2, "pts": 0.0, "reb": 0.3, "ast": 0.3, "stl": 0.0, "blk": 0.0, "to": 0.0, "fg_pct": 0.0, "three_pct": 0.0, "ft_pct": 0.0},
        "KJ Perry": {"number": 0, "pos": "G", "height": "6'3\"", "weight": "180 lbs", "class": "FR", "hometown": "—", "gp": 0, "min": 0.0, "pts": 0.0, "reb": 0.0, "ast": 0.0, "stl": 0.0, "blk": 0.0, "to": 0.0, "fg_pct": 0.0, "three_pct": 0.0, "ft_pct": 0.0},
    },
    "team2_players": {
        "Brayden Burries": {"number": 5, "pos": "G", "height": "6'4\"", "weight": "205 lbs", "class": "FR", "hometown": "San Bernardino, CA", "gp": 25, "min": 29.1, "pts": 15.7, "reb": 4.7, "ast": 2.6, "stl": 1.6, "blk": 0.2, "to": 0.0, "fg_pct": 50.0, "three_pct": 37.3, "ft_pct": 79.6},
        "Koa Peat": {"number": 10, "pos": "F", "height": "6'8\"", "weight": "235 lbs", "class": "FR", "hometown": "Chandler, AZ", "gp": 25, "min": 27.0, "pts": 13.8, "reb": 5.4, "ast": 2.6, "stl": 0.7, "blk": 0.7, "to": 0.0, "fg_pct": 54.2, "three_pct": 33.3, "ft_pct": 60.6},
        "Jaden Bradley": {"number": 0, "pos": "G", "height": "6'3\"", "weight": "200 lbs", "class": "SR", "hometown": "Rochester, NY", "gp": 25, "min": 29.2, "pts": 13.4, "reb": 3.4, "ast": 4.4, "stl": 1.8, "blk": 0.0, "to": 0.0, "fg_pct": 48.7, "three_pct": 40.0, "ft_pct": 79.8},
        "Motiejus Krivas": {"number": 13, "pos": "C", "height": "7'2\"", "weight": "260 lbs", "class": "JR", "hometown": "Siaulia, Lithuania", "gp": 25, "min": 24.6, "pts": 11.1, "reb": 8.7, "ast": 1.1, "stl": 0.7, "blk": 1.9, "to": 0.0, "fg_pct": 59.4, "three_pct": 33.3, "ft_pct": 79.2},
        "Tobe Awaka": {"number": 30, "pos": "F", "height": "6'8\"", "weight": "255 lbs", "class": "SR", "hometown": "Hyde Park, NY", "gp": 25, "min": 21.2, "pts": 10.0, "reb": 9.7, "ast": 1.0, "stl": 0.3, "blk": 0.7, "to": 0.0, "fg_pct": 60.5, "three_pct": 62.5, "ft_pct": 65.3},
        "Ivan Kharchenkov": {"number": 8, "pos": "F", "height": "6'7\"", "weight": "220 lbs", "class": "FR", "hometown": "Munich, Germany", "gp": 25, "min": 26.2, "pts": 9.7, "reb": 3.6, "ast": 2.2, "stl": 1.6, "blk": 0.4, "to": 0.0, "fg_pct": 48.7, "three_pct": 29.2, "ft_pct": 72.5},
        "Anthony Dell'Orso": {"number": 3, "pos": "G", "height": "6'6\"", "weight": "205 lbs", "class": "SR", "hometown": "Melbourne, Australia", "gp": 25, "min": 20.8, "pts": 8.0, "reb": 2.0, "ast": 2.4, "stl": 0.9, "blk": 0.2, "to": 0.0, "fg_pct": 38.4, "three_pct": 29.7, "ft_pct": 86.0},
        "Addison Arnold": {"number": 22, "pos": "G", "height": "6'3\"", "weight": "185 lbs", "class": "SO", "hometown": "Simi Valley, CA", "gp": 0, "min": 0.0, "pts": 0.0, "reb": 0.0, "ast": 0.0, "stl": 0.0, "blk": 0.0, "to": 0.0, "fg_pct": 0.0, "three_pct": 0.0, "ft_pct": 0.0},
        "Dwayne Aristode": {"number": 2, "pos": "F", "height": "6'8\"", "weight": "220 lbs", "class": "FR", "hometown": "Lelystad, Netherlands", "gp": 0, "min": 0.0, "pts": 0.0, "reb": 0.0, "ast": 0.0, "stl": 0.0, "blk": 0.0, "to": 0.0, "fg_pct": 0.0, "three_pct": 0.0, "ft_pct": 0.0},
        "Jackson Cook": {"number": 11, "pos": "G", "height": "6'3\"", "weight": "185 lbs", "class": "SO", "hometown": "Oxford, England", "gp": 0, "min": 0.0, "pts": 0.0, "reb": 0.0, "ast": 0.0, "stl": 0.0, "blk": 0.0, "to": 0.0, "fg_pct": 0.0, "three_pct": 0.0, "ft_pct": 0.0},
        "Sven Djopmo": {"number": 42, "pos": "G", "height": "6'2\"", "weight": "190 lbs", "class": "SO", "hometown": "Reims, France", "gp": 0, "min": 0.0, "pts": 0.0, "reb": 0.0, "ast": 0.0, "stl": 0.0, "blk": 0.0, "to": 0.0, "fg_pct": 0.0, "three_pct": 0.0, "ft_pct": 0.0},
        "Jackson Francois": {"number": 7, "pos": "G", "height": "6'5\"", "weight": "160 lbs", "class": "SR", "hometown": "Las Vegas, NV", "gp": 0, "min": 0.0, "pts": 0.0, "reb": 0.0, "ast": 0.0, "stl": 0.0, "blk": 0.0, "to": 0.0, "fg_pct": 0.0, "three_pct": 0.0, "ft_pct": 0.0},
        "Sidi Gueye": {"number": 15, "pos": "F", "height": "6'11\"", "weight": "215 lbs", "class": "FR", "hometown": "Guediawaye, Senegal", "gp": 0, "min": 0.0, "pts": 0.0, "reb": 0.0, "ast": 0.0, "stl": 0.0, "blk": 0.0, "to": 0.0, "fg_pct": 0.0, "three_pct": 0.0, "ft_pct": 0.0},
        "Bryce James": {"number": 6, "pos": "G", "height": "6'5\"", "weight": "195 lbs", "class": "FR", "hometown": "Akron, OH", "gp": 0, "min": 0.0, "pts": 0.0, "reb": 0.0, "ast": 0.0, "stl": 0.0, "blk": 0.0, "to": 0.0, "fg_pct": 0.0, "three_pct": 0.0, "ft_pct": 0.0},
        "Mabil Mawut": {"number": 20, "pos": "F", "height": "6'11\"", "weight": "200 lbs", "class": "FR", "hometown": "Bor, South Sudan", "gp": 0, "min": 0.0, "pts": 0.0, "reb": 0.0, "ast": 0.0, "stl": 0.0, "blk": 0.0, "to": 0.0, "fg_pct": 0.0, "three_pct": 0.0, "ft_pct": 0.0},
        "Evan Nelson": {"number": 21, "pos": "G", "height": "6'2\"", "weight": "175 lbs", "class": "SR", "hometown": "Tucson, AZ", "gp": 0, "min": 0.0, "pts": 0.0, "reb": 0.0, "ast": 0.0, "stl": 0.0, "blk": 0.0, "to": 0.0, "fg_pct": 0.0, "three_pct": 0.0, "ft_pct": 0.0},
    },
}

# ---- Game 2: Wisconsin vs Ohio State ----
GAMES["Wisconsin Badgers vs Ohio State Buckeyes"] = {
    "team1_name": "Wisconsin Badgers",
    "team1_short": "Wisconsin",
    "team1_color": "#C5050C",
    "team1_color_rgb": "197,5,12",
    "team2_name": "Ohio State Buckeyes",
    "team2_short": "Ohio State",
    "team2_color": "#BB0000",
    "team2_color_rgb": "187,0,0",
    "team1_players": {
        "Nick Boyd": {"number": 2, "pos": "G", "height": "6'3\"", "weight": "177 lbs", "class": "SR", "hometown": "Garnerville, NY", "gp": 25, "min": 30.9, "pts": 20.6, "reb": 3.4, "ast": 3.7, "stl": 0.9, "blk": 0.0, "to": 1.7, "fg_pct": 47.9, "three_pct": 37.4, "ft_pct": 81.6},
        "John Blackwell": {"number": 25, "pos": "G", "height": "6'4\"", "weight": "203 lbs", "class": "JR", "hometown": "Bloomfield Hills, MI", "gp": 24, "min": 33.3, "pts": 19.0, "reb": 5.0, "ast": 2.4, "stl": 1.3, "blk": 0.1, "to": 1.6, "fg_pct": 40.9, "three_pct": 37.6, "ft_pct": 85.6},
        "Nolan Winter": {"number": 31, "pos": "F", "height": "7'0\"", "weight": "235 lbs", "class": "JR", "hometown": "Lakeville, MN", "gp": 25, "min": 31.3, "pts": 13.7, "reb": 9.0, "ast": 1.7, "stl": 0.6, "blk": 1.2, "to": 0.9, "fg_pct": 57.3, "three_pct": 32.1, "ft_pct": 74.2},
        "Austin Rapp": {"number": 22, "pos": "F", "height": "6'10\"", "weight": "238 lbs", "class": "SO", "hometown": "Melbourne, Australia", "gp": 21, "min": 21.5, "pts": 9.3, "reb": 3.8, "ast": 1.7, "stl": 0.5, "blk": 0.6, "to": 0.9, "fg_pct": 42.1, "three_pct": 33.3, "ft_pct": 84.4},
        "Braeden Carrington": {"number": 0, "pos": "G", "height": "6'5\"", "weight": "197 lbs", "class": "SR", "hometown": "Brooklyn Park, MN", "gp": 24, "min": 16.5, "pts": 7.1, "reb": 2.6, "ast": 0.9, "stl": 0.3, "blk": 0.3, "to": 0.5, "fg_pct": 41.0, "three_pct": 40.8, "ft_pct": 74.4},
        "Andrew Rohde": {"number": 7, "pos": "G", "height": "6'6\"", "weight": "195 lbs", "class": "SR", "hometown": "Brookfield, WI", "gp": 24, "min": 25.5, "pts": 6.4, "reb": 2.0, "ast": 2.8, "stl": 1.2, "blk": 0.1, "to": 1.0, "fg_pct": 38.8, "three_pct": 31.6, "ft_pct": 76.2},
        "Aleksas Bieliauskas": {"number": 32, "pos": "F", "height": "6'10\"", "weight": "235 lbs", "class": "FR", "hometown": "Kaunas, Lithuania", "gp": 25, "min": 17.7, "pts": 4.4, "reb": 4.0, "ast": 0.7, "stl": 0.2, "blk": 0.7, "to": 0.9, "fg_pct": 43.8, "three_pct": 30.8, "ft_pct": 66.7},
        "Jack Janicki": {"number": 5, "pos": "G", "height": "6'5\"", "weight": "200 lbs", "class": "SO", "hometown": "White Bear Lake, MN", "gp": 25, "min": 16.7, "pts": 2.2, "reb": 2.0, "ast": 1.1, "stl": 0.7, "blk": 0.2, "to": 0.6, "fg_pct": 31.3, "three_pct": 27.7, "ft_pct": 60.0},
        "Zach Kinziger": {"number": 4, "pos": "G", "height": "6'3\"", "weight": "185 lbs", "class": "FR", "hometown": "De Pere, WI", "gp": 10, "min": 6.2, "pts": 1.9, "reb": 0.4, "ast": 0.4, "stl": 0.4, "blk": 0.0, "to": 0.1, "fg_pct": 35.0, "three_pct": 33.3, "ft_pct": 50.0},
        "Hayden Jones": {"number": 13, "pos": "G", "height": "6'6\"", "weight": "198 lbs", "class": "FR", "hometown": "Nelson, New Zealand", "gp": 18, "min": 6.7, "pts": 1.7, "reb": 1.1, "ast": 0.3, "stl": 0.1, "blk": 0.0, "to": 0.6, "fg_pct": 60.0, "three_pct": 100.0, "ft_pct": 57.9},
        "Jack Robison": {"number": 11, "pos": "F", "height": "6'6\"", "weight": "198 lbs", "class": "SO", "hometown": "Lakeville, MN", "gp": 13, "min": 2.1, "pts": 1.1, "reb": 0.5, "ast": 0.1, "stl": 0.1, "blk": 0.1, "to": 0.3, "fg_pct": 83.3, "three_pct": 75.0, "ft_pct": 50.0},
        "Will Garlock": {"number": 23, "pos": "F", "height": "7'0\"", "weight": "243 lbs", "class": "FR", "hometown": "Middleton, WI", "gp": 23, "min": 6.8, "pts": 1.0, "reb": 1.1, "ast": 0.9, "stl": 0.1, "blk": 0.1, "to": 0.4, "fg_pct": 75.0, "three_pct": 0.0, "ft_pct": 35.7},
        "Isaac Gard": {"number": 15, "pos": "G", "height": "6'3\"", "weight": "170 lbs", "class": "SR", "hometown": "Oregon, WI", "gp": 12, "min": 1.2, "pts": 0.7, "reb": 0.3, "ast": 0.1, "stl": 0.0, "blk": 0.0, "to": 0.2, "fg_pct": 40.0, "three_pct": 50.0, "ft_pct": 100.0},
        "Elijah Gray": {"number": 6, "pos": "F", "height": "6'9\"", "weight": "235 lbs", "class": "SR", "hometown": "Charlotte, NC", "gp": 0, "min": 0.0, "pts": 0.0, "reb": 0.0, "ast": 0.0, "stl": 0.0, "blk": 0.0, "to": 0.0, "fg_pct": 0.0, "three_pct": 0.0, "ft_pct": 0.0},
        "Riccardo Greppi": {"number": 18, "pos": "F", "height": "6'10\"", "weight": "255 lbs", "class": "SO", "hometown": "Lecco, Italy", "gp": 12, "min": 1.3, "pts": 0.0, "reb": 0.3, "ast": 0.2, "stl": 0.0, "blk": 0.0, "to": 0.2, "fg_pct": 0.0, "three_pct": 0.0, "ft_pct": 0.0},
    },
    "team2_players": {
        "Bruce Thornton": {"number": 2, "pos": "G", "height": "6'2\"", "weight": "215 lbs", "class": "SR", "hometown": "Fairburn, GA", "gp": 25, "min": 36.2, "pts": 19.6, "reb": 5.3, "ast": 3.8, "stl": 1.3, "blk": 0.3, "to": 1.4, "fg_pct": 54.9, "three_pct": 38.9, "ft_pct": 82.5},
        "John Mobley Jr.": {"number": 0, "pos": "G", "height": "6'1\"", "weight": "175 lbs", "class": "SO", "hometown": "Reynoldsburg, OH", "gp": 24, "min": 31.0, "pts": 15.1, "reb": 2.5, "ast": 2.8, "stl": 0.8, "blk": 0.1, "to": 1.7, "fg_pct": 42.2, "three_pct": 40.0, "ft_pct": 87.8},
        "Devin Royal": {"number": 21, "pos": "F", "height": "6'6\"", "weight": "220 lbs", "class": "JR", "hometown": "Pickerington, OH", "gp": 24, "min": 32.4, "pts": 13.6, "reb": 5.6, "ast": 1.7, "stl": 0.6, "blk": 0.1, "to": 1.9, "fg_pct": 47.9, "three_pct": 29.5, "ft_pct": 81.1},
        "Christoph Tilly": {"number": 13, "pos": "C", "height": "7'0\"", "weight": "240 lbs", "class": "SR", "hometown": "Berlin, Germany", "gp": 24, "min": 26.5, "pts": 11.8, "reb": 4.7, "ast": 2.4, "stl": 0.6, "blk": 0.6, "to": 1.6, "fg_pct": 45.6, "three_pct": 23.5, "ft_pct": 76.0},
        "Amare Bynum": {"number": 1, "pos": "F", "height": "6'8\"", "weight": "220 lbs", "class": "FR", "hometown": "Omaha, NE", "gp": 25, "min": 27.4, "pts": 9.4, "reb": 4.6, "ast": 1.0, "stl": 0.6, "blk": 0.8, "to": 1.1, "fg_pct": 48.9, "three_pct": 28.1, "ft_pct": 72.7},
        "Brandon Noel": {"number": 14, "pos": "F", "height": "6'8\"", "weight": "240 lbs", "class": "SR", "hometown": "Lucasville, OH", "gp": 14, "min": 20.6, "pts": 7.4, "reb": 4.1, "ast": 1.0, "stl": 0.3, "blk": 0.2, "to": 1.1, "fg_pct": 64.3, "three_pct": 21.4, "ft_pct": 73.3},
        "Taison Chatman": {"number": 3, "pos": "G", "height": "6'4\"", "weight": "175 lbs", "class": "SO", "hometown": "Minneapolis, MN", "gp": 20, "min": 10.2, "pts": 4.0, "reb": 1.0, "ast": 0.7, "stl": 0.4, "blk": 0.1, "to": 0.6, "fg_pct": 52.0, "three_pct": 53.3, "ft_pct": 78.6},
        "Puff Johnson": {"number": 6, "pos": "G", "height": "6'8\"", "weight": "210 lbs", "class": "SR", "hometown": "Moon Township, PA", "gp": 5, "min": 10.6, "pts": 3.0, "reb": 1.2, "ast": 0.0, "stl": 0.2, "blk": 0.0, "to": 0.4, "fg_pct": 57.1, "three_pct": 75.0, "ft_pct": 80.0},
        "Ivan Njegovan": {"number": 7, "pos": "C", "height": "7'1\"", "weight": "250 lbs", "class": "SO", "hometown": "Otocac, Croatia", "gp": 21, "min": 11.1, "pts": 2.9, "reb": 3.3, "ast": 0.7, "stl": 0.1, "blk": 0.4, "to": 0.7, "fg_pct": 53.5, "three_pct": 50.0, "ft_pct": 60.9},
        "Gabe Cupps": {"number": 4, "pos": "G", "height": "6'2\"", "weight": "180 lbs", "class": "SO", "hometown": "Dayton, OH", "gp": 24, "min": 13.1, "pts": 1.8, "reb": 1.3, "ast": 1.3, "stl": 0.5, "blk": 0.0, "to": 0.7, "fg_pct": 37.5, "three_pct": 23.5, "ft_pct": 82.4},
        "Mathieu Grujicic": {"number": 9, "pos": "G", "height": "6'6\"", "weight": "205 lbs", "class": "FR", "hometown": "Berlin, Germany", "gp": 6, "min": 5.3, "pts": 1.0, "reb": 0.8, "ast": 0.3, "stl": 0.2, "blk": 0.0, "to": 0.2, "fg_pct": 12.5, "three_pct": 14.3, "ft_pct": 42.9},
        "Colin White": {"number": 20, "pos": "F", "height": "6'6\"", "weight": "205 lbs", "class": "SO", "hometown": "Ottawa, OH", "gp": 23, "min": 8.5, "pts": 0.8, "reb": 1.0, "ast": 0.4, "stl": 0.3, "blk": 0.1, "to": 0.1, "fg_pct": 37.5, "three_pct": 0.0, "ft_pct": 33.3},
        "Myles Herro": {"number": 8, "pos": "G", "height": "6'3\"", "weight": "165 lbs", "class": "FR", "hometown": "Milwaukee, WI", "gp": 0, "min": 0.0, "pts": 0.0, "reb": 0.0, "ast": 0.0, "stl": 0.0, "blk": 0.0, "to": 0.0, "fg_pct": 0.0, "three_pct": 0.0, "ft_pct": 0.0},
        "Braylen Nash": {"number": 55, "pos": "G", "height": "6'4\"", "weight": "180 lbs", "class": "SO", "hometown": "New Albany, OH", "gp": 4, "min": 0.8, "pts": 0.0, "reb": 0.0, "ast": 0.3, "stl": 0.0, "blk": 0.0, "to": 0.0, "fg_pct": 0.0, "three_pct": 0.0, "ft_pct": 0.0},
        "Josh Ojianwuna": {"number": 17, "pos": "F", "height": "6'10\"", "weight": "230 lbs", "class": "SR", "hometown": "Asaba, Nigeria", "gp": 0, "min": 0.0, "pts": 0.0, "reb": 0.0, "ast": 0.0, "stl": 0.0, "blk": 0.0, "to": 0.0, "fg_pct": 0.0, "three_pct": 0.0, "ft_pct": 0.0},
    },
}


# ═══════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS (all team-agnostic, accept colors/names as params)
# ═══════════════════════════════════════════════════════════════════════════

def height_to_inches(h: str) -> int:
    h = h.replace('"', "").replace("'", " ").strip()
    parts = h.split()
    return int(parts[0]) * 12 + int(parts[1]) if len(parts) == 2 else 0


POSITION_COMPAT = {
    ("G", "G"): 1.0, ("G", "F"): 0.4, ("G", "C"): 0.1,
    ("F", "G"): 0.4, ("F", "F"): 1.0, ("F", "C"): 0.6,
    ("C", "G"): 0.1, ("C", "F"): 0.6, ("C", "C"): 1.0,
}


def matchup_score(p1: dict, p2: dict) -> float:
    score = 0.0
    score += POSITION_COMPAT.get((p1["pos"], p2["pos"]), 0.3) * 30
    h1, h2 = height_to_inches(p1["height"]), height_to_inches(p2["height"])
    if h1 > 0 and h2 > 0:
        score += max(0, 20 - abs(h1 - h2) * 3)
    if p2["pts"] > 0:
        score += min(p2["pts"] / 20.0, 1.0) * 15
    defensive = p2["stl"] + p2["blk"]
    score += min(defensive / 3.0, 1.0) * (15 if p1["pts"] >= 15 else 8)
    if p1["reb"] >= 5:
        score += min(p2["reb"] / 10.0, 1.0) * 10
    else:
        score += min(p2["reb"] / 10.0, 1.0) * 5
    score += min(p2["min"] / 30.0, 1.0) * 10
    return score


def generate_matchup_reason(n1: str, p1: dict, n2: str, p2: dict) -> str:
    reasons = []
    if p1["pos"] == p2["pos"]:
        reasons.append(f"same position ({p2['pos']})")
    else:
        reasons.append(f"positional flex ({p2['pos']} guarding {p1['pos']})")
    h1, h2 = height_to_inches(p1["height"]), height_to_inches(p2["height"])
    if h1 > 0 and h2 > 0:
        diff = h2 - h1
        if diff > 2:
            reasons.append(f"{diff}\" taller — size advantage")
        elif diff < -2:
            reasons.append(f"gives up {abs(diff)}\" but compensates elsewhere")
    if p1["pts"] >= 15 and (p2["stl"] + p2["blk"]) >= 1.5:
        reasons.append(f"strong defender ({p2['stl']:.1f} STL, {p2['blk']:.1f} BLK) to counter {n1}'s {p1['pts']:.1f} PPG")
    if p2["pts"] >= 10:
        reasons.append(f"scores {p2['pts']:.1f} PPG on the other end")
    if p2["reb"] >= 7 and p1["reb"] >= 5:
        reasons.append(f"matches on the glass ({p2['reb']:.1f} RPG)")
    return "; ".join(reasons).capitalize() if reasons else "Best available matchup"


def find_best_lineup(selected_names: list[str], t1_players: dict, t2_players: dict) -> list[dict]:
    ordered = sorted(selected_names, key=lambda n: t1_players[n]["pts"], reverse=True)
    available = {n: p for n, p in t2_players.items() if p["gp"] > 0}
    used = set()
    results = []
    for name1 in ordered:
        p1 = t1_players[name1]
        best_name, best_score = None, -1
        for name2, p2 in available.items():
            if name2 in used:
                continue
            s = matchup_score(p1, p2)
            if s > best_score:
                best_score, best_name = s, name2
        if best_name is None:
            remaining = [n for n in t2_players if n not in used]
            best_name = remaining[0] if remaining else None
        if best_name:
            p2 = t2_players[best_name]
            reason = generate_matchup_reason(name1, p1, best_name, p2)
            results.append({"t1_name": name1, "t1": p1, "t2_name": best_name, "t2": p2, "score": best_score, "reason": reason})
            used.add(best_name)
    return results


# ---- Heatmap ----

MATCHUP_AXES = ["Position", "Size", "Scoring", "Defense", "Rebounding", "Efficiency"]


def _axis_advantage(p1: dict, p2: dict) -> list[float]:
    pos_order = {"C": 3, "F": 2, "G": 1}
    pos_val = max(-1, min(1, (pos_order.get(p1["pos"], 2) - pos_order.get(p2["pos"], 2)) * 0.5))
    h1, h2 = height_to_inches(p1["height"]), height_to_inches(p2["height"])
    size_val = max(-1.0, min(1.0, (h1 - h2) / 6.0)) if h1 and h2 else 0.0
    scoring_val = max(-1.0, min(1.0, (p1["pts"] - p2["pts"]) / 15.0))
    def_val = max(-1.0, min(1.0, ((p1["stl"] + p1["blk"]) - (p2["stl"] + p2["blk"])) / 3.0))
    reb_val = max(-1.0, min(1.0, (p1["reb"] - p2["reb"]) / 6.0))
    eff_val = max(-1.0, min(1.0, (p1["fg_pct"] - p2["fg_pct"]) / 20.0))
    return [pos_val, size_val, scoring_val, def_val, reb_val, eff_val]


def build_matchup_matrix(results: list[dict], t1_short: str, t2_short: str, t1_color: str, t2_color: str) -> go.Figure:
    n = len(results)
    z, hover_text, y_labels = [], [], []
    for r in results:
        vals = _axis_advantage(r["t1"], r["t2"])
        z.append(vals)
        row_hover = []
        for ax, v in zip(MATCHUP_AXES, vals):
            who = t1_short if v > 0 else t2_short if v < 0 else "Even"
            row_hover.append(f"{r['t1_name']} vs {r['t2_name']}<br>{ax}: {who} advantage ({v:+.2f})")
        hover_text.append(row_hover)
        y_labels.append(f"{r['t1_name']}  vs  {r['t2_name']}")

    # Derive lighter shades from team colors for the colorscale
    fig = go.Figure(data=go.Heatmap(
        z=z, x=MATCHUP_AXES, y=y_labels, hovertext=hover_text, hoverinfo="text",
        colorscale=[
            [0.0, t2_color], [0.35, "#ef9a9a"], [0.5, "#ffffff"],
            [0.65, "#90caf9"], [1.0, t1_color],
        ],
        zmin=-1, zmax=1,
        colorbar=dict(title="Advantage", tickvals=[-1, -0.5, 0, 0.5, 1],
                      ticktext=[f"{t2_short} ++", f"{t2_short} +", "Even", f"{t1_short} +", f"{t1_short} ++"],
                      tickfont=dict(size=11)),
    ))
    fig.update_layout(height=60 + n * 70, margin=dict(t=30, b=30, l=10, r=10), yaxis=dict(autorange="reversed"), xaxis_side="top")
    return fig


# ---- Predicted outcome diverging bar chart ----

def build_predicted_outcome_chart(results: list[dict], t1_name: str, t2_name: str, t1_short: str, t2_short: str, t1_color: str, t2_color: str) -> go.Figure:
    cats = ["PPG", "RPG", "APG", "STL", "BLK", "FG%"]
    keys = ["pts", "reb", "ast", "stl", "blk", "fg_pct"]
    n = len(results) or 1
    t1_vals, t2_vals = [], []
    for k in keys:
        t1_vals.append(sum(r["t1"][k] for r in results))
        t2_vals.append(sum(r["t2"][k] for r in results))
    t1_vals[-1] /= n
    t2_vals[-1] /= n

    fig = go.Figure()
    fig.add_trace(go.Bar(y=cats, x=[-v for v in t1_vals], orientation="h", name=t1_name, marker_color=t1_color,
                         text=[f"{v:.1f}" for v in t1_vals], textposition="inside", insidetextanchor="middle", textfont=dict(color="white", size=13)))
    fig.add_trace(go.Bar(y=cats, x=t2_vals, orientation="h", name=t2_name, marker_color=t2_color,
                         text=[f"{v:.1f}" for v in t2_vals], textposition="inside", insidetextanchor="middle", textfont=dict(color="white", size=13)))
    max_val = max(max(t1_vals), max(t2_vals)) * 1.15
    fig.update_layout(barmode="overlay",
                      xaxis=dict(range=[-max_val, max_val], zeroline=True, zerolinewidth=2, zerolinecolor="black", showticklabels=False),
                      yaxis=dict(autorange="reversed"), legend=dict(orientation="h", y=1.12, x=0.3), margin=dict(t=50, b=20, l=10, r=10), height=320)
    fig.add_annotation(x=0, y=-0.3, text="0", showarrow=False, yref="paper", font=dict(size=11, color="gray"))
    fig.add_annotation(x=-max_val * 0.5, y=-0.12, text=f"< {t1_short}", showarrow=False, yref="paper", font=dict(size=12, color=t1_color, family="Arial Black"))
    fig.add_annotation(x=max_val * 0.5, y=-0.12, text=f"{t2_short} >", showarrow=False, yref="paper", font=dict(size=12, color=t2_color, family="Arial Black"))
    return fig


# ---- Bench recommendation ----

def rank_bench_options(starter_names: list[str], results: list[dict], team_players: dict, is_team2: bool = False) -> list[dict]:
    starters = set(starter_names)
    bench = []
    for name, p in team_players.items():
        if name in starters or p["gp"] == 0:
            continue
        impact = p["pts"] * 1.0 + p["reb"] * 0.8 + p["ast"] * 0.7 + p["stl"] * 1.2 + p["blk"] * 1.2 + p["fg_pct"] * 0.05 + p["min"] * 0.1
        starter_positions = [team_players[n]["pos"] for n in starters if n in team_players]
        if starter_positions.count(p["pos"]) <= 1:
            impact *= 1.25
        best_replace, best_replace_reason = None, "general depth"
        for r in results:
            if is_team2:
                teammate, teammate_name, opponent, opponent_name = r["t2"], r["t2_name"], r["t1"], r["t1_name"]
            else:
                teammate, teammate_name, opponent, opponent_name = r["t1"], r["t1_name"], r["t2"], r["t2_name"]
            if teammate["pos"] == p["pos"] or (teammate["pos"] in ("F", "G") and p["pos"] in ("F", "G")):
                if best_replace is None or teammate["pts"] < team_players.get(best_replace, {"pts": 999}).get("pts", 999):
                    best_replace = teammate_name
                    if is_team2:
                        axis_vals = _axis_advantage(opponent, teammate)
                        weakest_idx = int(np.argmax(axis_vals))
                    else:
                        axis_vals = _axis_advantage(teammate, opponent)
                        weakest_idx = int(np.argmin(axis_vals))
                    best_replace_reason = f"could shore up {MATCHUP_AXES[weakest_idx].lower()} vs {opponent_name}"
        bench.append({"name": name, "player": p, "impact": impact, "replace_for": best_replace, "reason": best_replace_reason})

    if not bench:
        return bench
    max_impact = max(b["impact"] for b in bench)
    for b in bench:
        b["stars"] = max(0.5, min(5.0, round((b["impact"] / max_impact) * 5 * 2) / 2))
    bench.sort(key=lambda b: b["impact"], reverse=True)
    return bench


def stars_display(n: float) -> str:
    full = int(n)
    half = 1 if (n - full) >= 0.5 else 0
    empty = 5 - full - half
    return ("★" * full) + ("½" * half) + ("☆" * empty) + f"  ({n:.1f}/5.0)"


# ---- Spider / Radar charts ----

RADAR_CATEGORIES = ["Scoring", "Rebounding", "Playmaking", "Steals", "Blocks", "Efficiency"]


def _team_radar_values(player_dicts: list[dict]) -> list[float]:
    n = len(player_dicts) or 1
    avg = lambda key: sum(p[key] for p in player_dicts) / n
    return [
        min(avg("pts") / 25.0, 1.0) * 100,
        min(avg("reb") / 10.0, 1.0) * 100,
        min(avg("ast") / 6.0, 1.0) * 100,
        min(avg("stl") / 2.5, 1.0) * 100,
        min(avg("blk") / 2.5, 1.0) * 100,
        min(avg("fg_pct") / 65.0, 1.0) * 100,
    ]


def build_radar_chart(t1_players: list[dict], t2_players: list[dict], t1_name: str, t2_name: str, t1_color: str, t1_rgb: str, t2_color: str, t2_rgb: str) -> go.Figure:
    t1_vals = _team_radar_values(t1_players)
    t2_vals = _team_radar_values(t2_players)
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=t1_vals + [t1_vals[0]], theta=RADAR_CATEGORIES + [RADAR_CATEGORIES[0]], fill="toself", name=t1_name, line_color=t1_color, fillcolor=f"rgba({t1_rgb},0.25)"))
    fig.add_trace(go.Scatterpolar(r=t2_vals + [t2_vals[0]], theta=RADAR_CATEGORIES + [RADAR_CATEGORIES[0]], fill="toself", name=t2_name, line_color=t2_color, fillcolor=f"rgba({t2_rgb},0.25)"))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), legend=dict(x=0.35, y=-0.1, orientation="h"), margin=dict(t=40, b=40, l=60, r=60), height=450)
    return fig


# ---- Game simulation ----

def simulate_game(t1_players: list[dict], t2_players: list[dict], t1_name: str, t2_name: str, t1_color: str, t1_rgb: str, t2_color: str, t2_rgb: str, confidence_pct: int = 90, n_sims: int = 500, seed: int = 42):
    rng = np.random.default_rng(seed)
    n_poss = 70
    t1_ppg = sum(p["pts"] for p in t1_players)
    t2_ppg = sum(p["pts"] for p in t2_players)
    t1_rate, t2_rate = t1_ppg / n_poss, t2_ppg / n_poss
    t1_fg = np.mean([p["fg_pct"] for p in t1_players]) if t1_players else 45
    t2_fg = np.mean([p["fg_pct"] for p in t2_players]) if t2_players else 45
    t1_sigma = t1_rate * (1.0 - t1_fg / 100) * 1.2
    t2_sigma = t2_rate * (1.0 - t2_fg / 100) * 1.2

    t1_cum = np.clip(rng.normal(t1_rate, t1_sigma, (n_sims, n_poss)), 0, None).cumsum(axis=1)
    t2_cum = np.clip(rng.normal(t2_rate, t2_sigma, (n_sims, n_poss)), 0, None).cumsum(axis=1)
    possessions = np.arange(1, n_poss + 1)
    lo, hi = (100 - confidence_pct) / 2, 100 - (100 - confidence_pct) / 2

    t1_med, t1_lo, t1_hi = np.median(t1_cum, axis=0), np.percentile(t1_cum, lo, axis=0), np.percentile(t1_cum, hi, axis=0)
    t2_med, t2_lo, t2_hi = np.median(t2_cum, axis=0), np.percentile(t2_cum, lo, axis=0), np.percentile(t2_cum, hi, axis=0)

    fig = go.Figure()
    # Team 1 band + line
    fig.add_trace(go.Scatter(x=possessions, y=t1_hi, mode="lines", line=dict(width=0), showlegend=False, hoverinfo="skip"))
    fig.add_trace(go.Scatter(x=possessions, y=t1_lo, mode="lines", line=dict(width=0), fill="tonexty", fillcolor=f"rgba({t1_rgb},0.15)", showlegend=False, hoverinfo="skip"))
    fig.add_trace(go.Scatter(x=possessions, y=t1_med, mode="lines", name=t1_name, line=dict(color=t1_color, width=3)))
    # Team 2 band + line
    fig.add_trace(go.Scatter(x=possessions, y=t2_hi, mode="lines", line=dict(width=0), showlegend=False, hoverinfo="skip"))
    fig.add_trace(go.Scatter(x=possessions, y=t2_lo, mode="lines", line=dict(width=0), fill="tonexty", fillcolor=f"rgba({t2_rgb},0.15)", showlegend=False, hoverinfo="skip"))
    fig.add_trace(go.Scatter(x=possessions, y=t2_med, mode="lines", name=t2_name, line=dict(color=t2_color, width=3)))
    fig.add_vline(x=35, line_dash="dash", line_color="gray", annotation_text="Halftime")

    t1_final, t2_final = t1_cum[:, -1], t2_cum[:, -1]
    t1_wins = (t1_final > t2_final).sum()
    ties = n_sims - t1_wins - (t2_final > t1_final).sum()
    t1_wp = (t1_wins + ties * 0.5) / n_sims * 100
    t2_wp = 100 - t1_wp

    fig.add_annotation(x=n_poss, y=max(t1_med[-1], t2_med[-1]) + 5,
                       text=f"Win prob: {t1_name.split()[0]} {t1_wp:.0f}% — {t2_name.split()[0]} {t2_wp:.0f}%",
                       showarrow=False, font=dict(size=13, color="black"), bgcolor="rgba(255,255,255,0.8)")
    fig.update_layout(xaxis_title="Possession", yaxis_title="Cumulative Score", legend=dict(x=0.01, y=0.99), margin=dict(t=30, b=40), height=450, hovermode="x unified")
    return fig, t1_wp, t2_wp, np.median(t1_final), np.median(t2_final)


# ═══════════════════════════════════════════════════════════════════════════
# STREAMLIT UI
# ═══════════════════════════════════════════════════════════════════════════

st.set_page_config(page_title="Lineup Analyzer", layout="wide")

st.title("🏀 College Basketball — Lineup Matchup Analyzer")
st.caption("2025-26 Season  |  Choose a game, select a starting five, and get the optimal counter-lineup")

# ---- Game selector ----
game_names = list(GAMES.keys())
selected_game = st.selectbox("Choose a game to analyze:", game_names, key="game_select")
G = GAMES[selected_game]

# ---- Team side selector ----
pick_team = st.radio(
    "Which team's starting five do you want to pick?",
    [G["team1_short"], G["team2_short"]],
    horizontal=True,
    key=f"side_{selected_game}",
)

# Assign pick/opp based on selection — "pick" = user-selected team, "opp" = counter team
if pick_team == G["team1_short"]:
    PICK_NAME, OPP_NAME = G["team1_name"], G["team2_name"]
    PICK_SHORT, OPP_SHORT = G["team1_short"], G["team2_short"]
    PICK_COLOR, OPP_COLOR = G["team1_color"], G["team2_color"]
    PICK_RGB, OPP_RGB = G["team1_color_rgb"], G["team2_color_rgb"]
    PICK_PLAYERS, OPP_PLAYERS = G["team1_players"], G["team2_players"]
else:
    PICK_NAME, OPP_NAME = G["team2_name"], G["team1_name"]
    PICK_SHORT, OPP_SHORT = G["team2_short"], G["team1_short"]
    PICK_COLOR, OPP_COLOR = G["team2_color"], G["team1_color"]
    PICK_RGB, OPP_RGB = G["team2_color_rgb"], G["team1_color_rgb"]
    PICK_PLAYERS, OPP_PLAYERS = G["team2_players"], G["team1_players"]

# ---- Predicted outcome bar chart (if results exist for this game+side) ----
state_key = f"results_{selected_game}_{pick_team}"
if state_key in st.session_state and st.session_state[state_key]:
    st.subheader("Predicted Outcome")
    outcome_fig = build_predicted_outcome_chart(st.session_state[state_key], PICK_NAME, OPP_NAME, PICK_SHORT, OPP_SHORT, PICK_COLOR, OPP_COLOR)
    st.plotly_chart(outcome_fig, use_container_width=True)

st.divider()

# ---- Pick-team Roster overview ----
with st.expander(f"📋 Full {PICK_NAME} Roster & Stats", expanded=False):
    rows = []
    for name, p in PICK_PLAYERS.items():
        rows.append({"#": p["number"], "Player": name, "Pos": p["pos"], "Ht": p["height"], "Class": p["class"],
                      "GP": p["gp"], "PPG": p["pts"], "RPG": p["reb"], "APG": p["ast"], "FG%": p["fg_pct"], "3P%": p["three_pct"]})
    st.dataframe(pd.DataFrame(rows).sort_values("PPG", ascending=False), use_container_width=True, hide_index=True)

# ---- Selection ----
st.subheader(f"Select Your {PICK_SHORT} Starting Five")

player_options = [f"{name}  ({p['pos']}, {p['pts']:.1f} PPG)" for name, p in sorted(PICK_PLAYERS.items(), key=lambda x: -x[1]["pts"])]
name_lookup = {f"{name}  ({p['pos']}, {p['pts']:.1f} PPG)": name for name, p in PICK_PLAYERS.items()}

selected_labels = st.multiselect("Choose up to 5 players:", options=player_options, max_selections=5, placeholder=f"Pick your {PICK_SHORT} lineup...", key=f"select_{selected_game}_{pick_team}")
selected_names = [name_lookup[label] for label in selected_labels]

if selected_names:
    st.markdown(f"**Your {PICK_SHORT} Selections:**")
    sel_rows = []
    for name in selected_names:
        p = PICK_PLAYERS[name]
        sel_rows.append({"#": p["number"], "Player": name, "Pos": p["pos"], "Ht": p["height"],
                          "PPG": p["pts"], "RPG": p["reb"], "APG": p["ast"], "STL": p["stl"], "BLK": p["blk"], "FG%": p["fg_pct"]})
    st.dataframe(pd.DataFrame(sel_rows), use_container_width=True, hide_index=True)

st.divider()

# ---- Generate matchup ----
if st.button(f"🔍 Generate {OPP_SHORT} Counter-Lineup", type="primary", disabled=len(selected_names) == 0):
    results = find_best_lineup(selected_names, PICK_PLAYERS, OPP_PLAYERS)
    st.session_state[state_key] = results

    st.subheader(f"Suggested {OPP_NAME} Lineup")

    for i, r in enumerate(results):
        col1, col2, col3 = st.columns([2, 1, 2])
        with col1:
            st.markdown(f"**#{r['t1']['number']} {r['t1_name']}** ({PICK_SHORT})")
            st.caption(f"{r['t1']['pos']} | {r['t1']['height']} | {r['t1']['class']}")
            st.metric("PPG", f"{r['t1']['pts']:.1f}")
            st.caption(f"{r['t1']['reb']:.1f} RPG · {r['t1']['ast']:.1f} APG · {r['t1']['stl']:.1f} STL · {r['t1']['blk']:.1f} BLK")
        with col2:
            st.markdown("<div style='text-align:center; padding-top:30px; font-size:2em;'>⚔️</div>", unsafe_allow_html=True)
        with col3:
            st.markdown(f"**#{r['t2']['number']} {r['t2_name']}** ({OPP_SHORT})")
            st.caption(f"{r['t2']['pos']} | {r['t2']['height']} | {r['t2']['class']}")
            st.metric("PPG", f"{r['t2']['pts']:.1f}")
            st.caption(f"{r['t2']['reb']:.1f} RPG · {r['t2']['ast']:.1f} APG · {r['t2']['stl']:.1f} STL · {r['t2']['blk']:.1f} BLK")
        st.info(f"**Why this matchup:** {r['reason']}")
        if i < len(results) - 1:
            st.divider()

    # ---- Summary table ----
    st.divider()
    st.subheader("Matchup Summary")
    summary_rows = []
    for r in results:
        summary_rows.append({
            f"{PICK_SHORT} Player": r["t1_name"], f"{PICK_SHORT} Pos": r["t1"]["pos"], f"{PICK_SHORT} PPG": r["t1"]["pts"],
            "": "vs",
            f"{OPP_SHORT} Player": r["t2_name"], f"{OPP_SHORT} Pos": r["t2"]["pos"], f"{OPP_SHORT} PPG": r["t2"]["pts"],
            "Matchup Score": f"{r['score']:.1f}",
        })
    st.dataframe(pd.DataFrame(summary_rows), use_container_width=True, hide_index=True)

    # ---- Team comparison metrics ----
    pick_total_pts = sum(PICK_PLAYERS[n]["pts"] for n in selected_names)
    opp_total_pts = sum(r["t2"]["pts"] for r in results)
    pick_total_reb = sum(PICK_PLAYERS[n]["reb"] for n in selected_names)
    opp_total_reb = sum(r["t2"]["reb"] for r in results)
    st.subheader("Lineup Comparison")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric(f"{PICK_SHORT} Combined PPG", f"{pick_total_pts:.1f}")
    c2.metric(f"{OPP_SHORT} Combined PPG", f"{opp_total_pts:.1f}")
    c3.metric(f"{PICK_SHORT} Combined RPG", f"{pick_total_reb:.1f}")
    c4.metric(f"{OPP_SHORT} Combined RPG", f"{opp_total_reb:.1f}")

    # ---- Spider / Radar charts ----
    st.divider()
    st.subheader("Team Radar Comparison")
    pick_lineup = [PICK_PLAYERS[n] for n in selected_names]
    opp_lineup = [r["t2"] for r in results]
    radar_fig = build_radar_chart(pick_lineup, opp_lineup, PICK_NAME, OPP_NAME, PICK_COLOR, PICK_RGB, OPP_COLOR, OPP_RGB)
    st.plotly_chart(radar_fig, use_container_width=True)

    col_r1, col_r2 = st.columns(2)
    with col_r1:
        st.markdown(f"**{PICK_NAME}**")
        solo1 = go.Figure()
        vals1 = _team_radar_values(pick_lineup)
        solo1.add_trace(go.Scatterpolar(r=vals1 + [vals1[0]], theta=RADAR_CATEGORIES + [RADAR_CATEGORIES[0]], fill="toself", name=PICK_SHORT, line_color=PICK_COLOR, fillcolor=f"rgba({PICK_RGB},0.3)"))
        solo1.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=False, margin=dict(t=20, b=20, l=40, r=40), height=350)
        st.plotly_chart(solo1, use_container_width=True)
    with col_r2:
        st.markdown(f"**{OPP_NAME}**")
        solo2 = go.Figure()
        vals2 = _team_radar_values(opp_lineup)
        solo2.add_trace(go.Scatterpolar(r=vals2 + [vals2[0]], theta=RADAR_CATEGORIES + [RADAR_CATEGORIES[0]], fill="toself", name=OPP_SHORT, line_color=OPP_COLOR, fillcolor=f"rgba({OPP_RGB},0.3)"))
        solo2.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=False, margin=dict(t=20, b=20, l=40, r=40), height=350)
        st.plotly_chart(solo2, use_container_width=True)

    # ---- Game simulation ----
    st.divider()
    st.subheader("Game Simulation")
    st.caption("Monte Carlo simulation: each possession scored from a normal distribution based on lineup stats. Adjust confidence to widen/narrow the band.")
    confidence = st.slider("Confidence interval (%)", min_value=50, max_value=99, value=90, step=5, key=f"sim_conf_{selected_game}_{pick_team}")
    sim_fig, pick_wp, opp_wp, pick_med_score, opp_med_score = simulate_game(pick_lineup, opp_lineup, PICK_NAME, OPP_NAME, PICK_COLOR, PICK_RGB, OPP_COLOR, OPP_RGB, confidence_pct=confidence)
    st.plotly_chart(sim_fig, use_container_width=True)
    sc1, sc2, sc3, sc4 = st.columns(4)
    sc1.metric(f"{PICK_SHORT} Win Prob", f"{pick_wp:.0f}%")
    sc2.metric(f"{OPP_SHORT} Win Prob", f"{opp_wp:.0f}%")
    sc3.metric(f"{PICK_SHORT} Median Score", f"{pick_med_score:.0f}")
    sc4.metric(f"{OPP_SHORT} Median Score", f"{opp_med_score:.0f}")

    # ---- 5×5 Matchup strength heatmap ----
    st.divider()
    st.subheader("Matchup Strength Matrix")
    st.caption(f"{PICK_SHORT} color = {PICK_SHORT} advantage, {OPP_SHORT} color = {OPP_SHORT} advantage. Each row is a head-to-head matchup across six dimensions.")
    matrix_fig = build_matchup_matrix(results, PICK_SHORT, OPP_SHORT, PICK_COLOR, OPP_COLOR)
    st.plotly_chart(matrix_fig, use_container_width=True)

    # ---- Bench recommendation ----
    st.divider()
    st.subheader(f"First Off the Bench — {OPP_SHORT}")
    st.caption(f"{OPP_SHORT} bench players ranked by potential impact. Star rating reflects scoring, defense, rebounding, positional need, and ability to improve the weakest matchup.")
    opp_starter_names = [r["t2_name"] for r in results]
    bench = rank_bench_options(opp_starter_names, results, OPP_PLAYERS, is_team2=True)
    if bench:
        top = bench[0]
        st.success(f"**Recommended:** #{top['player']['number']} {top['name']}  ({top['player']['pos']}, {top['player']['class']})  —  {stars_display(top['stars'])}  \n_{top['reason']}_")
        bench_rows = []
        for b in bench:
            p = b["player"]
            bench_rows.append({"#": p["number"], "Player": b["name"], "Pos": p["pos"], "Class": p["class"],
                               "Rating": stars_display(b["stars"]), "PPG": p["pts"], "RPG": p["reb"], "APG": p["ast"],
                               "STL": p["stl"], "BLK": p["blk"], "Sub For": b["replace_for"] or "—", "Rationale": b["reason"]})
        st.dataframe(pd.DataFrame(bench_rows), use_container_width=True, hide_index=True)
    else:
        st.warning("No bench players available with game experience.")

elif len(selected_names) == 0:
    st.info(f"Select 1–5 {PICK_SHORT} players above, then click **Generate {OPP_SHORT} Counter-Lineup**.")

# ---- Opponent roster reference ----
with st.expander(f"📋 Full {OPP_NAME} Roster & Stats", expanded=False):
    opp_rows = []
    for name, p in OPP_PLAYERS.items():
        opp_rows.append({"#": p["number"], "Player": name, "Pos": p["pos"], "Ht": p["height"], "Class": p["class"],
                         "GP": p["gp"], "PPG": p["pts"], "RPG": p["reb"], "APG": p["ast"], "FG%": p["fg_pct"], "3P%": p["three_pct"]})
    st.dataframe(pd.DataFrame(opp_rows).sort_values("PPG", ascending=False), use_container_width=True, hide_index=True)
