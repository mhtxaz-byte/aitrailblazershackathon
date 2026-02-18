# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Mission

Advise the coach to get more wins. Build a multi-agent system for college basketball lineup analysis, focused on BYU Cougars vs Arizona Wildcats matchups.

## Agent Roles

- **Developer Agent**: professional software developer
- **Marketing Agent**: master marketer
- **Analytics Agent**: sports analyst focused on college basketball
- **Data Science Agent**: PhD statistician, software developer, and sports gambler
- **Basketball Coach Agent**: vets lineup and five-player combinations to maximize win probability

## Core Feature

A front end where a user selects up to 5 players from the BYU Cougars roster. Based on that selection, the system suggests an optimal opposing lineup from the Arizona Wildcats roster.

### Data Sources (ESPN)

- BYU Cougars — roster: `/team/roster/_/id/252`, stats: `/team/stats/_/id/252`, general: `/team/_/id/252`
- Arizona Wildcats — roster: `/team/roster/_/id/12`, stats: `/team/stats/_/id/12`, general: `/team/_/id/12`

(All under `https://www.espn.com/mens-college-basketball/`)

## Architecture

Single-file Streamlit app (`app.py`) with embedded 2025-26 season data from ESPN.

- **Data layer**: BYU and Arizona player dictionaries at the top of `app.py` with roster info + per-game stats (PPG, RPG, APG, STL, BLK, FG%, 3P%, FT%)
- **Matchup engine**: `find_best_lineup()` uses greedy assignment — scores each Arizona player against each BYU player via `matchup_score()` (weighted: position compatibility, size, scoring, defense, rebounding, minutes), then assigns best available
- **UI**: Streamlit multiselect (max 5) → Generate button → side-by-side matchup cards with stats and explanations

## Environment

- Python 3.9 virtual environment in `apenv/`
- Activate: `source apenv/bin/activate`
- Run app: `streamlit run app.py`
- Install deps: `pip install -r requirements.txt`
