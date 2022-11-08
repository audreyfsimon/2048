
from cmu_112_graphics import *
import random, string, math, time, copy

from cmu_112_graphics import *
import random
from dataclasses import make_dataclass
import pygame


#################################################
# Helper functions
#################################################

# Citation - Taken from 15-112 Website: 
# https://www.cs.cmu.edu/~112/notes/notes-2d-lists.html#dimensions

def make2dList(rows, cols, placement):
    return [ ([placement] * cols) for row in range(rows) ]

# https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#caching\
# PhotoImages

def getCachedImage(app,image):
    if ('cachedPhotoImage' not in image.__dict__):
        image.cachedPhotoImage = ImageTk.PhotoImage(image)
    return image.cachedPhotoImage

#################################################
# Main App
#################################################

def gameDimensions():
    rows = 4
    cols = 4
    cellSize = 100
    margin = 30
    return rows,cols,cellSize,margin

def playGame():
    rows,cols,cellSize,margin = gameDimensions()
    width = 2*margin+cellSize*cols
    height = 2*margin+cellSize*rows
    runApp(width=width, height=height)

#############################################
# Global Variables
#############################################

def appStarted(app):
    app.gameLevel = 'Easy'
    app.gameMode = "Play"
    app.timeRef = time.time()
    app.time = 0
    app.level = 0
    app.rows,app.cols,app.cellSize,app.margin = gameDimensions()
    app.terrain = createTerrain(app.rows,app.cols,app.level)
    app.numboard = copy.deepcopy(app.terrain)
    makeNums(app.terrain,app.numboard,app.rows,app.cols)
    app.copyTerrain = copy.deepcopy(app.terrain)
    app.guessingBoard = make2dList(app.rows,app.cols,'guess')
    app.clickMode = 'Normal'
    app.bombs =0
    app.foundBombs = 0
    app.foundBlanks = 0
    for row in range(len(app.copyTerrain)):
        for col in range(len(app.copyTerrain[0])):
            if app.copyTerrain[row][col]=='bomb':
                app.bombs += 1
    app.blanks = app.rows*app.cols-app.bombs
    print (app.numboard)
    a = [10,0,30,40]
    app.d = {2:'lightcyan',4:'paleturquoise',8:'turquoise',16:'lightseagreen',
    32:'teal',64:'lightslategrey',128:'darkslategray',256:'forestgreen',
    512: 'limegreen',1024: 'lightgreen',2048:'orchid'}
    #for i in reversed(range(4)):
        #print (a[i])

#############################################
# Key Pressed Functions
#############################################

def refreshTerrain(app):
    app.terrain = createTerrain(app.rows,app.cols,app.level)

def moveRight(app):
    refreshTerrain(app)
    for col in reversed(range(len(app.numboard))):
        for row in reversed(range(len(app.numboard[0]))):
            if app.numboard[row][col]!=0:
                r = row
                c = col
                for i in range(4):
                    print (r,c)
                    if c!=3:
                        if app.numboard[r][c+1]==app.numboard[r][c]:
                            if app.terrain[r][c+1]!=100:
                                app.terrain[r][c+1]=100
                                app.numboard[r][c+1]*=2
                                app.numboard[r][c]=0
                        elif app.numboard[r][c+1]==0:
                            app.numboard[r][c+1]=app.numboard[r][c]
                            app.numboard[r][c]=0
                        c=c+1
                print (app.terrain)

def moveLeft(app):
    refreshTerrain(app)
    for col in range(len(app.numboard)):
        for row in range(len(app.numboard[0])):
            if app.numboard[row][col]!=0:
                r = row
                c = col
                print ("A")
                for i in range(4):
                    print (r,c)
                    if c!=0 & app.numboard[r][c-1]==0:
                        if app.numboard[r][c-1]==app.numboard[r][c]:
                            print ("B")
                            if app.terrain[r][c]!=100:
                                print("C")
                                app.terrain[r][c-1]=100
                                app.numboard[r][c-1]*=2
                                app.numboard[r][c]=0
                        elif app.numboard[r][c-1]==0:
                            print ("D")
                            app.numboard[r][c-1]=app.numboard[r][c]
                            app.numboard[r][c]=0
                        c=c-1

