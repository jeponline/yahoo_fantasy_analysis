from yahoo_oauth import OAuth2
import yahoo_fantasy_api as yfa
import pandas as pd
from flask import current_app
import os
import json
import logging

logger = logging.getLogger(__name__)

def get_oauth():
    """Get OAuth2 object for Yahoo Fantasy API."""
    credentials_file = current_app.config['CREDENTIALS_FILE']
    try:
        oauth = OAuth2(None, None, from_file=credentials_file)
        if not oauth.token_is_valid():
            oauth.refresh_access_token()
        return oauth
    except Exception as e:
        logger.error(f"OAuth initialization error: {e}")
        return None

def check_auth_status():
    """Check if authentication with Yahoo Fantasy API is working."""
    try:
        oauth = get_oauth()
        if oauth and oauth.token_is_valid():
            return True
        return False
    except Exception:
        return False

def get_game():
    """Get Yahoo Fantasy API game object."""
    oauth = get_oauth()
    if not oauth:
        return None
    return yfa.Game(oauth, 'mlb')

def get_leagues(year=2025):
    """Get leagues for the specified year."""
    game = get_game()
    if not game:
        return []
    
    try:
        return game.league_ids(year=year)
    except Exception as e:
        logger.error(f"Error getting leagues: {e}")
        return []

def get_league(league_id):
    """Get league object for specified league ID."""
    game = get_game()
    if not game:
        return None
    
    try:
        return game.to_league(league_id)
    except Exception as e:
        logger.error(f"Error getting league: {e}")
        return None

def get_team(team_key):
    """Get team object for specified team key."""
    league_id = '.'.join(team_key.split('.')[:3])
    league = get_league(league_id)
    if not league:
        return None
    
    try:
        return league.to_team(team_key)
    except Exception as e:
        logger.error(f"Error getting team: {e}")
        return None

def get_roster(team_key):
    """Get roster for specified team."""
    team = get_team(team_key)
    if not team:
        return []
    
    try:
        roster_data = team.roster()
        return pd.DataFrame(roster_data).to_dict('records')
    except Exception as e:
        logger.error(f"Error getting roster: {e}")
        return []

def get_league_standings(league_id):
    """Get standings for specified league."""
    league = get_league(league_id)
    if not league:
        return []
    
    try:
        standings = league.standings()
        return standings
    except Exception as e:
        logger.error(f"Error getting standings: {e}")
        return []

def get_league_teams(league_id):
    """Get teams for specified league."""
    league = get_league(league_id)
    if not league:
        return []
    
    try:
        teams = league.teams()
        return teams
    except Exception as e:
        logger.error(f"Error getting teams: {e}")
        return []

def get_league_settings(league_id):
    """Get settings for specified league."""
    league = get_league(league_id)
    if not league:
        return {}
    
    try:
        settings = league.settings()
        return settings
    except Exception as e:
        logger.error(f"Error getting settings: {e}")
        return {}