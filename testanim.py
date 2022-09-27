import sys
import pygame
from pygame.math import Vector2
from reversiGrid import StoneType
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

    stone = FlippingReversiStone(stoneType=StoneType.BlackStone, imageScale=Vector2(settings.GRID_WIDTH * 0.8))
    stone.moveTo(Vector2(settings.SCREENRECT.width / 2 - stone.image.get_width() / 2, settings.SCREENRECT.height / 2 - stone.image.get_height() / 2))
    stone.setStoneType(StoneType.WhiteStone)
    
    renderGroups = RenderUpdates(stone)
    
    while True: 
        clock.tick(settings.FRAME_RATE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

        screen.blit(background, (0, 0))
        renderGroups.update()
        changedAreas = renderGroups.draw(screen)

        # pygame.display.update(changedAreas)
        pygame.display.update()
    
main()