def moveDown(app):
    refreshTerrain(app)
    for col in reversed(range(len(app.numboard))):
        for row in reversed(range(len(app.numboard[0]))):
            if app.numboard[row][col]!=0:
                r = row
                c = col
                for i in range(4):
                    if r!=3:
                        if app.numboard[r+1][c]==0:
                            app.numboard[r+1][c]=app.numboard[r][c]
                            app.numboard[r][c]=0
                        elif app.numboard[r+1][c]==app.numboard[r][c]:
                            if app.terrain[r][c]!=100:
                                print("C")
                                app.terrain[r+1][c]=100
                                #app.numboard[r][c-1]*=2
                                #app.numboard[r][c]=0
                                app.numboard[r+1][c]*=2
                                app.numboard[r][c]=0
                            #return
                        r=r+1

def moveUp(app):
    refreshTerrain(app)
    for col in (range(len(app.numboard))):
        for row in (range(len(app.numboard[0]))):
            if app.numboard[row][col]!=0:
                r = row
                c = col
                for i in range(4):
                    if r!=0:
                        if app.numboard[r-1][c]==0:
                            app.numboard[r-1][c]=app.numboard[r][c]
                            app.numboard[r][c]=0
                        elif app.numboard[r-1][c]==app.numboard[r][c]:
                            #app.numboard[r-1][c]*=2
                            #app.numboard[r][c]=0
                            if app.terrain[r][c]!=100:
                                print("C")
                                app.terrain[r-1][c]=100
                                #app.numboard[r][c-1]*=2
                                #app.numboard[r][c]=0
                                app.numboard[r-1][c]*=2
                                app.numboard[r][c]=0
                            #return
                        r=r-1


def moveLeft(app):
    for row in range(len(app.numboard)):
        for col in range(len(app.numboard[0])):
            if app.numboard[row][col]!=0:
                app.numboard[row][col-1]=app.numboard[row][col]
                app.numboard[row][col]=0


def addNum(app):
    init = random.randint(0,15)
    v = random.choice([2,4])
    r = getRow(init)
    c = getCol(init)
    while (app.numboard[r][c]!=0):
        init = random.randint(0,15)
        r = getRow(init)
        c = getCol(init)
    app.numboard[r][c] = v

def keyPressed(app,event):
    if event.key=='r':
        appStarted(app)
    if event.key=='a':
        addNum(app)
    if event.key=='b':
        if app.gameMode == 'Play':
            app.gameMode = 'Cheat'
        else:
            app.gameMode = 'Play'
    if event.key=='f':
        if app.clickMode == 'Normal':
            app.clickMode = 'Flag'
        else:
            app.clickMode = 'Normal'
    if event.key == 'Left':
        moveLeft(app);
        addNum(app)
        #print (app.numboard)
    if event.key == 'Right':
        moveRight(app);
        addNum(app)
    if event.key == 'Down':
        moveDown(app)
        addNum(app)
    if event.key == 'Up':
        moveUp(app)
        addNum(app)

    
    
    
def mousePressed(app,event):
    if app.clickMode == 'Normal':
        if clickedBox(event.x,event.y,app.width,app.height,app.margin):
            row,col = getCellBounds(app,event.x,event.y)
            app.copyTerrain[row][col]='G'
            if app.guessingBoard[row][col]!='Flagged':
                app.guessingBoard[row][col] = "Guessed"
                app.foundBlanks += 1
            if app.terrain[row][col]==0:
                selectNearby(row,col,app)
            elif app.terrain[row][col] == 'bomb':
                app.gameMode = "Over"
    elif app.clickMode == 'Flag':
        if clickedBox(event.x,event.y,app.width,app.height,app.margin):
            row,col = getCellBounds(app,event.x,event.y)
            if app.guessingBoard[row][col] == "Flagged":
                app.guessingBoard[row][col] = "guess"
                if app.copyTerrain[row][col]=='found':
                    app.copyTerrain[row][col]='bomb'
                    app.foundBombs-=1
            else:
                app.guessingBoard[row][col]='Flagged'
                if app.copyTerrain[row][col]=='bomb':
                    app.copyTerrain[row][col]='found'
                    app.foundBombs+=1
    if app.foundBombs == app.bombs and app.foundBlanks==app.blanks:
        app.gameMode = 'Winner'

    

        


def clickedBox(x,y,width,height,margin):
    if margin<=x and x<=width-margin and margin<=y and height-margin>=y:
        return True

