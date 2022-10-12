
from reversiGrid import StoneType
import reversiUtility
from pygame import Vector2, Color

class Player:
    def __init__(self, stoneType: StoneType, name: str, fontColor: Color, iconPath: str, iconSize: Vector2):
        self.stoneType = stoneType
        self.name = name
        self.fontColor = fontColor
        self.icon = reversiUtility.loadImageScaled(iconPath, iconSize)

    def __str__(self):
        return "Player: stoneType=%s" % (self.stoneType)