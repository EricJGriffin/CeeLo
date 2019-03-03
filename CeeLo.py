# CeeLo.py
from random import randrange
from graphics import *
from dieview2 import DieView
from button import Button

class Dice:

    def __init__(self):
        self.dice = [0]*3
        self.rollAll()

    def rollAll(self):
        self.roll(range(3))

    def roll(self, which):
        for pos in which:
            self.dice[pos] = randrange(1,7)

    def values(self):
        return self.dice[:]

    def score(self):
        counts = [0] * 7
        for value in self.dice:
            counts[value] = counts[value] + 1
            
        # each outcome will have an assigned ranking
        if 4 in self.dice and 5 in self.dice and 6 in self.dice:
            return "Automatic Win", 13

        elif 1 in self.dice and 2 in self.dice and 3 in self.dice:
            return "Automatic Loss", 0
        
        elif 3 in counts:
            if self.dice[0] == 1:
                return "Trip Ones", 7
            elif self.dice[0] == 2:
                return "Trip Twos", 8
            elif self.dice[0] == 3:
                return "Trip Threes", 9
            elif self.dice[0] == 4:
                return "Trip Fours", 10
            elif self.dice[0] == 5:
                return "Trip Fives", 11
            elif self.dice[0] == 6:
                return "Trip Sixes", 12

        elif 2 in counts:
            firstVal = self.dice[0]
            if firstVal == self.dice[1]:
                myNum = self.dice[2]
            elif firstVal == self.dice[2]:
                myNum = self.dice[1]
            else:
                myNum = self.dice[0]

            if myNum == 1:
                return "One", 1
            elif myNum == 2:
                return "Two", 2
            elif myNum == 3:
                return "Three", 3
            elif myNum == 4:
                return "Four", 4
            elif myNum == 5:
                return "Five", 5
            elif myNum == 6:
                return "Six", 6
        else:
            return "Garbage", 0

class Player:
    def __init__(self):
        self.money = 100
        self.dice = Dice()

    def values(self):
        return self.dice.values()

    def winsPot(self, pot):
        self.money = self.money + pot

    def subtract(self, amt):
        self.money = self.money - amt

    def getMoney(self):
        return self.money

    def playerRoll(self):
        result = "Garbage"
        while result == "Garbage":
            self.dice.rollAll()
            result, score = self.playerScore()
        

    def playerScore(self):
        result, score = self.dice.score()
        return result, score

    
class CeeLo:
    def __init__(self, interface, players):
        #self.dice = Dice()
        self.interface = interface
        self.playerList = []
        for i in range(players):
            self.playerList.append(Player())
        
    def run(self):
        while self.interface.continuePlaying(): 
            self.playRound()
        self.interface.close()

    
    def playRound(self):
        self.interface.activePlayers(self.playerList) 
        potCount = 0
        for i, player in enumerate(self.playerList):
            self.interface.displayMoney(i, player.getMoney()) 
            self.interface.currentPlayer(i)                 
            if self.interface.roll() and (player.getMoney() >= 10):  
                player.subtract(10)
                potCount = potCount + 1
                player.playerRoll()
                self.interface.displayResult(i, player) 
                self.interface.displayMoney(i, player.getMoney())
            self.interface.resetPlayerColor(i) 
        winner, addedPotCnt = self.determineWinner()
        potCount = potCount + addedPotCnt
        self.interface.displayWinner(winner)
        self.awardWinner(winner, potCount) 
        for i, player in enumerate(self.playerList):
            self.interface.displayMoney(i, player.getMoney())

    def determineWinner(self): # need to handle same scores
        scoreList = []
        copyList= []
        for i, player in enumerate(self.playerList):
            result, score = player.playerScore()
            scoreList.append(score)
        copyList = scoreList[:]
        copyList.sort()
        highIndex = scoreList.index(copyList[-1])
        if scoreList.count(copyList[-1]) == 1:    
            return highIndex, 0
        elif scoreList.count(copyList[-1]) > 1:
            highIndex, addedPotCnt = self.doubleDown(copyList[-1])
            return highIndex, addedPotCnt

    def DDwinner(self, iList):
        scoreList = []
        copyList = []
        #print("indexList:", iList)
        for pIndex in iList:
            result, score = self.playerList[pIndex].playerScore()
            scoreList.append(score)
        copyList = scoreList[:]
        copyList.sort()
        scoreListIndex = scoreList.index(copyList[-1])
        #print("scoreListIndex", scoreListIndex)
        highIndex = iList[scoreListIndex]
        #print(highIndex)
        return highIndex

    def awardWinner(self, winner, potCount):
        award = potCount * 10
        self.playerList[winner].winsPot(award)

    def doubleDown(self, highScore):
        # the process will be to first look through the playerList and see
        # which players have the same score as the high score (copyList[-1])
        # then to make a list of the indexes within the player list of those
        # players. Then loop through that list, using each index in the list
        # to activate the players and make them play
        self.interface.doubleDown()
        indexList = [] # this is a list of the player indexes that have high score
        for i, player in enumerate(self.playerList):
            result, score = player.playerScore()
            if score == highScore:
                indexList.append(i)
        # temporarily change colors of players in a double down
        self.interface.doubleColor(indexList)# will change colors of players in DD
        
        # cycle through the index list and make the players loose 10 bucks and
        # increase potCount by 1
        potCount = 0
        for each in indexList:
            self.interface.displayMoney(each, self.playerList[each].getMoney())
            self.interface.currentPlayer(each)
            if self.interface.roll() and (self.playerList[each].getMoney() >= 10):
                self.playerList[each].subtract(10)
                potCount = potCount + 1
                self.playerList[each].playerRoll()
                self.interface.displayResult(each, self.playerList[each]) 
                self.interface.displayMoney(each, self.playerList[each].getMoney())
            self.interface.resetDoubleColor(each)
        winner = self.DDwinner(indexList)
        return winner, potCount
            
        
        
            
