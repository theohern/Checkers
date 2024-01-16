# Checkers bots based on the Deep-Q learning algorithm

This study were part of the course NIE-MVI : "Computational Intelligence Methods" in the Technical University of Prague. 

Have you ever wondered how a computer can learn to play a board game by itself?
I have, and I have been experimenting with checkers.

The computer needs an opponent to play. Like a human, when it plays it will improve. 
If the computer wins the game, we will encourage it to play the same moves, but if it loses, it will know that the moves it played led to defeat, so it will avoid playing them again. 

To start, we are going to create a model. It will decide which move to play.
This model works like a function: it takes a board as input and returns the move to play.

At first, the computer will randomly select the moves to play. Little by little, as the game progresses, it will improve its understanding of which moves are good and which are bad. We owe all these calculations to a neural network called MLP, which is capable of learning from experience what is a good move and what is a bad move.

I chose to train it 3 times with 3 different opponents. 
1) Learning to play against a random player (who doesn't think)
2) Learn to play against someone who has already played well.
3) Learn to play against yourself. In simple terms, this means playing for both people, like a human playing alone for both players.

The learning phase consists of 10,000 games.
So which of the three players is the best ?

## results

The big winner is the one who has played against himself : he wins all the games against the other two players.
Then it's the one who played against someone who didn't know how to play. 
It's quite surprising, but if you have only played against an experienced player, you have learned nothing, after the learning phase it still don't know how to play.

A report with more details is available. This is the report.txt file


## files

- $checkers.py$ is an implementations of the game of checkers
- $training.py$ is training the different models and save them into .keras files
- $compare.py$ is comparing the different bots created. 

for any improvement or use of my code, please contact me.




