from reversiGrid import ReversiGrid, StoneType
import pygame

def convertGridToInt(grid: ReversiGrid):
    return 0 if grid.isEmpty else int(grid.stoneType)

def convertIntToGrid(value: int):
    if value == 0: return ReversiGrid()
    else: return ReversiGrid(False, StoneType(value))

def loadImage(filename):
    try:
        surface = pygame.image.load(filename)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s' % (filename, pygame.get_error()))
    return surface.convert_alpha()

def loadImageScaled(filename, scale):
    return pygame.transform.scale(loadImage(filename), scale)