class GraphicInterface:

    def __init__(self):
        self.win = GraphWin("CeeLo", 700, 600)
        self.win.setCoords(0,0,7,6)
        self.drawPlayers()
        self.drawMoneyDisplays()
        self.drawDice()
        self.continueButton = Button(self.win, Point(1,1), 1, 0.3, "Play Round")
        self.rollButton = Button(self.win, Point(6,1), 0.5, 0.4, "Roll!")
        self.resultDisplay = Text(Point(2, 5.5), "").draw(self.win)
        self.resultDisplay.setSize(20)
        self.winnerDisplay = Text(Point(3.5, 0.2), "").draw(self.win)
        self.winnerDisplay.setSize(20)
        

    def drawPlayers(self):
        circSpecs = [(3.5, 5), (5, 4), (5,2), (3.5, 1), (2,2), (2,4)]
        self.playerLabels = []
        self.playerCircles = []
        for i, (x, y) in enumerate(circSpecs):
            self.playerCircles.append(Circle(Point(x, y), 0.5).draw(self.win))
            self.playerLabels.append(Text(Point(x,y), "Player {0}".format(i+1)).draw(self.win))

    def drawMoneyDisplays(self):
        displaySpecs = [(3.5, 5.7), (5, 4.7), (5, 2.7), (3.5, 1.7), (2,2.7),
                              (2, 4.7)]
        self.moneyDisplays = []
        for x, y in displaySpecs:
            Rectangle(Point(x-0.4, y - 0.12), Point(x + 0.4, y + 0.12)).draw(self.win)
            self.moneyDisplays.append(Text(Point(x,y), "").draw(self.win))

    def drawDice(self):
        self.dieOne = DieView(self.win, Point(2.9, 3), 0.5)
        self.dieTwo = DieView(self.win, Point(3.5, 3.6), 0.5)
        self.dieThree = DieView(self.win, Point(4.1, 3), 0.5)
        
    def continuePlaying(self):
        self.continueButton.activate()
        
        while True:
            try:
                p = self.win.checkMouse()
                if self.continueButton.clicked(p):
                    self.continueButton.deactivate()
                    return True
            except AttributeError as error:
                pass
        
    def activePlayers(self, playerList):
        self.resultDisplay.setText("")
        self.winnerDisplay.setText("")
        for i, player in enumerate(playerList):
            if player.getMoney() >= 10:
                self.playerCircles[i].setFill("green")
                self.playerLabels[i].setStyle("bold")
                
    def currentPlayer(self, pIndex):
        self.playerCircles[pIndex].setFill("orange")

    def resetPlayerColor(self, pIndex):
        self.playerCircles[pIndex].setFill("green")

    def resetDoubleColor(self, pIndex):
        self.playerCircles[pIndex].setFill("pink")
        
    def displayMoney(self, pIndex, money):
        self.moneyDisplays[pIndex].setText("$ {0}".format(str(money)))
        
    def roll(self):
        self.rollButton.activate()

        while True:
            try:
                p = self.win.checkMouse()
                if self.rollButton.clicked(p):
                    self.rollButton.deactivate()
                    return True
            except AttributeError as error:
                pass

    def displayResult(self, pIndex, player):
        # this method has to display the DieView as well as the result/score
        # of the roll

        values = player.values()
        self.dieOne.setValue(values[0])
        self.dieTwo.setValue(values[1])
        self.dieThree.setValue(values[2])

        result, score = player.playerScore()
        self.resultDisplay.setText("{0}".format(result))

    def displayWinner(self, winner):
        self.winnerDisplay.setText("Player {0} wins!".format(str(winner + 1)))
        
    def doubleColor(self, indexList):
        for pIndex in indexList:
            self.playerCircles[pIndex].setFill("pink")

    def doubleDown(self):
        self.winnerDisplay.setText("Double Down!")
