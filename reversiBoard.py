from asyncio.windows_events import NULL
import pygame
from pygame.math import Vector2
from pygame.surface import Surface
from pygame.color import Color
import math
from reversiGrid import ReversiGrid, StoneType
import reversiUtility

class ReversiBoardInfo:
    def __init__(self, boardOffset: Vector2, numGridX: int, numGridY: int, gridWidth: float, gridColor: Color, backgroundColor: Color):
        self.boardOffset = boardOffset
        self.gridSizeX = numGridX
        self.gridSizeY = numGridY
        self.gridWidth = gridWidth
        self.gridColor = gridColor
        self.backgroundColor = backgroundColor

class FlipInfo:
    def __init__(self, startX: int, startY: int):
        self.__startPoint = (startX, startY)
        self.__endPoints = []

    def __str__(self):
        message = "start point(%d, %d), %d end points:\n" % (self.__startPoint[0], self.__startPoint[1], self.getNumEndPoints())
        for endIdx in range(self.getNumEndPoints()):
            endX, endY = self.getEndPoint(endIdx)
            message += "end point(%d, %d): inner points=[" % (endX, endY)
            innerPoints = self.getInnerPoints(endIdx)
            for i in range(len(innerPoints)):
                inrPnt = innerPoints[i]
                if i != 0: message += " "
                message += "(%d, %d)" % (inrPnt[0], inrPnt[1])
            message += "]"
            if endIdx < self.getNumEndPoints() - 1: message += "\n"

        return message

    def getStartPoint(self):
        return self.__startPoint

    def clearEndPoints(self):
        self.__endPoints.clear()

    def appendEndPoint(self, x: int, y: int):
        diffX, diffY = FlipInfo.getDiff(self.__startPoint, (x, y))
        # check if a line made with the start point and given end point is vertical, horizontal or diagonal(45 deg). if true, then append it.
        if diffX == 0 or diffY == 0 or abs(diffX) == abs(diffY):
            self.__endPoints.append((x, y))
            return True
        return False

    def getNumEndPoints(self):
        return len(self.__endPoints)

    def getEndPoint(self, endIdx: int):
        return self.__endPoints[endIdx]

    def getDiff(start, end):
        return tuple([end[i] - start[i] for i in range(2)])

    def getDirection(self, endIdx: int):
        return tuple([min(max(self.__endPoints[endIdx][i] - self.__startPoint[i], -1), 1) for i in range(2)])

    def getInnerPoints(self, endIdx: int):
        result = []
        dirX, dirY = self.getDirection(endIdx)
        endX, endY = self.__endPoints[endIdx]
        x, y = self.__startPoint
        while x + dirX != endX or y + dirY != endY:
            x += dirX
            y += dirY
            result.append((x, y))
        return result
    
