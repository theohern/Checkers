import checkers
import matplotlib.pyplot as plt
from keras import Sequential, regularizers
from keras.layers import Dense
import tensorflow as tfw
import numpy as np
import random
from tqdm import tqdm

def concatenate(array1, array2):
    for i in range(len(array2)):
        array1.append(array2[i])
    return array1  

def GetModel(Oppenent):
    model = Sequential()
    model.add(Dense(32, activation='relu', input_dim=5)) 
    model.add(Dense(16, activation='relu',  kernel_regularizer=regularizers.l2(0.1)))

    model.add(Dense(1, activation='relu',  kernel_regularizer=regularizers.l2(0.1)))
    model.compile(optimizer='nadam', loss='binary_crossentropy', metrics=["acc"])

    data = [] 
    labels = np.zeros(1)
    winrates = []
    learning_rate = 0.5
    discount_factor = 0.95
    exploration = 0.95
    win = 0
    lose = 0
    draw = 0

    for generations in tqdm(range(500)):
        data = []
        for g in range(10):
            temp_data = []
            game = checkers.Checkers()
            player = 1
            count = 0
            while True:
                count += 1
                end2 = 0
                if count > 1000 :
                    draw += 1
                    break

                else :
                    if (player == 1) : 
                        leafs = game.minmax(player, RL=True)
                        Leaf = tfw.zeros((len(leafs), 5))
                        for l in range(len(leafs)) :
                            tensor = leafs[l][2]
                            Leaf = tfw.tensor_scatter_nd_update(Leaf, [[l]], [tensor[:5]])
                        scores = model.predict_on_batch(Leaf)
                        if (len(scores) == 0):
                            end2 = -player
                            continue
                        i = np.argmax(scores)
                        game.PushMove(leafs[i][0])
                        tab = leafs[i][2][:5]
                        temp_data.append(tab)
                    elif (player == -1):
                        if Oppenent == "random":
                            leafs = game.GetValidMoves(player) 
                            if (len(leafs) == 0):
                                end2 = -player
                                continue
                            move = random.choice(leafs)
                            game.PushMove(move)

                        elif Oppenent == "minmax":
                            moves = game.minmax(player)
                            if len(moves) == 0 : 
                                end2 == -player
                                continue
                            if random.random() >= exploration:
                                Moves = game.GetValidMoves(player) 
                                move = random.choice(Moves)
                                game.PushMove(move)
                            else :
                                move = random.choice(moves)
                                game.PushMove(move)
                        
                        elif Oppenent == "itself":
                            leafs = game.minmax(player, RL=True)
                            Leaf = tfw.zeros((len(leafs), 5))
                            for l in range(len(leafs)) :
                                tensor = leafs[l][2]
                                Leaf = tfw.tensor_scatter_nd_update(Leaf, [[l]], [tensor[:5]])
                            scores = model.predict_on_batch(Leaf)
                            if (len(scores) == 0):
                                end2 = -player
                                continue
                            if (random.random() >= exploration):
                                move = random.choice(leafs)
                                move = move[0]
                                game.PushMove(move)
                            else:
                                i = np.argmax(scores)
                                game.PushMove(leafs[i][0])
                        elif Oppenent == "trained":
                            continue
                        else :
                            raise("player do not exist")

                end = game.EndGame()

                if end == 1 or end2 == 1:
                    win += 1
                    reward = 10
                    temp_tensor = tfw.constant(temp_data[1:])
                    old_prediction = model.predict_on_batch(temp_tensor)
                    optimal_futur_value = np.ones(old_prediction.shape)
                    temp_labels = old_prediction + learning_rate * (reward + discount_factor * optimal_futur_value - old_prediction )
                    data = concatenate(data, temp_data[1:])
                    labels = np.vstack((labels, temp_labels))
                    break
			

                
                elif end == -1 or end2 == -1: 
                    lose = lose + 1
                    reward = -10
                    temp_tensor = tfw.constant(temp_data[1:])
                    old_prediction = model.predict_on_batch(temp_tensor)
                    optimal_futur_value = -1*np.ones(old_prediction.shape)
                    temp_labels = old_prediction + learning_rate * (reward + discount_factor * optimal_futur_value - old_prediction )
                    data = concatenate(data, temp_data[1:])
                    labels = np.vstack((labels, temp_labels))
                    break

                player = -player 
        data = tfw.constant(data)
        model.fit(data[1:], labels[2:], epochs=16, batch_size=256, verbose=0)
        labels = np.zeros(1)
        winrate = int((win)/(win+draw+lose)*100)
        winrates.append(winrate)
        model.save("models/"+Oppenent+"aa.keras")

    

    indices = list(range(len(winrates)))

    plt.plot(indices, winrates, marker='o', linestyle='-')

    plt.title('Rates of win')
    plt.xlabel('generations')
    plt.ylabel('wins [%]')

    plt.show()

if "__main__" == __name__ :
    Oppenent = "itself"
    print(Oppenent)
    GetModel(Oppenent=Oppenent)