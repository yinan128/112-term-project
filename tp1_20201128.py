from cmu_112_graphics import *
import random
import time
from entity import Entity, Player
from map import generateMap, Map, Room


def appStarted(app):

    # map generation
    app.mapRows = app.mapCols = 70
    app.map = generateMap(app.mapRows, app.mapCols)

    # player (born at a random room.)
    birthRoom = random.choice(app.map.rooms)
    cx = birthRoom.cx
    cy = birthRoom.cy
    print(cx,cy)
    app.player = Player(cx, cy)
    app.playerSpriteCount = 0

    # others
    app.margin = 20
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



def keyPressed(app, event):
    if event.key == "Up":
        app.player.y -= 1
    elif event.key == "Down":
        app.player.y += 1
    elif event.key == "Left":
        app.player.x -= 1
    elif event.key == "Right":
        app.player.x += 1
    elif event.key == "Tab":
        app.drawMiniMap = not app.drawMiniMap


def timerFired(app):
    app.playerSpriteCount = (app.playerSpriteCount+1) % 4


######################################################
#                     helpers                        #
######################################################

def getGlobalCellBounds(app, row, col):
    cellWidth = (app.width - app.margin * 2) // app.mapCols
    cellHeight = (app.height - app.margin * 2) // app.mapRows
    x1 = cellWidth * col + app.margin
    y1 = cellHeight * row + app.margin
    x2 = cellWidth * (col + 1) + app.margin
    y2 = cellHeight * (row + 1) + app.margin
    return x1, y1, x2, y2


def getCellBoundsInFrame(app, row, col):
    rows = cols = app.viewDepth * 2 + 1
    cellWidth = (app.width - app.margin * 2) // cols
    cellHeight = (app.height - app.margin * 2) // rows
    x1 = cellWidth * col + app.margin
    y1 = cellHeight * row + app.margin
    x2 = cellWidth * (col + 1) + app.margin
    y2 = cellHeight * (row + 1) + app.margin
    return x1, y1, x2, y2


def moveIfValid(app, direction):
    drow, dcol = direction
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

def drawGameMap(app, canvas):
    for row in range(app.mapRows):
        for col in range(app.mapCols):
            if (col, row) == (app.player.x, app.player.y):
                x1, y1, x2, y2 = getGlobalCellBounds(app, row, col)
                canvas.create_rectangle(x1, y1, x2, y2, fill='red')
                continue

            if app.map.cells[row][col] == 0: # walls
                x1, y1, x2, y2 = getGlobalCellBounds(app, row, col)
                canvas.create_rectangle(x1, y1, x2, y2, fill='cyan')

def drawFirstPerspeciveMap(app,canvas):
    deviation_col = app.player.x - app.viewDepth
    deviation_row = app.player.y - app.viewDepth
    for row in range(app.viewDepth*2+1):
        for col in range(app.viewDepth*2+1):
            x1, y1, x2, y2 = getCellBoundsInFrame(app, row, col)
            if app.map.cells[row+deviation_row][col+deviation_col] == 0: # walls
                fillColor = "grey"
            else:
                fillColor = "white"
            canvas.create_rectangle(x1,y1,x2,y2,fill=fillColor)


def drawPlayer(app, canvas):
    # player is always located in the center of frame.
    cx, cy = app.width//2, app.height//2
    i = app.playerSpriteCount
    canvas.create_image(cx, cy, image=ImageTk.PhotoImage(app.player.getTile(i)))
    canvas.create_text(10,10,text=f"currPos={app.player.x,app.player.y}",anchor="w")


def drawMissMsg(app, canvas):
    canvas.create_text(app.width / 2, app.height / 2, text='Missed!', fill='red')


def redrawAll(app, canvas):
    # drawFirstPerspective(app, canvas)
    drawFirstPerspeciveMap(app, canvas)
    drawPlayer(app, canvas)

    if app.drawMiniMap:
        drawGameMap(app, canvas)

    if app.sendMissMsg:
        drawMissMsg(app, canvas)

def main():
    width = 11*48
    height = 11*48
    margin = 20
    runApp(width=width+margin*2, height=height+margin*2)

main()
