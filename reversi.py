import sys
from turtle import width
import pygame
from pygame.math import Vector2
import math

# Game in general
FRAME_RATE = 60

# Board
BOARD_START_POS = Vector2(10, 10)

# Grids
NUM_GRIDS_X = 8
NUM_GRIDS_Y = 8
GRID_WIDTH = float(50)
GRID_COLOR = pygame.Color(0, 0, 0)

# Reversi stone to draw
class StoneToDraw:
    def __init__(self, isBlack: bool, indexX: int, indexY: int):
        self.isBlack = isBlack
        self.indexX = indexX
        self.indexY = indexY
        # self.debugPrint()
        
    def debugPrint(self):
        print("Debugging a stone: isBlack=%s, Index=(%d, %d)" % (("True" if self.isBlack else "False"), self.indexX, self.indexY))

def onLeftMouseButtonClicked(posX: int, posY: int):
    # print("mousePos=(%d, %d)" % (posX, posY))
    pass
    # todo

def IsOverReversiBoard(coordinate: Vector2):
    return BOARD_START_POS.x <= coordinate.x and coordinate.x <= BOARD_START_POS.x + GRID_WIDTH * NUM_GRIDS_X and BOARD_START_POS.y <= coordinate.y and coordinate.y <= BOARD_START_POS.y + GRID_WIDTH * NUM_GRIDS_Y

def GetGridIndex(coordinate: Vector2):
    return (math.floor((coordinate.x - BOARD_START_POS.x) / GRID_WIDTH)
            , math.floor((coordinate.y - BOARD_START_POS.y) / GRID_WIDTH))

def GetPositionFromGridIndex(indexX: int, indexY: int):
    return Vector2(BOARD_START_POS.x + GRID_WIDTH * indexX + GRID_WIDTH / 2
                   , BOARD_START_POS.y + GRID_WIDTH * indexY + GRID_WIDTH / 2)

def drawReversiStone(drawnSurface: pygame.Surface, stone: StoneToDraw):
    radius = 20
    StoneColor = (0 ,0, 0) if stone.isBlack else (255, 255, 255)
    pygame.draw.circle(drawnSurface, StoneColor, GetPositionFromGridIndex(stone.indexX, stone.indexY), radius)

def drawReversiBoard(drawnSurface: pygame.Surface):
    # todo draw a green board
    drawGrids(drawnSurface, BOARD_START_POS, GRID_WIDTH)
    
def drawGrids(drawnSurface: pygame.Surface, startPos: Vector2, gridWidth: int):
    # print("drawing grids: startPos=%s, width=%.1f" % (startPos, width))
    
    lineStart = Vector2()
    lineEnd = Vector2()
    # x if 0, y if 1
    for axis in range(2):
        numGrids_current = NUM_GRIDS_X if axis == 0 else NUM_GRIDS_Y
        numGrids_opposite = NUM_GRIDS_Y if axis == 0 else NUM_GRIDS_X
        numLoop = numGrids_current + 1
        oppositeAxis = 1 if axis == 0 else 0
        
        startValue_opposite = startPos[oppositeAxis]
        endValue_opposite = startValue_opposite + gridWidth * numGrids_opposite
        
        # print("axis=%d, numGrids_current=%d, numGrids_opposite=%d, numLoop=%d" % (axis, numGrids_current, numGrids_opposite, numLoop))
        # print("startValue_opposite=%.1f, endValue_opposite=%.1f" % (endValue_opposite, endValue_opposite))
        
        # 0 to numLoop
        for i in range(numLoop):
            # if isX:
            #     lineStart = Vector2(0, 0)
            #     lineEnd = Vector2(0, 0)
            # else:
            #     lineStart = Vector2(0, 0)
            #     lineEnd = Vector2(0, 0)
            
            value_current = startPos[axis] + gridWidth * i
            
            lineStart[axis] = value_current
            lineStart[oppositeAxis] = startValue_opposite
            
            lineEnd[axis] = value_current
            lineEnd[oppositeAxis] = endValue_opposite
                
            # print("lineStart=%s, lineEnd=%s" % (lineStart, lineEnd))
            pygame.draw.line(drawnSurface, GRID_COLOR, lineStart, lineEnd, 1)

def main():
    pygame.init()
    
    display_x, display_y = (600, 600)
    main_surface = pygame.display.set_mode((display_x, display_y))
    pygame.display.set_caption("Reverse")
    clock = pygame.time.Clock()
    
    # # pygame.mouse.set_visible(False)
    # # pygame.event.set_grab(True)
    
    stonesToDraw = []
    
    runningGame = True
    while runningGame: 
        clock.tick(FRAME_RATE)
         
        mousePos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runningGame = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                runningGame = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:    # left mouse button
                onLeftMouseButtonClicked(*mousePos)
                
                if IsOverReversiBoard(Vector2(mousePos)):
                    stone = StoneToDraw(False, *(GetGridIndex(Vector2(mousePos))))
                    stonesToDraw.append(stone)
                    stone.debugPrint()
            
        if not runningGame: break
        
        # draw background color
        main_surface.fill((220, 220, 220))
        
        drawReversiBoard(main_surface)
        
        for stone in stonesToDraw:
            drawReversiStone(main_surface, stone)
        
        # drawReversiStone(False, main_surface, Vector2(display_x / 2, display_y / 2))
        
        pygame.display.update()
        
    pygame.quit()
    sys.exit()
    
if __name__ == "__main__":
    main()