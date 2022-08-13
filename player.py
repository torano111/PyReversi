
from reversiGrid import ReversiGrid, StoneType

class Player:
    def __init__(self, stoneType: StoneType):
        self.stoneType = stoneType

    def __str__(self):
        return "Player: stoneType=%s" % (self.stoneType)