def selectNearby(row,col,app):
    moves = [(-1,0),(0,-1),(0,1),(1,0)]
    for (drow,dcol) in moves:
        testRow = row + drow
        testCol = col + dcol
        if moveIsLegal(testRow,testCol,app.terrain):
            if app.copyTerrain[testRow][testCol] == 0:
                app.copyTerrain[testRow][testCol] = 'G'
                if app.guessingBoard[row][col]!='Flagged':
                    app.guessingBoard[testRow][testCol] = "Guessed"
                    app.foundBlanks +=1
                selectNearby(testRow,testCol,app)
            elif type(app.copyTerrain[testRow][testCol]) == int:
                app.copyTerrain[testRow][testCol] = 'G'
                app.guessingBoard[testRow][testCol] = 'Guessed'
                app.foundBlanks += 1
    #print (app.terrain)
    

#############################################
# Timer Fired Functions
#############################################

def timerFired(app):  
    app.time = int((time.time()-app.timeRef))

def getRow(val):
    return val//4%4

def getCol(val):
    return val%4

def makeNums(terrain,numterrain,rows,cols):
    init = random.randint(0,15)
    init2 = random.randint(0,15)
    v1 = random.choice([2,2,4])
    v2 = random.choice([2,2,4])
    while (init==init2):
        init2 = random.randint(0,16)
    r1 = (getRow(init))
    c1 = (getCol(init))
    r2 = (getRow(init2))
    c2 = (getCol(init2))
    terrain[r1][c1] = 1
    terrain[r2][c2] = 1
    numterrain[r1][c1] = v1
    numterrain[r2][c2] = v2
    #numterrain[3][1] = 12
    #numterrain[2][1] = 12
    #numterrain[1][1] = 12
    #numterrain[0][1] = 12
    return
    for row in range(len(terrain)):
        for col in range(len(terrain[0])):
            #if (terrain[row][col])==1:
            #    return
            moves = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
            for (drow,dcol) in moves:
                testRow = row + drow
                testCol = col + dcol
                if moveIsLegal(testRow,testCol,terrain) and \
                    terrain[row][col]!='bomb':
                    if terrain[testRow][testCol] == 'bomb':
                        terrain[row][col] += 1

def moveIsLegal(row,col,terrain):
    if row >= len(terrain) or row<0 or col>=len(terrain[0]) or col<0:
        return False
    return True

def createTerrain(rows,cols,level):
    terrain = make2dList(rows,cols,0)
    return terrain

def getCellBounds(app,row,col):
    x0 = app.margin+app.cellSize*col+app.mapX+app.distance*app.cellSize
    x1 = x0+app.cellSize
    y0 = app.cellSize*row+app.margin
    y1 = y0+app.cellSize
    return x0,x1,y0,y1

def getCellBounds(app,x,y):
    col = (x-app.margin)//app.cellSize
    row = (y-app.margin)//app.cellSize
    return row,col

