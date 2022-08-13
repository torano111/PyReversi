from reversiGrid import ReversiGrid, StoneType

def convertGridToInt(grid: ReversiGrid):
    return 0 if grid.isEmpty else int(grid.stoneType)

def convertIntToGrid(value: int):
    if value == 0: return ReversiGrid()
    else: return ReversiGrid(False, StoneType(value))