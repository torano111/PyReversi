from reversiStoneType import StoneType
import pygame

def loadImage(filename):
    try:
        surface = pygame.image.load(filename)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s' % (filename, pygame.get_error()))
    return surface.convert_alpha()

def loadImageScaled(filename, scale):
    return pygame.transform.scale(loadImage(filename), scale)