def drawCell(app,canvas,row,col,num):
    #x = app.margin+app.cellSize*col+app.mapX+app.cellSize/2
    #IMG = getCachedImage(app,IMG)
    #canvas.create_image(x+app.distance*app.cellSize,
    #app.cellSize*row+app.margin+app.cellSize/2,image=IMG)
    if num == 'guess':
        color = 'light grey'
    elif num == 'Guessed':
        color = None
    elif num == 'Flagged':
        color = 'purple'
    elif num == 'bomb':
        color = 'red'
    elif type(num)==int and num>0:
        color = app.d[num]
    elif type(num)==int and num==0:
        color = 'light green'
    else:
        color = 'purple'
    canvas.create_rectangle(app.margin+col*app.cellSize,
    app.margin+row*app.cellSize,
    app.margin+(col+1)*app.cellSize,app.margin+(row+1)*app.cellSize,fill=color)
    if type(num)==int and num>0:
        canvas.create_text(app.margin+col*app.cellSize+app.cellSize//2,
        app.margin+row*app.cellSize+app.cellSize//2,text=num,font='Arial 50')


def drawBoard(app,canvas):
    for row in range(len(app.terrain)):
        for col in range(len(app.terrain[0])):
            drawCell(app,canvas,row,col,app.numboard[row][col])

def drawGuessingBoard(app,canvas):
    for row in range(len(app.terrain)):
        for col in range(len(app.terrain[0])):
            drawCell(app,canvas,row,col,app.numboard[row][col])

def drawGameOver(app,canvas):
    canvas.create_rectangle(app.width//2-200,app.height//2-100,
    app.width//2+200,app.height//2+100,
    fill='Black')
    canvas.create_text(app.width//2,app.height//2,text='Game Over!',
    fill='White',
    font='Arial 50')

def drawWinner(app,canvas):
    canvas.create_rectangle(app.width//2-200,app.height//2-100,
    app.width//2+200,app.height//2+100,
    fill='Pink')
    canvas.create_text(app.width//2,app.height//2,text='You Won!!!',
    fill='White',
    font='Arial 50')

def drawStart(app,canvas):
    canvas.create_rectangle(0,0,app.width,app.height,fill='Grey')
    canvas.create_text(app.width//2,app.height//5,
    text='Welcome to Minesweeper!')

def drawFlagMode(app,canvas):
    return
    if app.clickMode == 'Flag':
        canvas.create_rectangle(app.width//2-100,10,app.width//2+100,30,
        fill='light green',width=0)
        canvas.create_text(app.width//2,20,text="FLAG MODE ON",font='Arial 18')
    else:
        canvas.create_rectangle(app.width//2-100,10,app.width//2+100,30,
        fill='red',width=0)
        canvas.create_text(app.width//2,20,text="FLAG MODE OFF",font='Arial 18')
        
#############################################
# Run Game
#############################################
def redrawAll(app,canvas):
    canvas.create_rectangle(0,0,app.width,app.height,fill='pink')
    drawBoard(app,canvas)
    if app.gameMode == 'Play':
       drawGuessingBoard(app,canvas)
    if app.gameMode == 'Over':
        drawGameOver(app,canvas)
    if app.gameMode == 'Winner':
        drawWinner(app,canvas)
    drawFlagMode(app,canvas)
    if app.gameMode == 'Start':
        drawStart(app,canvas)
    #canvas.create_triangle(0,0,20,20)
    #canvas.create_rectangle(100,100,300,300,)

if (__name__ == '__main__'):
    playGame()


def slope(x1, y1, x2, y2):
    m = (y2-y1) / (x2-x1)
    return m

def intercept(x1, y1, x2, y2):
    b = (x1*y2 - x2*y1) / (x1-x2)
    return b

def remove_x_coords(x,y):
    new_x = []
    new_y = []
    for i in range(len(x)-1, -1, -1):
        if x[i] not in new_x:
            new_x.append(x[i])
            new_y.append(y[i])
    return sorted(new_x), list(reversed(new_y))

def remove_xh_coords(x,y):
    new_x = []
    new_y = []
    for i in range(len(x)-1, -1, -1):
        if x[i] not in new_x:
            new_x.insert(0,x[i])
            new_y.insert(0,y[i])
    return (new_x), ((new_y))

for i in range(10, 0, -1):
    print (i)

def linear_interpolate(n, x_knots, y_knots, x_input):
    x_coords, y_coords = zip(*sorted(zip(x_knots, y_knots)))
    x_coords = list(x_coords)
    y_coords = list(y_coords)
    index = 0
    for i in range(len(x_coords)):
        if x_coords[i] == x_input:
            return y_coords[i]
        if x_coords[i] > x_input:
            index = i
            break
    if index == 0:
        index += 1
    x1, x2 = x_coords[index-1], x_coords[index]
    y1, y2 = y_coords[index-1], y_coords[index]
    print (x_coords, y_coords)
    x_coords, y_coords = remove_x_coords(x_coords, y_coords)
    print (x_coords, y_coords)
    return
    #return
    m = slope(x1, y1, x2, y2)
    b = intercept(x1, y1, x2, y2)
    y = m * x_input + b
    print (y)

n = int('5')
x_knots = [-98.0, -88.0, -82.0, -77.0, -76.0, -71.0, -68.0, -64.0, -64.0, -32.0, -30.0, -29.0, -21.0, 9.0, 14.0, 19.0, 27.0, 46.0, 50.0, 56.0, 59.0, 60.0, 67.0, 82.0, 84.0, 87.0, 89.0, 94.0, 94.0, 99.0]
y_knots = [-66.0, 80.0, 8.0, -13.0, -8.0, -51.0, 94.0, 58.0, 62.0, -12.0, -56.0, 40.0, 83.0, -27.0, -19.0, 9.0, -35.0, -69.0, -12.0, -69.0, -81.0, 26.0, -11.0, -73.0, -31.0, 18.0, 45.0, -75.0, -33.0, 88.0]
x_input = 120
linear_interpolate(n, x_knots, y_knots, x_input)
