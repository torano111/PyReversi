from reversiStoneType import StoneType

class ReversiGrid:
    def __init__(self, isEmpty: bool = True, stoneType: StoneType = StoneType.BlackStone):
        self.isEmpty = isEmpty
        self.stoneType = stoneType

    def __str__(self):
        return "ReversiGrid: %s" % (self.stoneType)

    def ToInt(self):
        return 0 if self.isEmpty else int(self.stoneType)

    @classmethod
    def ToGrid(cls, value: int):
        if value == 0: return ReversiGrid(isEmpty=True)
        else: return ReversiGrid(isEmpty=False, stoneType=StoneType(value))