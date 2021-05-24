import requests
import json
import chess.pgn
import io
import pandas as pd
import math


username = ""
year = ""
month = ""

def get_data_by_month(username, year, month):
    """
    Returns a dataframe with all games played for the given 
    month/year. 
    
    
    """
    url = f"https://api.chess.com/pub/player/{username}/games/{year}/{month}"
    print(url)
    data = requests.get(url)
    if data.status_code != 200:
        raise Exception("The following response was returned: " + str(data.status_code))
    else:
        data = json.loads(data.text)
        games = data["games"]
    
    
    all_games=[]
    for game in games:
        pgn = (game['pgn'])
        pgn = io.StringIO(pgn)
        game = chess.pgn.read_game(pgn)
        all_games.append(game)
        
        
    game_list = []
    for g in all_games:
        moves = (g.mainline_moves())
        moves = [str(x) for x in moves]
        
        white = (g.headers['White'])
        if white.lower() == username.lower():
            is_white = 1
        else:
            is_white = 0
        
        
        game = {"Date": (g.headers["Date"]), "Player_white": white, "Player_black": (g.headers['Black']), "Playing_as_white" : is_white, "Result": (g.headers['Result']), "Termination": (g.headers['Termination']), "Moves": moves, "No_of_moves": (math.ceil(len(moves)/2)), "First_move": (moves[0]), "Response": (moves[1])}
        game_list.append(game)
    game_list = pd.DataFrame(game_list)
    return game_list

        