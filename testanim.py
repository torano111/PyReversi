import sys
import pygame
from pygame.math import Vector2
from reversiStoneType import StoneType
import reversiUtility
import settings
from reversiSprites import FlippingReversiStone
from pygame.sprite import Group, GroupSingle, RenderUpdates

# does initialization and operates game tick.
def main():
    pygame.init()
    
    screen = pygame.display.set_mode(settings.SCREENRECT.size)
    pygame.display.set_caption("Reversi")
    clock = pygame.time.Clock()

    background = pygame.Surface(screen.get_size())
    background.convert()
    background.fill((0, 220, 220))
    screen.blit(background, (0, 0))

    stones = []
    stone0 = FlippingReversiStone(stoneType=StoneType.BlackStone, imageScale=Vector2(settings.GRID_WIDTH * 0.8))
    stone0.moveTo(Vector2(settings.SCREENRECT.width / 2 - stone0.image.get_width(), settings.SCREENRECT.height / 2 - stone0.image.get_height()))

    stone1 = FlippingReversiStone(stoneType=StoneType.WhiteStone, imageScale=Vector2(settings.GRID_WIDTH * 0.8))
    stone1.moveTo(Vector2(settings.SCREENRECT.width / 2, settings.SCREENRECT.height / 2))

    stones.append(stone0)
    stones.append(stone1)
    
    renderGroups = RenderUpdates(stone0, stone1)
    
    while True: 
        clock.tick(settings.FRAME_RATE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

            # click to flip stones
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:    # left mouse button
                hasAnimatingStone = False
                for stone in stones:
                    if stone.isAnimating():
                        hasAnimatingStone = True
                        break
                
                if not hasAnimatingStone:
                    for stone in stones:
                        newStoneType = StoneType.WhiteStone if stone.stoneType == StoneType.BlackStone else StoneType.BlackStone
                        stone.setStoneType(newStoneType, True)
                
        screen.blit(background, (0, 0))
        renderGroups.update()
        changedAreas = renderGroups.draw(screen)

        # pygame.display.update(changedAreas)
        pygame.display.update()
    
main()