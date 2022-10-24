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
    
    gm = GameManager(screen)
    gm.startGame()

    while gm.getGameState() != GameState.EndingGame: 
        deltaTime = clock.tick(settings.FRAME_RATE) / 1000.0
        gm.update(deltaTime)
        pygame.display.update()
        
    pygame.quit()
    sys.exit()
    
if __name__ == "__main__":
    main()