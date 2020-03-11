import pygame
import random
import numpy
from scipy.spatial import distance
from tensorflow import keras

def food():
    snake_no_grids= [i for i in grids if i not in Snake]
    food_plc = random.choice(snake_no_grids)
    return food_plc
def display():
    pygame.draw.rect(screen,(0,0,0), (0,0,M*grid_size,N*grid_size))
    for i in Snake:
        pygame.draw.rect(screen,(255,255,255), (i[0]*grid_size,i[1]*grid_size,grid_size,grid_size),1)
    pygame.draw.rect(screen,(255,255,255), (Food[0]*grid_size,Food[1]*grid_size,grid_size,grid_size))
    pygame.display.update()
def new_snake():
    global snake_tail,snake_head
    new_snake=[]
    if move == 'Right' :
        new_snake.append((Snake[0][0]+1,Snake[0][1]))
    elif move == 'Left' :
        new_snake.append((Snake[0][0]-1,Snake[0][1]))
    elif move == 'Top' :
        new_snake.append((Snake[0][0],Snake[0][1]-1))
    elif move == 'Bottum' :
        new_snake.append((Snake[0][0],Snake[0][1]+1))
    for i in Snake:
        new_snake.append(i)
    snake_tail=new_snake.pop()
    snake_head=new_snake[0]
    return new_snake
def data_get():
    val={'Right':0,'Left':1,'Top':2,'Bottum':3}
    a_Train_label.append(val[move])
    il,iid=[],[]
    r=(snake_head[0]+1,snake_head[1])
    l=(snake_head[0]-1,snake_head[1])
    t=(snake_head[0],snake_head[1]-1)
    b=(snake_head[0],snake_head[1]+1)
    for i in [r,l,t,b]:
        iid.append(int(distance.euclidean(i, Food)))
        if not (i in grids) or i in Snake:
            il.append(int(0))
        else:
            il.append(int(1))
    il.extend(iid)
    a_Train_data.append(il)
def train_model():
    global model
    Train_dataa=numpy.reshape(Train_data,(len(Train_data),8,1))
    Train_labela=numpy.array(Train_label)
    model.compile(optimizer='adam',loss='sparse_categorical_crossentropy',metrics=['accuracy'])
    model.fit(Train_dataa,Train_labela,epochs=3)
def model_pred():
    lst=['Right','Left','Top','Bottum']
    global move
    il,iid=[],[]
    r=(snake_head[0]+1,snake_head[1])
    l=(snake_head[0]-1,snake_head[1])
    t=(snake_head[0],snake_head[1]-1)
    b=(snake_head[0],snake_head[1]+1)
    for i in [r,l,t,b]:
        iid.append(int(distance.euclidean(i, Food)))
        if not (i in grids) or i in Snake:
            il.append(int(0))
        else:
            il.append(int(1))
    il.extend(iid)
    pred=model.predict(numpy.reshape(il,(1,8,1)))
    move=lst[numpy.argmax(pred[0])] 
def right_label(ip):
    block,distance=ip[:4],ip[4:]
    if sum(block)==1:
        return block.index(1)
    else:
        oop=[]
        for i in range(4):
            if block[i]==0:
                oop.append(100)
            else:
                oop.append(distance[i])
        return oop.index(min(oop)) 
def updata_train_data():
    a_Train_data.pop()
    a_Train_label.pop()
    if len(Train_data) <= 20000:
        data,label=[],[]
        for i in a_Train_data:
            data.append(i)
            label.append(right_label(i))
        Train_label.extend(label)
        Train_data.extend(data)
    else:
        sample=a_Train_data[-1]
        label=right_label(sample)
        Train_data.append(sample)
        Train_label.append(label)

M,N=40,30
grid_size=20
Snake=[(-1,0),(-2,0),(-3,0),(-4,0)]
move='Right'
grids=[]
for i in range(M):
    for j in range(N):
        grids.append((i,j))

Train_data,Train_label=[[1,0,0,0,0,0,0,0],[0,1,0,0,0,0,0,0],[0,0,1,0,0,0,0,0],[0,0,0,1,0,0,0,0]],[0,1,2,3]
a_Train_data,a_Train_label=[],[]
model=  keras.Sequential([
                keras.layers.Flatten(input_shape=(8,1)),
                keras.layers.Dense(100,activation='relu'),
                keras.layers.Dense(4,activation='softmax')
                ])

mloop=True
while mloop:
    pygame.init()
    screen = pygame.display.set_mode((M*grid_size,N*grid_size))
    Food=food()
    train_model()
    loop=True
    while loop:
        pygame.time.wait(50)
        Snake=new_snake()
        display()
        model_pred()
        data_get()
        snake_body=Snake[1:len(Snake)]
        if snake_head==Food:
            Food=food()
            Snake.append(snake_tail)
        if not (snake_head in grids) or snake_head in snake_body:
            print('Game over')
            print('Score : ',len(Snake)-4)
            updata_train_data()
            train_model()
            Snake=[(-1,0),(-2,0),(-3,0),(-4,0)]
            move='Right'
            loop=False
        ev=pygame.event.get()
        for event in ev:
            if event.type == pygame.QUIT:
                pygame.quit()
                loop=False
                mloop=False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    move='Right'
                elif event.key == pygame.K_LEFT:
                    move='Left'
                elif event.key == pygame.K_UP:
                    move='Top'
                elif event.key == pygame.K_DOWN:
                    move='Bottum'