from enum import IntEnum

class StoneType(IntEnum):
    BlackStone = 1,
    WhiteStone = 2,

class ReversiGrid:
    def __init__(self, isEmpty: bool = True, stoneType: StoneType = StoneType.BlackStone):
        self.isEmpty = isEmpty
        self.stoneType = stoneType

    def __str__(self):
        return "ReversiGrid: %s" % (self.stoneType)