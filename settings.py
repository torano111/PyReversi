import pygame
import reversiGridsList

# Game in general
FRAME_RATE = 60.0
SEC_PER_FRAME = 1.0 / FRAME_RATE
SCREENRECT = pygame.Rect(0, 0, 600, 600)

# Board
BOARD_START_POS = pygame.Vector2(10, 10)
# BOARD_COLOR = pygame.Color(220, 220, 220)
BOARD_COLOR = pygame.Color(0, 255, 0)
INITIAL_GRIDS = reversiGridsList.reversiGrids
# INITIAL_GRIDS = reversiGridsList.testFlipGrids1
# INITIAL_GRIDS = reversiGridsList.testFlipGrids2

# Grids
GRID_SIZE_X = 8
GRID_SIZE_Y = 8
GRID_WIDTH = float(50)
GRID_COLOR = pygame.Color(0, 0, 0)

# flipping reversi
DIRECTORY_FLIPPING_REVERSI = "images\\flippingReversi\\"
ANIM_DURATION_FLIPPING_REVERSI = 1.0
FILES_FLIPPING_REVERSI = [
    "flippingReversi000.png",
    "flippingReversi001.png",
    "flippingReversi002.png",
    "flippingReversi003.png",
    "flippingReversi004.png",
    "flippingReversi005.png",
    "flippingReversi006.png",
    "flippingReversi007.png",
    "flippingReversi008.png",
    "flippingReversi009.png",
    "flippingReversi010.png",
]