# Stores grids array and handles rendering of Reversi board as well as stones
class ReversiBoard:
    def __init__(self, surface: Surface, boardInfo: ReversiBoardInfo):
        self.surface = surface
        self.boardInfo = boardInfo

        # make a 2d array of numGridX * numGridY 
        self.__grids = [[ReversiGrid() for i in range(0, boardInfo.gridSizeX)] for j in range(0, boardInfo.gridSizeY)]

    def getGridsAsStr(self):
        message = "[\n"
        for y in range(0, self.boardInfo.gridSizeY):
            message += "    ["
            for x in range(0, self.boardInfo.gridSizeX):
                grid = self.getGrid(x, y)
                # gridNum = 0 if grid.isEmpty else (1 if grid.stoneType == StoneType.BlackStone else 2)
                gridNum = reversiUtility.convertGridToInt(grid)
                message += str(gridNum) if x == 0 else ", " + str(gridNum)
            message += "],\n"
        message += "]"
        return message

    def __str__(self):
        return self.getGridsAsStr()

    def getGridSize(self):
        return self.boardInfo.gridSizeX, self.boardInfo.gridSizeY

    def containGrid(self, indexX: int, indexY: int):
        return 0 <= indexX and indexX < len(self.__grids) and 0 <= indexY and indexY < len(self.__grids[indexX])

    def getGrid(self, indexX: int, indexY: int):
        return self.__grids[indexX][indexY]

    def setGrid(self, indexX: int, indexY: int, newGrid: ReversiGrid, playAnimation: bool = True):
        lastGrid = self.__grids[indexX][indexY]
        self.__grids[indexX][indexY] = newGrid

        if playAnimation:
            if lastGrid.isEmpty and not newGrid.isEmpty:
                # todo play animation for new stone
                pass
            elif not lastGrid.isEmpty and not newGrid.isEmpty and lastGrid.stoneType != newGrid.stoneType:
                # todo play animation for flip
                pass

    def isOverReversiBoard(self, coordinate: Vector2):
        return self.boardInfo.boardOffset.x <= coordinate.x and coordinate.x <= self.boardInfo.boardOffset.x + self.boardInfo.gridWidth * self.boardInfo.gridSizeX and self.boardInfo.boardOffset.y <= coordinate.y and coordinate.y <= self.boardInfo.boardOffset.y + self.boardInfo.gridWidth * self.boardInfo.gridSizeY

    def getGridIndex(self, coordinate: Vector2):
        return (math.floor((coordinate.x - self.boardInfo.boardOffset.x) / self.boardInfo.gridWidth)
                , math.floor((coordinate.y - self.boardInfo.boardOffset.y) / self.boardInfo.gridWidth))

    def getPositionFromGridIndex(self, indexX: int, indexY: int):
        return (self.boardInfo.boardOffset.x + self.boardInfo.gridWidth * indexX + self.boardInfo.gridWidth / 2
                   , self.boardInfo.boardOffset.y + self.boardInfo.gridWidth * indexY + self.boardInfo.gridWidth / 2)

    # should be called every frame
    def update(self):
        # draw background color
        self.surface.fill(self.boardInfo.backgroundColor)

        self.drawGrids()
        self.drawStones()

    def drawGrids(self):
        # print("drawing grids: boardOffset=%s, gridWidth=%.1f" % (self.boardInfo.boardOffset, self.boardInfo.gridWidth))
    
        lineStart = Vector2()
        lineEnd = Vector2()
        
        # x if 0, y if 1
        for axis in range(2):
            numGrids_current = self.boardInfo.gridSizeX if axis == 0 else self.boardInfo.gridSizeY
            numGrids_opposite = self.boardInfo.gridSizeY if axis == 0 else self.boardInfo.gridSizeX
            numLoop = numGrids_current + 1
            oppositeAxis = 1 if axis == 0 else 0

            startValue_opposite = self.boardInfo.boardOffset[oppositeAxis]
            endValue_opposite = startValue_opposite + self.boardInfo.gridWidth * numGrids_opposite
        
            # print("axis=%d, numGrids_current=%d, numGrids_opposite=%d, numLoop=%d" % (axis, numGrids_current, numGrids_opposite, numLoop))
            # print("startValue_opposite=%.1f, endValue_opposite=%.1f" % (endValue_opposite, endValue_opposite))
        
            # 0 to numLoop
            for i in range(numLoop):
                value_current = self.boardInfo.boardOffset[axis] + self.boardInfo.gridWidth * i
            
                lineStart[axis] = value_current
                lineStart[oppositeAxis] = startValue_opposite
            
                lineEnd[axis] = value_current
                lineEnd[oppositeAxis] = endValue_opposite
                
                # print("lineStart=%s, lineEnd=%s" % (lineStart, lineEnd))
                pygame.draw.line(self.surface, self.boardInfo.gridColor, lineStart, lineEnd, 1)
    
    def drawStones(self):
        for x in range(0, self.boardInfo.gridSizeX):
            for y in range(0, self.boardInfo.gridSizeY):
                if self.containGrid(x, y):
                    grid = self.getGrid(x, y)
                    if not grid.isEmpty:
                        StoneColor = (0 ,0, 0) if grid.stoneType == StoneType.BlackStone else (255, 255, 255)
                        radius = self.boardInfo.gridWidth / 2.0 * 0.8
                        pygame.draw.circle(self.surface, StoneColor, self.getPositionFromGridIndex(x, y), radius)

    def canFlipStonesAt(self, indexX: int, indexY: int, stoneType: StoneType):
        return self.getFlipInfo(indexX, indexY, stoneType).getNumEndPoints() > 0

    def getFlipInfo(self, indexX: int, indexY: int, stoneType: StoneType):
        flipInfo = FlipInfo(indexX, indexY)

        # check 8 directions
        for x in range(-1, 2):
            for y in range(-1, 2):
                if x == 0 and y == 0: continue
                # print("getFlipDirection: (x,y) = (%d, %d)" % (x, y))
                
                # check if a stone of the same type exists as end point towards the direction, 
                # and at least one stone of the opposite type exists between start and end,
                # and no empty grid between them.
                # if that confition is met, then we can say that it is flippable
                hasOppositeStoneBtwStartAndEnd = False
                hasEndPoint = False
                hasEmptyGrid = False
                endPoint = (0, 0)
                posX, posY = indexX, indexY
                while self.containGrid(posX + x, posY + y):
                    posX += x
                    posY += y
                    grid = self.getGrid(posX, posY)

                    if grid.isEmpty:
                        hasEmptyGrid = True
                        break
                    elif grid.stoneType == stoneType:
                        hasEndPoint = True
                        endPoint = (posX, posY)
                        break
                    elif grid.stoneType != stoneType:
                        hasOppositeStoneBtwStartAndEnd = True

                if hasOppositeStoneBtwStartAndEnd and hasEndPoint and not hasEmptyGrid:
                    flipInfo.appendEndPoint(*endPoint)

        return flipInfo