from reversiBoard import ReversiBoard, FlipInfo
from enum import IntEnum
from player import Player
import pygame
from pygame.math import Vector2
from reversiGrid import ReversiGrid
from pygame import Surface
from reversiStoneType import StoneType
import settings

class PlayerActionType(IntEnum):
    Nothing = 0,
    PutStone = 1,

class GameState(IntEnum):
    Initializing = 1,
    WaitingForPlayer = 2,
    WaitingForGame = 3,
    ShowResult = 4
    EndingGame = 5,

class GameResult:
    def __init__(self, showPlayer0ResultDelay = 1.0, showPlayer1ResultDelay = 1.0, showWinnerDelay = 1.0):
        self.showPlayer0Result = False
        self.showPlayer0ResultDelay = showPlayer0ResultDelay
        self.showPlayer1Result = False
        self.showPlayer1ResultDelay = showPlayer1ResultDelay
        self.showWinner = False
        self.showWinnerDelay = showWinnerDelay
        self.timeElapsed = 0.0
        self.player0Score = 0
        self.player1Score = 0
        self.winner = -1

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
        self.__gameResult = GameResult(1, 1, 1)

    def getPlayer(self, index: int):
        return self.__players[index]

    def getCurrentPlayer(self):
        return self.getPlayer(self.__curPlayerIdx)

    def getOtherPlayer(self):
        return self.getPlayer(self.getOtherPlayerIndex(self.__curPlayerIdx))

    def getGameState(self):
        return self.__gameState

    def getOtherPlayerIndex(self, idx):
        return 0 if len(self.__players) <= idx + 1 else idx + 1

    def __changePlayerTurn(self):
        lastPlayerIdx = self.__curPlayerIdx
        self.__curPlayerIdx = self.getOtherPlayerIndex(self.__curPlayerIdx)

        print("changed player turn %d -> %d %s" % (lastPlayerIdx, self.__curPlayerIdx, self.getCurrentPlayer()))

    def StartGame(self, startPlayerIdx: int = 0, initialGrids = []):
        if self.__gameState == GameState.Initializing:
            self.__curPlayerIdx = startPlayerIdx
            # x and y inversed
            sizeY, sizeX = self.board.getGridSize(); 

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
                        # x and y inversed
                        self.board.setGrid(y, x, grid, False)

            self.__gameState = GameState.WaitingForPlayer
            self.board.update()

            if settings.DEBUG_SHOW_GRIDS_EVERY_TURN:
                print(self.board)

    # should be called every tick
    def update(self, deltaTime):
        for event in pygame.event.get():
            # debug game
            if event.type == pygame.KEYDOWN and event.key == settings.DEBUG_KEY:
                print("Debug Reversi:\n")
                print(self.board)

            # finish game
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.__gameState = GameState.EndingGame
                return
            # check player input
            elif self.__gameState == GameState.WaitingForPlayer:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:    # left mouse button
                    self.handlePlayerAction(PlayerActionType.PutStone)

        if self.__gameState == GameState.WaitingForGame:
            self.handleFlipAnimation()

        self.mainSurface.fill(settings.SCREEN_COLOR)
        self.board.update()

        if self.__gameState == GameState.ShowResult:
            self.showResult(deltaTime)

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
                            print("Couldn't put stone at (%d, %d) because no stone can be flipped." % (mouseIndexX, mouseIndexY))
                            return
                        
                        # place a stone
                        self.board.setGrid(mouseIndexX, mouseIndexY, newGrid, False)
                        self.flipStoneType = newGrid.stoneType
                        self.flippingStoneInfos.clear()
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

        if len(self.flippingStoneInfos) == 0:
            self.onEndPlayerTurn()

    def onEndPlayerTurn(self):
        self.__gameState = GameState.WaitingForPlayer

        # change the player turn
        if not settings.DEBUG_NO_TURN_CHANGE and self.canPlayerPutStone(self.getOtherPlayer()):
            if settings.DEBUG_SHOW_GRIDS_EVERY_TURN:
                print(self.board)
                
            self.__changePlayerTurn()
        elif not self.canPlayerPutStone(self.getCurrentPlayer()):
            self.__gameState = GameState.ShowResult
        else:
            print("Player %d turn still continues. player %d turn was skipped!" % (self.__curPlayerIdx, self.getOtherPlayerIndex(self.__curPlayerIdx)))


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

    def canPlayerPutStone(self, player: Player):
        gridSizeX, gridSizeY = self.board.getGridSize()
        for x in range(gridSizeX):
            for y in range(gridSizeY):
                grid = self.board.getGrid(x, y)
                if not grid.isEmpty: continue
                
                flipInfo = self.board.getFlipInfo(x, y, player.stoneType)
                if flipInfo.getNumEndPoints() > 0:
                # if self.board.canFlipStonesAt(x, y, player.stoneType):
                    print("Player can put stone at (%d, %d)!" % (x, y))
                    return True

        return False

    def showResult(self, deltaTime):
        # print("finished game! showing the result.")

        # player 0 result
        if self.__gameResult.showPlayer0Result:
            curPlayer = self.getPlayer(0)
            font = pygame.font.Font(None, settings.RESULT_FONT_SIZE)
            text = curPlayer.name + ": " + str(self.__gameResult.player0Score)
            textSurface = font.render(text, 1, settings.RESULT_FONT_COLOR)
            self.mainSurface.blit(textSurface, settings.RESULT_FONT_COORDINATE)
        elif self.__gameResult.timeElapsed >= self.__gameResult.showPlayer0ResultDelay:
            self.__gameResult.showPlayer0Result = True
            self.__gameResult.timeElapsed = 0.0

            self.__gameResult.player0Score = self.board.getNumStones(self.__players[0].stoneType)
            print("Player 0 score: %d" % (self.__gameResult.player0Score))
            return

        # player 1 result
        if self.__gameResult.showPlayer1Result:
            curPlayer = self.getPlayer(1)
            font = pygame.font.Font(None, settings.RESULT_FONT_SIZE)
            text = curPlayer.name + ": " + str(self.__gameResult.player1Score)
            textSurface = font.render(text, 1, settings.RESULT_FONT_COLOR)
            self.mainSurface.blit(textSurface, settings.RESULT_FONT_COORDINATE + settings.RESULT_FONT_COORDINATE_OFFSET)
        elif self.__gameResult.timeElapsed >= self.__gameResult.showPlayer1ResultDelay:
            self.__gameResult.showPlayer1Result = True
            self.__gameResult.timeElapsed = 0.0

            self.__gameResult.player1Score = self.board.getNumStones(self.__players[1].stoneType)
            print("Player 1 score: %d" % (self.__gameResult.player1Score))
            return

        # winner
        if self.__gameResult.showWinner:
            curPlayer = self.getPlayer(1)
            font = pygame.font.Font(None, settings.RESULT_FONT_SIZE)
            prefix = "Result: "
            if self.__gameResult.winner == 0 or self.__gameResult.winner == 1:
                text = prefix + self.getPlayer(self.__gameResult.winner).name
            else:
                text = prefix + "Draw"
            textSurface = font.render(text, 1, settings.RESULT_FONT_COLOR)
            self.mainSurface.blit(textSurface, settings.RESULT_FONT_COORDINATE + settings.RESULT_FONT_COORDINATE_OFFSET * 2)
        elif self.__gameResult.timeElapsed >= self.__gameResult.showWinnerDelay:
            self.__gameResult.showWinner = True
            self.__gameResult.timeElapsed = 0.0

            if self.__gameResult.player0Score == self.__gameResult.player1Score:
                self.__gameResult.winner = -1   # draw
            elif self.__gameResult.player0Score > self.__gameResult.player1Score:
                self.__gameResult.winner = 0
            else: #self.__gameResult.player0Score < self.__gameResult.player1Score: self.__gameResult.winner 
                self.__gameResult.winner = 1
            
            print("Winner: %d" % (self.__gameResult.winner))
            return

        self.__gameResult.timeElapsed += deltaTime