import sys
from turtle import width
import pygame
from pygame.math import Vector2
from gameManager import GameManager, GameState, PlayerActionType
from reversiBoard import ReversiBoardInfo, ReversiBoard
from reversiGrid import ReversiGrid, StoneType
from player import Player
import reversiGridsList

# Game in general
FRAME_RATE = 60
DISPLAY_X = 600
DISPLAY_Y = 600

# Board
BOARD_START_POS = Vector2(10, 10)
BOARD_COLOR = pygame.Color(220, 220, 220)
INITIAL_GRIDS = reversiGridsList.reversiGrids
# INITIAL_GRIDS = reversiGridsList.testFlipGrids1
# INITIAL_GRIDS = reversiGridsList.testFlipGrids2

# Grids
GRID_SIZE_X = 8
GRID_SIZE_Y = 8
GRID_WIDTH = float(50)
GRID_COLOR = pygame.Color(0, 0, 0)

# does initialization and operates game tick.
def main():
    pygame.init()
    
    main_surface = pygame.display.set_mode((DISPLAY_X, DISPLAY_Y))
    pygame.display.set_caption("Reversi")
    clock = pygame.time.Clock()
    
    # # pygame.mouse.set_visible(False)
    # # pygame.event.set_grab(True)
    
    player0 = Player(StoneType.BlackStone)
    player1 = Player(StoneType.WhiteStone)

    boardInfo = ReversiBoardInfo(BOARD_START_POS, GRID_SIZE_X, GRID_SIZE_Y, GRID_WIDTH, GRID_COLOR, BOARD_COLOR)
    board = ReversiBoard(main_surface, boardInfo)
    gm = GameManager(board, player0, player1)
    gm.StartGame(0, INITIAL_GRIDS)

    while gm.getGameState() != GameState.EndingGame: 
        clock.tick(FRAME_RATE)
        gm.update()
        pygame.display.update()
        
    pygame.quit()
    sys.exit()
    
if __name__ == "__main__":
    main()