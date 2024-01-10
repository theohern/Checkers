import checkers
import matplotlib.pyplot as plt
from keras.models import load_model
import tensorflow as tfw
import numpy as np
import random


Random = load_model("models/random.keras")
Minmax = load_model("models/minmax.keras")
Itself = load_model("models/itself.keras")


def playRandomMinMax(Bot1="random", Bot2="random", verbose=False):
    end2 = 0
    game = checkers.Checkers()
    if verbose : game.Show()
    player = -1
    NumberOfMoves = 0
    while True :
        player = -player
        if (player == 1):
            a = game.CopyBoard()
            moves = game.GetValidMoves(player, Filter=True)
            if len(moves) == 0 : 
                if verbose : print(f"player {player} lose")
                return -player
            if Bot1 == "random" : move = random.choice(moves)
            elif Bot1 == "minmax" : move = random.choice(game.minmax(1))
            elif Bot1 == "Trandom" : 
                leafs = game.minmax(player, RL=True) # move | score | features
                Leaf = tfw.zeros((len(leafs), 5))
                for l in range(len(leafs)) :
                    tensor = leafs[l][2]
                    Leaf = tfw.tensor_scatter_nd_update(Leaf, [[l]], [tensor[:5]])
                scores = Random.predict_on_batch(Leaf)
                if (len(scores) == 0):
                    end2 = -player
                i = np.argmax(scores)
                move = leafs[i][0]
            elif Bot1 == "Tminmax":  
                leafs = game.minmax(player, RL=True) 
                Leaf = tfw.zeros((len(leafs), 5))
                for l in range(len(leafs)) :
                    tensor = leafs[l][2]
                    Leaf = tfw.tensor_scatter_nd_update(Leaf, [[l]], [tensor[:5]])
                scores = Minmax.predict_on_batch(Leaf)
                if (len(scores) == 0):
                    end2 = -player
                i = np.argmax(scores)
                move = leafs[i][0]
            elif Bot1 == "Titself":  
                leafs = game.minmax(player, RL=True) 
                Leaf = tfw.zeros((len(leafs), 5))
                for l in range(len(leafs)) :
                    tensor = leafs[l][2]
                    Leaf = tfw.tensor_scatter_nd_update(Leaf, [[l]], [tensor[:5]])
                scores = Itself.predict_on_batch(Leaf)
                if (len(scores) == 0):
                    end2 = -player
                i = np.argmax(scores)
                move = leafs[i][0]
            else : raise(f"Do not know the type of bot {Bot1}")
            game.PushMove(move)
            if game.CompareBoard(a, game.board) :
                print(f"move did not play {move}")
                print(game.board)
                break
            if verbose :
                print(move)
                game.GetScore(verbose=True)
                game.GetFeatures(player, verbose=True)
                game.Show()
            end = game.EndGame()
            if (end == 1 or end2 == 1) :
                if verbose : print("white win")
                return 1
            elif (end == -1 or end2 == -1) : 
                if verbose : print("black win")
                return -1
        elif player == -1:
            a = game.CopyBoard()
            moves = game.GetValidMoves(player, Filter=True)
            if len(moves) == 0 : 
                if verbose : print(f"player {player} lose")
                return -player
            if Bot2 == "random" : move = random.choice(moves)
            elif Bot2 == "minmax" : move = random.choice(game.minmax(-1))
            elif Bot2 == "Trandom" : 
                leafs = game.minmax(player, RL=True) # move | score | features
                Leaf = tfw.zeros((len(leafs), 5))
                for l in range(len(leafs)) :
                    tensor = leafs[l][2]
                    Leaf = tfw.tensor_scatter_nd_update(Leaf, [[l]], [tensor[:5]])
                scores = Random.predict_on_batch(Leaf)
                if (len(scores) == 0):
                    end2 = -player
                i = np.argmax(scores)
                move = leafs[i][0]
            elif Bot2 == "Tminmax": 
                leafs = game.minmax(player, RL=True) 
                Leaf = tfw.zeros((len(leafs), 5))
                for l in range(len(leafs)) :
                    tensor = leafs[l][2]
                    Leaf = tfw.tensor_scatter_nd_update(Leaf, [[l]], [tensor[:5]])
                scores = Minmax.predict_on_batch(Leaf)
                if (len(scores) == 0):
                    end2 = -player
                i = np.argmax(scores)
                move = leafs[i][0]
            elif Bot2 == "Titself": 
                leafs = game.minmax(player, RL=True) 
                Leaf = tfw.zeros((len(leafs), 5))
                for l in range(len(leafs)) :
                    tensor = leafs[l][2]
                    Leaf = tfw.tensor_scatter_nd_update(Leaf, [[l]], [tensor[:5]])
                scores = Itself.predict_on_batch(Leaf)
                if (len(scores) == 0):
                    end2 = -player
                i = np.argmax(scores)
                move = leafs[i][0]
            else : raise(f"Do not know the type of bot {Bot2}")
            game.PushMove(move)
            if game.CompareBoard(a, game.board) :
                print(f"move did not play {move}")
                print(game.board)
                break
            if verbose :
                print(move)
                game.GetScore(verbose=True)
                game.GetFeatures(player, verbose=True)
                game.Show()
            end = game.EndGame()
            if (end == 1 or end2 == 1) :
                if verbose : print("white win")
                return 1
            elif (end == -1 or end2 == -1) : 
                if verbose : print("black win")
                return -1    
        NumberOfMoves += 2   
        if (NumberOfMoves > 300):
            return 0   

def CompareBots(player1, player2, NumberPlays):
    black = 0
    white = 0
    draw = 0
    for i in range(NumberPlays):
        if i % (NumberPlays/10) == ((NumberPlays/10) -1) : print(f"[{i+1}/{NumberPlays}]%")
        ret = playRandomMinMax(Bot1=player1, Bot2=player2, verbose=False)
        if ret == 1 : white += 1
        elif ret == -1 : black += 1
        elif ret == 0 : draw+=1
        else : raise (f"Problem with return value of function Compare2Bots, get {ret}")

    black_percent = (black / NumberPlays) * 100
    white_percent = (white / NumberPlays) * 100
    draw_percent = (draw / NumberPlays) * 100

    labels = 'Black', 'White', 'Draw'
    sizes = [black_percent, white_percent, draw_percent]
    colors = ['lightcoral', 'lightskyblue', 'green']

    plt.figure(figsize=(8, 6))
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')  # Assure que le graphique est un cercle
    plt.title(player1 + '(White) against ' + player2 +' (Black)')
    plt.show()

if "__main__" == __name__ :
    player1 = "Trandom"
    player2 = "Trandom"
    print(player1, player2)
    CompareBots(player1=player1, player2=player2, NumberPlays=100)
    print(player1, player2)