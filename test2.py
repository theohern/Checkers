import checkers
import matplotlib.pyplot as plt
from keras import Sequential, regularizers
from keras.layers import Activation, Conv2D, Dropout, Dense, Flatten, BatchNormalization
from keras.models import model_from_json
import tensorflow as tfw
import numpy as np
import random


def CompareRandomMinmax(player1, player2, NumberPlays):
    black = 0
    white = 0
    draw = 0
    for i in range(NumberPlays):
        if i % (NumberPlays/10) == ((NumberPlays/10) -1) : print(f"[{i+1}/{NumberPlays}]%")
        game = checkers.Checkers()
        ret = game.playRandomMinMax(Bot1=player1, Bot2=player2, verbose=False)
        if ret == 1 : white += 1
        elif ret == -1 : black += 1
        elif ret == 0 : draw+=1
        else : raise (f"Problem with return value of function Compare2Bots, get {ret}")

    # Calcul des pourcentages
    black_percent = (black / NumberPlays) * 100
    white_percent = (white / NumberPlays) * 100
    draw_percent = (draw / NumberPlays) * 100

    # Création des données pour le graphique
    labels = 'Black', 'White', 'Draw'
    sizes = [black_percent, white_percent, draw_percent]
    colors = ['lightcoral', 'lightskyblue', 'green']

    # Création du graphique en secteurs (disque)
    plt.figure(figsize=(8, 6))
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')  # Assure que le graphique est un cercle
    plt.title('Répartition des jeux entre Black et White')
    plt.show()

def main():
    CompareRandomMinmax("minmax", "minmax", 1000)

def concatenate(array1, array2):
    for i in range(len(array2)):
        array1.append(array2[i])
    return array1
    

def GetData(number):
    features = []
    while len(features) < number:
        game = checkers.Checkers()
        _, features = game.playRandomMinMax(Bot1="minmax", Bot2="minmax", verbose=False, GetFeatures=True, ArrayFeatures=features)
    return features[:number]

def GetModel():
    metrics_model = Sequential()
    metrics_model.add(Dense(32, activation='relu', input_dim=5)) 
    metrics_model.add(Dense(16, activation='relu',  kernel_regularizer=regularizers.l2(0.1)))

    # output is passed to relu() because labels are binary
    metrics_model.add(Dense(1, activation='relu',  kernel_regularizer=regularizers.l2(0.1)))
    metrics_model.compile(optimizer='nadam', loss='binary_crossentropy', metrics=["acc"])

    size = 10000
    data = GetData(size)
    metric = tfw.zeros((size, 5))
    target = tfw.zeros(size)
    count = 0
    for d in data:
        tensor = tfw.convert_to_tensor(d, dtype=tfw.float32)
        metric = tfw.tensor_scatter_nd_update(metric, [[count]], [tensor[:5]])
        target = tfw.tensor_scatter_nd_update(target, [[count]], [tensor[5]])
        count += 1

    
    history = metrics_model.fit(metric , target, epochs=32, batch_size=64, verbose=0)

   
    # History for accuracy
    plt.plot(history.history['acc'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'validation'], loc='upper left')
    plt.show()

    # History for loss
    plt.plot(history.history['loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'validation'], loc='upper left')
    plt.show()

    data = [] # tous les boards
    labels = np.zeros(1) # tous les QValues 
    winrates = []
    learning_rate = 0.5
    discount_factor = 0.95

    for generations in range (200):
        print(generations)
        data = []
        win = 0
        lose = 0
        draw = 0
        for g in range(10):
            temp_data = []
            game = checkers.Checkers()
            player = 1
            count = 0
            while True:
                count += 1
                end2 = 0
                if count > 200 :
                    #print("draw")
                    draw += 1
                    break

                else :
                    if (player == 1) : 
                        leafs = game.minmax(player, RL=True) # move | score | features
                        Leaf = tfw.zeros((len(leafs), 5))
                        for l in range(len(leafs)) :
                            tensor = leafs[l][2]
                            Leaf = tfw.tensor_scatter_nd_update(Leaf, [[l]], [tensor[:5]])
                        scores = metrics_model.predict_on_batch(Leaf)
                        if (len(scores) == 0):
                            end2 = -player
                            continue
                        i = np.argmax(scores)
                        game.PushMove(leafs[i][0])
                        tab = leafs[i][2][:5]
                        temp_data.append(tab)
                    elif (player == -1):
                        leafs = game.minmax(player) # move
                        if (len(leafs) == 0):
                            end2 = -player
                            continue
                        move = random.choice(leafs)
                        game.PushMove(move)

                #print(moves[i])
                #game.Show ()
                end = game.EndGame()

                if end == 1 or end2 == 1:
                    #print(f"player 1 wins");
                    win += 1
                    reward = 10
                    temp_tensor = tfw.constant(temp_data[1:])
                    old_prediction = metrics_model.predict_on_batch(temp_tensor)
                    optimal_futur_value = np.ones(old_prediction.shape)
                    temp_labels = old_prediction + learning_rate * (reward + discount_factor * optimal_futur_value - old_prediction )
                    data = concatenate(data, temp_data[1:])
                    labels = np.vstack((labels, temp_labels))
                    break
			

                
                elif end == -1 or end2 == -1: 
                    #print(f"player -1 win")
                    lose = lose + 1
                    reward = -10
                    temp_tensor = tfw.constant(temp_data[1:])
                    old_prediction = metrics_model.predict_on_batch(temp_tensor)
                    optimal_futur_value = -1*np.ones(old_prediction.shape)
                    temp_labels = old_prediction + learning_rate * (reward + discount_factor * optimal_futur_value - old_prediction )
                    data = concatenate(data, temp_data[1:])
                    labels = np.vstack((labels, temp_labels))
                    break

                player = -player 
        print(len(data))
        data = tfw.constant(data)
        print(data.shape)
        print("fitting the model")
        metrics_model.fit(data[1:], labels[2:], epochs=16, batch_size=256, verbose=0)
        print("done")
        labels = np.zeros(1)
        winrate = int((win+draw)/(win+draw+lose)*100)
        winrates.append(winrate)
        metrics_model.save_weights('model.h5')

    

    # Création de l'index pour l'axe x
    indices = list(range(len(winrates)))

    # Tracé du graphique
    plt.plot(indices, winrates, marker='o', linestyle='-')

    # Ajout de titres et de libellés d'axes
    plt.title('Graphique des valeurs en fonction de l\'index')
    plt.xlabel('Index dans le tableau')
    plt.ylabel('Valeurs')

    # Affichage du graphique
    plt.show()





if "__main__" == __name__ :
    GetModel()