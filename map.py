import random

class Map(object):
    def __init__(self,rows,cols,max_density=0.35):
        self.rows = rows
        self.cols = cols

        # list of cells, 0=wall,1=floor
        self.cells = [[0]*cols for _ in range(rows)]
        self.rooms = []
        self.floorArea = 0
        self.max_density = max_density


class Room(object):
    def __init__(self,x,y,width,height):
        # here take x,y as startCol,startRow
        self.x1, self.y1 = x, y
        self.x2, self.y2 = x+width, y+height
        self.cx = x + width//2
        self.cy = y + height//2

    def __repr__(self):
        return f'Room at({self.cx},{self.cy}),{self.x2-self.x1}x{self.y2-self.y1}'

    def intersects(self, other):
        bound_x1 = min(self.x1, other.x1)
        bound_y1 = min(self.y1, other.y1)
        bound_x2 = max(self.x2, other.x2)
        bound_y2 = max(self.y2, other.y2)
        return not (((bound_y2-bound_y1) >= (self.y2-self.y1 + other.y2-other.y1) or
                (bound_x2-bound_x1) >= (self.x2-self.x1 + other.x2-other.x1)))

    # modify the 2d List of terrain, update the floorArea and map.rooms
    def updateMap(self, map):
        for col in range(self.x1+1,self.x2):
            for row in range(self.y1+1,self.y2):
                map.cells[row][col] = 1
        map.floorArea += (self.x2-self.x1-1) * (self.y2-self.y1-1)

        # build connections between rooms
        if map.rooms != []:
            prevRoom = map.rooms[-1]
            for col,row in self.connectionBetweenRooms(prevRoom):
                if map.cells[row][col] == 0:
                    map.floorArea += 1
                map.cells[row][col] = 1

        # append new room to the rooms list
        map.rooms.append(self)

    def connectionBetweenRooms(self, prevRoom):
        result = set()
        startX, startY = self.cx, self.cy
        endX, endY = prevRoom.cx, prevRoom.cy

        # randomly choose a pattern of the connection
        # 0 = horizon first, vertical second
        # 1 = vertical first, horizon second
        dir = random.choice([0, 1])
        if dir == 0:
            cornerX, cornerY = endX, startY
            if startX <= cornerX:
                horiIndexFrom, horiIndexTo = startX, cornerX
            else:
                horiIndexFrom, horiIndexTo = cornerX, startX
            if endY <= cornerY:
                vertiIndexFrom, vertiIndexTo = endY, cornerY
            else:
                vertiIndexFrom, vertiIndexTo = cornerY, endY
        else:
            cornerX, cornerY = startX, endY
            if endX <= cornerX:
                horiIndexFrom, horiIndexTo = endX, cornerX
            else:
                horiIndexFrom, horiIndexTo = cornerX, endX
            if startY <= cornerY:
                vertiIndexFrom, vertiIndexTo = startY, cornerY
            else:
                vertiIndexFrom, vertiIndexTo = cornerY, startY

        for x in range(horiIndexFrom, horiIndexTo + 1):
            result.add((x, cornerY))
        for y in range(vertiIndexFrom, vertiIndexTo + 1):
            result.add((cornerX, y))
        return result


# generate a map of width*height large
# keep fill it with empty rooms until max_density (default by 0.4) is met.
def generateMap(width,height):
    map = Map(width, height)
    totalArea = width*height
    room_minSize = 5
    room_maxSize = 10

    while map.floorArea < map.max_density * totalArea:
        # create a room instance
        room_width = random.randint(room_minSize,room_maxSize)
        room_height = random.randint(room_minSize,room_maxSize)
        room_x = random.randint(0, width-room_width-1)
        room_y = random.randint(0, height-room_height-1)
        newRoom = Room(room_x, room_y, room_width, room_height)

        # if the new room intersect with others, then give up this new room.
        if any(newRoom.intersects(room) for room in map.rooms):
            continue

        # we got a qualified room now, update the map
        newRoom.updateMap(map)
    return map