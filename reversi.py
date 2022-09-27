import sys
from turtle import width
import pygame
from pygame.math import Vector2
from gameManager import GameManager, GameState, PlayerActionType
from reversiBoard import ReversiBoardInfo, ReversiBoard
from reversiGrid import ReversiGrid, StoneType
from player import Player
import reversiGridsList
import settings

# does initialization and operates game tick.
def main():
    pygame.init()
    
    screen = pygame.display.set_mode(settings.SCREENRECT.size)
    pygame.display.set_caption("Reversi")
    clock = pygame.time.Clock()
    
    # # pygame.mouse.set_visible(False)
    # # pygame.event.set_grab(True)
    
    player0 = Player(StoneType.BlackStone)
    player1 = Player(StoneType.WhiteStone)

    boardInfo = ReversiBoardInfo(settings.BOARD_START_POS, settings.GRID_SIZE_X, settings.GRID_SIZE_Y, settings.GRID_WIDTH, settings.GRID_COLOR, settings.BOARD_COLOR)
    board = ReversiBoard(screen, boardInfo)
    gm = GameManager(board, player0, player1)
    gm.StartGame(0, settings.INITIAL_GRIDS)

    # background = pygame.Surface((300, 300))
    # background.convert()
    # background.fill((0, 255, 0))

    while gm.getGameState() != GameState.EndingGame: 
        clock.tick(settings.FRAME_RATE)
        gm.update()
        # screen.blit(background, (0, 0))
        pygame.display.update()
        
    pygame.quit()
    sys.exit()
    
if __name__ == "__main__":
    main()