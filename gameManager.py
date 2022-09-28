from reversiBoard import ReversiBoard, FlipInfo
from enum import IntEnum
from player import Player
import pygame
from pygame.math import Vector2
from reversiGrid import ReversiGrid, StoneType
import reversiUtility
from pygame import Surface

DEBUG_KEY = pygame.K_F1
DEBUG_NO_TURN_CHANGE = False

class PlayerActionType(IntEnum):
    Nothing = 0,
    PutStone = 1,

class GameState(IntEnum):
    Initializing = 1,
    WaitingForPlayer = 2,
    WaitingForGame = 3,
    EndingGame = 4,

# Handles Reversi game logic
class GameManager:
    def __init__(self, surface: Surface, board: ReversiBoard, firstPlayer: Player, secondPlayer: Player, boardOffset: Vector2):
        self.mainSurface = surface
        self.board = board
        self.__players = [firstPlayer, secondPlayer]
        self.__gameState = GameState.Initializing
        self.__curPlayerIdx = 0 
        self.boardOffset = boardOffset

    def getPlayer(self, index: int):
        return self.__players[index]

    def getCurrentPlayer(self):
        return self.getPlayer(self.__curPlayerIdx)

    def getGameState(self):
        return self.__gameState

    def __changePlayerTurn(self):
        lastPlayerIdx = self.__curPlayerIdx
        self.__curPlayerIdx = 0 if len(self.__players) <= self.__curPlayerIdx + 1 else self.__curPlayerIdx + 1

        print("changed player turn %d -> %d %s" % (lastPlayerIdx, self.__curPlayerIdx, self.getCurrentPlayer()))

    def StartGame(self, startPlayerIdx: int = 0, initialGrids = []):
        if self.__gameState == GameState.Initializing:
            self.__curPlayerIdx = startPlayerIdx
            sizeX, sizeY = self.board.getGridSize(); 

            # check initGrids
            isValidArray = True
            if len(initialGrids) != sizeX:
                isValidArray = False
            else:
                for x in range(0, sizeX):
                    if len(initialGrids[x]) != sizeY:
                        isValidArray = False
                        break

            # initialize grids
            if isValidArray:
                for x in range(0, sizeX):
                    for y in range(0, sizeY):
                        grid = reversiUtility.convertIntToGrid(initialGrids[x][y])
                        self.board.setGrid(x, y, grid, False)

            self.__gameState = GameState.WaitingForPlayer
            self.board.update()

    # should be called every tick
    def update(self):
        for event in pygame.event.get():
            # debug game
            if event.type == pygame.KEYDOWN and event.key == DEBUG_KEY:
                print("Debug Reversi:\n")
                print(self.board)

            # finish game
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.__gameState = GameState.EndingGame
                return
            # check player input
            elif self.__gameState == GameState.WaitingForPlayer:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:    # left mouse button
                    self.__gameState = GameState.WaitingForGame
                    self.handlePlayerAction(PlayerActionType.PutStone)

                    # todo comment out this and do animation.
                    self.__gameState = GameState.WaitingForPlayer

        self.mainSurface.fill((220, 220, 220))
        self.mainSurface.blit(self.board.surface, self.boardOffset)
        self.board.update()

    def handlePlayerAction(self, action: PlayerActionType):
        player = self.getCurrentPlayer()

        if action == PlayerActionType.PutStone:
            mousePos = pygame.mouse.get_pos()
            if self.board.isOverReversiBoard(Vector2(mousePos) - self.boardOffset):
                    mouseIndexX, mouseIndexY = self.board.getGridIndex(Vector2(mousePos) - self.boardOffset)
                    lastGrid = self.board.getGrid(mouseIndexX, mouseIndexY)
                    newGrid = ReversiGrid(False, player.stoneType)
                    
                    if lastGrid.isEmpty:
                        flipInfo = self.board.getFlipInfo(mouseIndexX, mouseIndexY, player.stoneType)
                        if flipInfo.getNumEndPoints() <= 0:
                            print("Couldn't put stone at (%d, %d) because no stone can be flipped.")
                            return
                        
                        self.board.setGrid(mouseIndexX, mouseIndexY, newGrid, True)
                        print("Player %d put a stone(%s) at (%d, %d)" % (self.__curPlayerIdx, newGrid.stoneType, mouseIndexX, mouseIndexY))

                        # flip
                        print("flipInfo " + str(flipInfo))
                        for endIdx in range(0, flipInfo.getNumEndPoints()):
                            innerPoints = flipInfo.getInnerPoints(endIdx)
                            for inrPts in innerPoints:
                                self.board.setGrid(inrPts[0], inrPts[1], newGrid, True)

                        # todo check if the other player can put a stone before changing the turn. if not, skip his turn.
                        if not DEBUG_NO_TURN_CHANGE: self.__changePlayerTurn()
                        print("") # space