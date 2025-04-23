from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from datetime import datetime

@dataclass
class Player:
    """Class for storing player data."""
    player_id: str
    name: str
    position: str
    team: str
    status: Optional[str] = None
    
    @classmethod
    def from_api(cls, data: Dict[str, Any]) -> 'Player':
        """Create Player instance from API data."""
        return cls(
            player_id=str(data.get('player_id')),
            name=data.get('name', {}).get('full', ''),
            position=data.get('primary_position', ''),
            team=data.get('editorial_team_abbr', ''),
            status=data.get('status', '')
        )

@dataclass
class Team:
    """Class for storing team data."""
    team_key: str
    name: str
    manager: str
    logo_url: Optional[str] = None
    roster: Optional[List[Player]] = None
    
    @classmethod
    def from_api(cls, data: Dict[str, Any]) -> 'Team':
        """Create Team instance from API data."""
        return cls(
            team_key=data.get('team_key', ''),
            name=data.get('name', ''),
            manager=data.get('managers', {}).get('manager', {}).get('nickname', ''),
            logo_url=data.get('team_logos', {}).get('team_logo', {}).get('url', '')
        )

@dataclass
class League:
    """Class for storing league data."""
    league_id: str
    name: str
    num_teams: int
    teams: Optional[List[Team]] = None
    settings: Optional[Dict[str, Any]] = None
    
    @classmethod
    def from_api(cls, data: Dict[str, Any]) -> 'League':
        """Create League instance from API data."""
        return cls(
            league_id=data.get('league_key', ''),
            name=data.get('name', ''),
            num_teams=data.get('num_teams', 0)
        )

@dataclass
class DataSnapshot:
    """Class for storing a snapshot of data."""
    timestamp: datetime
    leagues: List[League]
    
    @classmethod
    def create_snapshot(cls, leagues_data: List[Dict[str, Any]]) -> 'DataSnapshot':
        """Create a snapshot from the current data."""
        leagues = [League.from_api(data) for data in leagues_data]
        return cls(
            timestamp=datetime.now(),
            leagues=leagues
        )
