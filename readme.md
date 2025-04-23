# Yahoo Fantasy Baseball Data Tracker

A Flask application to retrieve, store, and visualize Yahoo Fantasy Baseball data. This application allows you to:

- Connect to the Yahoo Fantasy API using OAuth
- Retrieve fantasy baseball data (leagues, teams, rosters, standings, etc.)
- Store data locally for offline analysis
- Schedule automatic data updates
- View data through a web interface

## Setup

### Prerequisites

- Python 3.8 or higher
- Yahoo Developer account and API credentials

### Installation

1. Clone this repository
   ```
   git clone https://github.com/yourusername/fantasy-baseball-tracker.git
   cd fantasy-baseball-tracker
   ```

2. Create a virtual environment and activate it
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```
   pip install -r requirements.txt
   ```

4. Create Yahoo OAuth credentials
   - Go to [Yahoo Developer Network](https://developer.yahoo.com/apps/create/)
   - Create a new application
   - Set Application Name (e.g., "Fantasy Baseball Tracker")
   - Select "Installed Application" as Application Type
   - Set Callback Domain to "localhost"
   - Select API Permissions: "Fantasy Sports"

5. Create OAuth configuration file
   - Create a file named `oauth2.json` in the `config` directory
   - Add your credentials:
     ```json
     {
       "consumer_key": "YOUR_CONSUMER_KEY",
       "consumer_secret": "YOUR_CONSUMER_SECRET"
     }
     ```

### Running the Application

Start the Flask development server:
```
python run.py
```

Navigate to `http://localhost:5000` in your web browser.

The first time you run the application, you'll be guided through the OAuth authorization process with Yahoo.

## Configuration

Edit `config/config.py` to customize:

- Data refresh interval
- Storage location
- Other application settings

## Data Storage

Data is stored in JSON format in the `data` directory. Each type of data (leagues, teams, rosters, etc.) is stored in a separate file with timestamps.

## Scheduling

The application uses Flask-APScheduler to run periodic data refresh tasks. You can configure the schedule in:

- `config/config.py` - Default schedule configuration
- Web interface (Settings page) - Runtime schedule adjustments

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Yahoo Fantasy API](https://developer.yahoo.com/fantasysports/guide/)
- [yahoo_fantasy_api](https://github.com/spilchen/yahoo_fantasy_api) Python library
- Flask and its extensions