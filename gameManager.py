from reversiBoard import ReversiBoard, FlipInfo
from enum import IntEnum
from player import Player
import pygame
from pygame.math import Vector2
from reversiGrid import ReversiGrid
from pygame import Surface
from reversiStoneType import StoneType
import settings

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
        self.flippingStoneInfos = []
        self.flipStoneType = StoneType.BlackStone

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
                        grid = ReversiGrid.ToGrid(initialGrids[x][y])
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
                    # self.__gameState = GameState.WaitingForGame
                    self.handlePlayerAction(PlayerActionType.PutStone)

                    # todo comment out this and do animation.
                    # self.__gameState = GameState.WaitingForPlayer
        
        if self.__gameState == GameState.WaitingForGame:
            self.handleFlipAnimation()

        self.mainSurface.fill(settings.SCREEN_COLOR)
        self.board.update()
        self.mainSurface.blit(self.board.surface, self.boardOffset)

        self.showCurrentPlayerNameAndIcon()

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
                        
                        # place a stone
                        self.board.setGrid(mouseIndexX, mouseIndexY, newGrid, False)
                        self.flipStoneType = newGrid.stoneType
                        self.flippingStoneInfos.clear()
                        # self.flippingStoneInfos.append((mouseIndexX, mouseIndexY))
                        print("Player %d put a stone(%s) at (%d, %d)" % (self.__curPlayerIdx, newGrid.stoneType, mouseIndexX, mouseIndexY))

                        # flip stones
                        print("flipInfo " + str(flipInfo))
                        for endIdx in range(0, flipInfo.getNumEndPoints()):
                            innerPoints = flipInfo.getInnerPoints(endIdx)
                            for inrPts in innerPoints:
                                if self.board.containGrid(inrPts[0], inrPts[1]):
                                    # gridToFlip = ReversiGrid(False, player.stoneType)
                                    # self.board.setGrid(inrPts[0], inrPts[1], gridToFlip, True)
                                    self.flippingStoneInfos.append(inrPts)

                        # todo check if the other player can put a stone before changing the turn. if not, skip his turn.
                        # if not DEBUG_NO_TURN_CHANGE: self.__changePlayerTurn()
                        print("") # space
                        self.__gameState = GameState.WaitingForGame

    def handleFlipAnimation(self):
        if len(self.flippingStoneInfos) > 0:
            flipInfo = self.flippingStoneInfos[0]
            if self.board.containGrid(flipInfo[0], flipInfo[1]):
                    flippingSprite = self.board.getSprite(flipInfo[0], flipInfo[1])
                    if not flippingSprite.isAnimating():
                        if flippingSprite.stoneType == self.flipStoneType:
                            # done animating
                            self.flippingStoneInfos.pop(0)
                        else:
                            # start animating
                            gridToFlip = ReversiGrid(False, self.flipStoneType)
                            self.board.setGrid(flipInfo[0], flipInfo[1], gridToFlip, True)
            else:
                print("error: reversi board doesn't contain (%d, %d)" % (flipInfo[0], flipInfo[1]))

        # change the player turn
        if len(self.flippingStoneInfos) == 0:
            self.__gameState = GameState.WaitingForPlayer

            if DEBUG_NO_TURN_CHANGE: return
            
            self.__changePlayerTurn()

    def showCurrentPlayerNameAndIcon(self):
        curPlayer = self.getCurrentPlayer()

        # Icon
        self.mainSurface.blit(curPlayer.icon, settings.PLAYER_ICON_COORDINATE)
        
        # Font
        fontColor = curPlayer.fontColor
        font = pygame.font.Font(None, settings.PLAYER_FONT_SIZE)
        text = curPlayer.name
        size = font.size(text)
        textSurface = font.render(text, 1, fontColor)
        self.mainSurface.blit(textSurface, settings.PLAYER_FONT_COORDINATE)