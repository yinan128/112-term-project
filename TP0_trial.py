from cmu_112_graphics import *
import random
import time

def appStarted(app):
    app.mapRows = app.mapCols = 100
    app.margin = 20
    app.gameMap = generateMap(app)
    app.currRow = app.mapRows // 2
    app.currCol = app.mapCols // 2
    app.viewDepth = 5
    app.drawMiniMap = False
    app.timerDelay = 100
    app.time_groundEffect = time.time()
    app.time_moveCtrl = time.time()
    app.lightEffect = 0
    app.moveAllowed = True

    app.sendMissMsg = False
    app.time_missMsg = time.time()




# randomly generate a Map of 50*50 cells
def generateMap(app):
    mapCells = [[False] * app.mapCols for _ in range(app.mapRows)]
    dirs = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    pathRow = app.mapRows // 2
    pathCol = app.mapCols // 2
    mapCells[pathRow][pathCol] = True
    while True:
        i = random.randint(0,3)
        dRow, dCol = dirs[i]
        pathRow += dRow
        pathCol += dCol
        if (pathRow < 0 or pathRow >= app.mapRows or
            pathCol < 0 or pathCol >= app.mapCols):
            return mapCells
        mapCells[pathRow][pathCol] = True


def keyPressed(app,event):
    if event.key == "Up":      moveIfValid(app,(-1,0))
    elif event.key == "Down":  moveIfValid(app,(+1,0))
    elif event.key == "Left":  moveIfValid(app,(0,-1))
    elif event.key == "Right": moveIfValid(app,(0,+1))
    elif event.key == "Tab":   app.drawMiniMap = not app.drawMiniMap


def timerFired(app):
    if time.time() - app.time_groundEffect >= .5:
        app.lightEffect = 1 if app.lightEffect == 0 else 0
        app.time_groundEffect = time.time()

    #
    if app.moveAllowed == False and time.time() - app.time_moveCtrl >= 0.8:
        app.moveAllowed = True
        app.time_moveCtrl = time.time()
    if app.moveAllowed and time.time() - app.time_moveCtrl >= 0.4:
        app.moveAllowed = False
        app.time_moveCtrl = time.time()

    # the error msg only last for 0.2 sec
    if app.sendMissMsg and time.time()-app.time_missMsg >= 0.2:
        app.sendMissMsg = False


######################################################
#                     helpers                        #
######################################################

def getCellBounds(app, row, col):
    cellWidth = (app.width - app.margin * 2)//app.mapCols
    cellHeight=(app.height-app.margin*2)//app.mapRows
    x1 = cellWidth * col + app.margin
    y1 = cellHeight * row + app.margin
    x2 = cellWidth * (col+1) + app.margin
    y2 = cellHeight * (row+1) + app.margin
    return x1,y1,x2,y2

def getCellBoundsLocal(app, row, col):
    rows = cols = app.viewDepth * 2 + 1
    cellWidth = (app.width - app.margin * 2)// cols
    cellHeight=(app.height-app.margin*2)// rows
    x1 = cellWidth * col + app.margin
    y1 = cellHeight * row + app.margin
    x2 = cellWidth * (col+1) + app.margin
    y2 = cellHeight * (row+1) + app.margin
    return x1,y1,x2,y2

def moveIfValid(app,direction):
     drow,dcol = direction
     row = app.currRow + drow
     col = app.currCol + dcol
     if not app.moveAllowed:
         app.sendMissMsg = True
         app.time_missMsg = time.time()
         return
     if app.gameMap[row][col]:
         app.currRow, app.currCol = row, col
         # make instant change of the ground pattern
         app.lightEffect = 1 if app.lightEffect == 0 else 0
         app.time_groundEffect = time.time()

######################################################
#                     viewers                        #
######################################################

def drawGameMap(app,canvas):
    rows = len(app.gameMap)
    cols = len(app.gameMap[0])
    for row in range(rows):
        for col in range(cols):
            if app.gameMap[row][col]:
                x1, y1, x2, y2 = getCellBounds(app, row, col)
                canvas.create_rectangle(x1, y1, x2, y2, fill='cyan')


def drawFirstPerspective(app,canvas):
    # only draw the part in the screen.
    startRow = app.currRow - app.viewDepth
    endRow = app.currRow + app.viewDepth + 1
    startCol = app.currCol - app.viewDepth
    endCol = app.currCol + app.viewDepth + 1
    for row in range(startRow,endRow):
        for col in range(startCol,endCol):
            x1, y1, x2, y2 = getCellBoundsLocal(app, row - startRow, col - startCol)
            if app.gameMap[row][col]:
                if (row-startRow+col-startCol) % 2 == app.lightEffect:
                    floorColor = 'gainsboro'
                else:
                    floorColor = 'white'
                canvas.create_rectangle(x1, y1, x2, y2, fill=floorColor)
            else:
                canvas.create_rectangle(x1, y1, x2, y2, fill='black')

def drawPlayer(app,canvas):
    cx = app.width // 2
    cy = app.height // 2
    rows = cols = app.viewDepth * 2 + 1
    cellWidth = (app.width - app.margin * 2) // cols
    cellHeight = (app.height - app.margin * 2) // rows
    r = min(cellWidth,cellHeight) // 2
    canvas.create_oval(cx-r,cy-r,cx+r,cy+r,fill='black')

def drawMissMsg(app,canvas):
    canvas.create_text(app.width/2,app.height/2,text='Missed!',fill='red')

def redrawAll(app,canvas):

    drawFirstPerspective(app,canvas)
    drawPlayer(app, canvas)

    if app.drawMiniMap:
        drawGameMap(app,canvas)

    if app.sendMissMsg:
        drawMissMsg(app, canvas)


runApp(width=800, height=800)