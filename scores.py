import requests
import pandas as pd
import time

print(r"""
 _      ____  __ __    ___      ____   __ __  _           _____   __   ___   ____     ___  _____
| |    |    ||  |  |  /  _]    |    \ |  |  || |         / ___/  /  ] /   \ |    \   /  _]/ ___/
| |     |  | |  |  | /  [_     |  _  ||  |  || |        (   \_  /  / |     ||  D  ) /  [_(   \_ 
| |___  |  | |  |  ||    _]    |  |  ||  _  || |___      \__  |/  /  |  O  ||    / |    _]\__  |
|     | |  | |  :  ||   [_     |  |  ||  |  ||     |     /  \ /   \_ |     ||    \ |   [_ /  \ |
|     | |  |  \   / |     |    |  |  ||  |  ||     |     \    \     ||     ||  .  \|     |\    |
|_____||____|  \_/  |_____|    |__|__||__|__||_____|      \___|\____| \___/ |__|\_||_____| \___|
                                                                                                           
      LIVE NHL SCORES  https://github.com/Q0LT
      Usage: Ctrl+C to stop the program.
    """)

api = "https://api-web.nhle.com/v1/score/now"

while True:
    response = requests.get(api)
    
    if response.status_code == 200:
        data = response.json()

        if 'games' in data:
            games = data['games']
            if len(games) > 0:
                game_info = []
                
                for game in games:
                    game_date = game['gameDate']
                    away_team = game['awayTeam']['abbrev']
                    home_team = game['homeTeam']['abbrev']
                    
                    if 'score' in game['awayTeam']:
                          away_score = game['awayTeam']['score']
                    else:
                          away_score = None
 
                    if 'score' in game['homeTeam']:
                          home_score = game['homeTeam']['score']
                    else:
                        home_score = None
                    
                    if 'clock' in game:
                        clock = game['clock']['timeRemaining']
                    else:
                        clock = None

                    networks = [broadcast['network'] for broadcast in game['tvBroadcasts']]
                    
                    networks_str = ', '.join(networks)

                    game_info.append([game_date, away_team, home_team, away_score, home_score, clock, networks_str])
                
                df = pd.DataFrame(game_info, columns=['Game Date', 'Away Team', 'Home Team', 'Away Score', 'Home Score', 'Clock', 'Networks'])
                print(df)
            else:
                print("No games found in the API response")
        else:
            print("No 'games' key found in the API response")
    else:
        print("Error fetching data")
    time.sleep(60)
