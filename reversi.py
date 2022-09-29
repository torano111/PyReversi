import sys
from turtle import width
import pygame
from pygame.math import Vector2
from gameManager import GameManager, GameState, PlayerActionType
from reversiBoard import ReversiBoardInfo, ReversiBoard
from reversiStoneType import StoneType
from player import Player
import reversiGridsList
import settings

# does initialization and operates game tick.
def main():
    pygame.init()
    
    screen = pygame.display.set_mode(settings.SCREENRECT.size)
    pygame.display.set_caption("Reversi")
    clock = pygame.time.Clock()
    
    player0 = Player(StoneType.WhiteStone)
    player1 = Player(StoneType.BlackStone)

    boardSizeOffset = 1 # offset for grids
    boardSurface = pygame.Surface((settings.GRID_WIDTH * settings.GRID_SIZE_X + boardSizeOffset, settings.GRID_WIDTH * settings.GRID_SIZE_Y + boardSizeOffset))
    boardSurface.convert()

    boardInfo = ReversiBoardInfo(Vector2(), settings.GRID_SIZE_X, settings.GRID_SIZE_Y, settings.GRID_WIDTH, settings.GRID_COLOR, settings.BOARD_COLOR)
    board = ReversiBoard(boardSurface, boardInfo)
    gm = GameManager(screen, board, player0, player1, settings.BOARD_START_POS)
    gm.StartGame(0, settings.INITIAL_GRIDS)

    while gm.getGameState() != GameState.EndingGame: 
        clock.tick(settings.FRAME_RATE)
        gm.update()
        pygame.display.update()
        
    pygame.quit()
    sys.exit()
    
if __name__ == "__main__":
    main()