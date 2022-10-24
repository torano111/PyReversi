import sys
from turtle import width
import pygame
from pygame.math import Vector2
from gameManager import GameManager, GameState
from reversiBoard import ReversiBoardInfo, ReversiBoard
from reversiStoneType import StoneType
from player import Player
import settings

# does initialization and operates game tick.
def main():
    pygame.init()
    
    screen = pygame.display.set_mode(settings.SCREENRECT.size)
    pygame.display.set_caption("Reversi")
    clock = pygame.time.Clock()
    
    IconSize = (settings.PLAYER_FONT_SIZE / 2.0, settings.PLAYER_FONT_SIZE / 2.0)
    player0 = Player(StoneType.WhiteStone, settings.PLAYER_NAME_0, settings.PLAYER_FONT_COLOR_0, settings.PLAYER_ICON_FILEPATH_0, IconSize)
    player1 = Player(StoneType.BlackStone, settings.PLAYER_NAME_1, settings.PLAYER_FONT_COLOR_1, settings.PLAYER_ICON_FILEPATH_1, IconSize)

    boardSizeOffset = 1 # offset for grids
    boardSurface = pygame.Surface((settings.GRID_WIDTH * settings.GRID_SIZE_X + boardSizeOffset, settings.GRID_WIDTH * settings.GRID_SIZE_Y + boardSizeOffset))
    boardSurface.convert()

    boardInfo = ReversiBoardInfo(Vector2(), settings.GRID_SIZE_X, settings.GRID_SIZE_Y, settings.GRID_WIDTH, settings.GRID_COLOR, settings.BOARD_COLOR)
    board = ReversiBoard(boardSurface, boardInfo)
    gm = GameManager(screen, board, player0, player1, settings.BOARD_START_POS)
    gm.StartGame(0, settings.INITIAL_GRIDS)

    while gm.getGameState() != GameState.EndingGame: 
        deltaTime = clock.tick(settings.FRAME_RATE) / 1000.0
        gm.update(deltaTime)
        pygame.display.update()
        
    pygame.quit()
    sys.exit()
    
if __name__ == "__main__":
    main()