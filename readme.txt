Librarys required : Tensorflow,Pygame,Numpy and Random

ABOUT THE GAME : A game was developed with a window size of 40 by 30 grids. It will have a snake with 4 grids as body and a random grid for the food.At each crash of snake,new snake will be generated at the top left of the window and score will displayed in the output.

ABOUT THE INPUT NEURONS: Input of Neuron network will have an array of 8 numbers:
1>>Is there an obstacle in the right grid of the snake head (1 — yes, 0 — no)
2>>Is there an obstacle in the left grid of the snake head (1 — yes, 0 — no)
3>>Is there an obstacle in the top grid of the snake head (1 — yes, 0 — no)
4>>Is there an obstacle in the bottom grid of the snake head (1 — yes, 0 — no)
5>>Euclidean distance to the food from the right grid of the snake head
6>>Euclidean distance to the food from the left grid of the snake head
7>>Euclidean distance to the food from the top grid of the snake head
8>>Euclidean distance to the food from the bottom grid of the snake head

ABOUT THE OUTPUT NEURONS: Output of Neuron network will have an array of 4 values, where the next move of snake will decedid based on the index of maximum value in the array.
index:0 Right move
index:1 Left move 
index:2 Top move 
index:3 Bottom move 

TRAINING THE NEURAL NETWORK : Initial 4 training sets are trained and after the every crash of snake the new traing data will be trained to neurol network.
LABELING TO THE TRAINING DATA  : 0,1,2 and 3 is labeled based on 8 input values.First preference is given to the grid having no obstacles around snake head and second preference was given to the grid having less distance to food from snake head.

Ex1:Data=[0,0,0,1,_,_,_,_] Label=3 (Hear we don't see the distance to food,we will save the snake by moving it to no obstacles side)
Ex2:Data=[1,0,0,1,12,_,_,15] Label=0 (Hear we will consider the distance to food because snake has 2 free movements,we will chose the movement which have less distance to food)
Ex3:Data=[1,0,1,1,12,_,10,15] Label=2
Ex4:Data=[0,1,0,0,12,_,_,15] Label=1
Ex5:Data=[1,1,1,1,12,23,34,15] Label=0
