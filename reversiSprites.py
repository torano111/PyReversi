import pygame
from pygame.sprite import Sprite
from pygame import Vector2
from reversiGrid import StoneType
import settings
import reversiUtility

class ReversiSprite(Sprite):
    def __init__(self, images = [], initImageIdx: int = 0, initLocation: Vector2 = Vector2(0, 0)):
        Sprite.__init__(self)
        self._images = images
        self.setCurrentImage(initImageIdx)
        self.rect = self.image.get_rect()
        self.moveTo(initLocation)
        self._animatingImages = False
        self.numTotalFrameToAnimate: float = 0
        self.loopAnimation = False
        self.reverseAnimation = False

    def setCurrentImage(self, index: int):
        self.image = self._images[index]
        self._imageIdx = index
        self._elapsedAnimationFrame = 0

    def getCurrentImage(self):
        return self.image

    def getImageIndex(self):
        return self._imageIdx

    def moveTo(self, newLocation):
        self.rect.move_ip(newLocation)

    def startAnimate(self):
        self._animatingImages = True

    def stopAnimate(self):
        self._animatingImages = False

    def isAnimating(self):
        return self._animatingImages

    def update(self, *args, **kwargs):
        numImages = len(self._images)
        if self._animatingImages and numImages > 0:
            framesPerImage: float = self.numTotalFrameToAnimate / float(numImages)
            if self._elapsedAnimationFrame >= framesPerImage:
                self._elapsedAnimationFrame = 0
                nextIdx = self._imageIdx - 1 if self.reverseAnimation else self._imageIdx + 1
                if 0<= nextIdx and nextIdx < numImages:
                    self.setCurrentImage(nextIdx)
                else:
                    if self.loopAnimation:
                        # restart
                        self.setCurrentImage(0 if self.reverseAnimation else len(self._images) - 1)
                    else:
                        self._animatingImages = False

            else:
                self._elapsedAnimationFrame += 1


class ReversiStone(ReversiSprite):
    def __init__(self, stoneType, images = [], initImageIdx: int = 0, initLocation: Vector2 = Vector2(0, 0)):
        ReversiSprite.__init__(self, images=images, initImageIdx=initImageIdx, initLocation=initLocation)
        self.stoneType = stoneType

class FlippingReversiStone(ReversiStone):
    loadedImages = []
    def __init__(self, stoneType, imageScale, initLocation: Vector2 = Vector2(0, 0)):
        if len(FlippingReversiStone.loadedImages) == 0:
            for filename in settings.FILES_FLIPPING_REVERSI:
                img = reversiUtility.loadImageScaled(settings.DIRECTORY_FLIPPING_REVERSI + filename, imageScale)
                FlippingReversiStone.loadedImages.append(img)

        initIdx = 0 if stoneType == StoneType.WhiteStone else len(FlippingReversiStone.loadedImages) - 1
        ReversiStone.__init__(self, stoneType=stoneType, images=FlippingReversiStone.loadedImages, initImageIdx=initIdx, initLocation=initLocation)
        self.numTotalFrameToAnimate = settings.ANIM_DURATION_FLIPPING_REVERSI / settings.SEC_PER_FRAME
        self.loopAnimation = False
        self.lastStoneType = self.stoneType
        self.reverseAnimation = False if stoneType == StoneType.WhiteStone else True

    def setStoneType(self, stoneType: StoneType, animate: bool = True):
        if self.stoneType != stoneType:
            self.lastStoneType = self.stoneType
            self.stoneType = stoneType
            if animate:
                self.startAnimate()
