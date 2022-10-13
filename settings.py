import pygame
import reversiGridsList

# Debugging
DEBUG_KEY = pygame.K_F1
DEBUG_NO_TURN_CHANGE = False
DEBUG_SHOW_GRIDS_EVERY_TURN = True

# Game in general
FRAME_RATE = 60.0
SEC_PER_FRAME = 1.0 / FRAME_RATE
SCREENRECT = pygame.Rect(0, 0, 600, 600)
SCREEN_COLOR = pygame.Color(99, 63, 32)

# Board
BOARD_START_POS = pygame.Vector2(10, 10)
BOARD_COLOR = pygame.Color(0, 255, 0)
INITIAL_GRIDS = reversiGridsList.reversiGrids
# INITIAL_GRIDS = reversiGridsList.testFlipGrids1
# INITIAL_GRIDS = reversiGridsList.testFlipGrids2
# INITIAL_GRIDS = reversiGridsList.testFlipGrids3
# INITIAL_GRIDS = reversiGridsList.testFlipGrids4

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

# Player Font
PLAYER_FONT_SIZE = 100
PLAYER_FONT_COORDINATE = (50, 500)
PLAYER_ICON_COORDINATE = (0, 500)

# Player 0
PLAYER_NAME_0 = "Player0"
PLAYER_ICON_FILEPATH_0 = "images\\flippingReversi\\flippingReversi000.png"
PLAYER_FONT_COLOR_0 = (255, 255, 255)

# Player 1
PLAYER_NAME_1 = "Player1"
PLAYER_ICON_FILEPATH_1 = "images\\flippingReversi\\flippingReversi010.png"
PLAYER_FONT_COLOR_1 = (0, 0, 0)