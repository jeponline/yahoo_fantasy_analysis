import os
import json
import pandas as pd
from datetime import datetime
from flask import current_app
import logging
from app.services.yahoo_api_service import (
    get_leagues, get_league_standings, get_league_teams,
    get_league_settings, get_roster
)

logger = logging.getLogger(__name__)

DATA_TYPES = {
    'leagues': get_leagues,
    'standings': lambda: _get_all_leagues_data(get_league_standings),
    'teams': lambda: _get_all_leagues_data(get_league_teams),
    'settings': lambda: _get_all_leagues_data(get_league_settings),
    'roster': lambda: _get_all_teams_data(get_roster)
}

def _get_all_leagues_data(func):
    """Get data for all leagues using the provided function."""
    result = {}
    leagues = get_leagues()
    
    for league_id in leagues:
        try:
            data = func(league_id)
            result[league_id] = data
        except Exception as e:
            logger.error(f"Error getting data for league {league_id}: {e}")
    
    return result

def _get_all_teams_data(func):
    """Get data for all teams using the provided function."""
    result = {}
    leagues = get_leagues()
    
    for league_id in leagues:
        try:
            from app.services.yahoo_api_service import get_league_teams
            teams = get_league_teams(league_id)
            
            for team_key in teams:
                try:
                    data = func(team_key)
                    result[team_key] = data
                except Exception as e:
                    logger.error(f"Error getting data for team {team_key}: {e}")
        except Exception as e:
            logger.error(f"Error getting teams for league {league_id}: {e}")
    
    return result

def get_data_file_path(data_type):
    """Get file path for storing/retrieving data."""
    data_dir = current_app.config['DATA_DIR']
    return os.path.join(data_dir, f"{data_type}.json")

def save_data(data_type, data):
    """Save data to JSON file."""
    try:
        file_path = get_data_file_path(data_type)
        
        # Add timestamp
        data_with_meta = {
            'timestamp': datetime.now().isoformat(),
            'data': data
        }
        
        with open(file_path, 'w') as f:
            json.dump(data_with_meta, f, indent=2)
        
        logger.info(f"Saved {data_type} data to {file_path}")
        return True
    except Exception as e:
        logger.error(f"Error saving {data_type} data: {e}")
        return False

def load_data(data_type):
    """Load data from JSON file."""
    try:
        file_path = get_data_file_path(data_type)
        
        if not os.path.exists(file_path):
            return None
        
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading {data_type} data: {e}")
        return None

def get_stored_data(data_type):
    """Get stored data of specified type."""
    if data_type not in DATA_TYPES:
        return {'error': f"Unknown data type: {data_type}"}
    
    data = load_data(data_type)
    if not data:
        # If data doesn't exist, try to fetch it
        refresh_data(data_type)
        data = load_data(data_type)
    
    return data or {'error': f"No data available for {data_type}"}

def refresh_data(data_type):
    """Refresh data of specified type."""
    if data_type not in DATA_TYPES:
        logger.error(f"Unknown data type: {data_type}")
        return False
    
    try:
        data_func = DATA_TYPES[data_type]
        data = data_func()
        save_data(data_type, data)
        return True
    except Exception as e:
        logger.error(f"Error refreshing {data_type} data: {e}")
        return False

def refresh_all_data(specific_type=None):
    """Refresh all data or a specific type."""
    if specific_type:
        return refresh_data(specific_type)
    
    success = True
    for data_type in DATA_TYPES:
        if not refresh_data(data_type):
            success = False
    
    return success

def get_available_data_types():
    """Get list of available data types."""
    return list(DATA_TYPES.keys())
