import pygame
import sys
from pygame import mixer

pygame.init()

# Title and Icon
pygame.display.set_caption("Tic Tac Toe")
icon = pygame.image.load("ticTacToeIcon.png")
pygame.display.set_icon(icon)

# Display
display = width, height = 980, 680
screen = pygame.display.set_mode(display)
bgImg = pygame.image.load("ticTacToeBoard.png")
bgMenu = pygame.image.load("ticTacToeMenu.png")
crossImg = pygame.image.load("ticTacToeCross.png")
circleImg = pygame.image.load("ticTacToeCircle.png")
verticalLine = pygame.image.load("ticTacToeVerticalLine.png")
crossLeftLine = pygame.image.load("ticTacToeCrossLeftLine.png")
crossRightLine = pygame.image.load("ticTacToeCrossRightLine.png")
horizontalLine = pygame.image.load("ticTacToeHorizontalLine.png")
againButtonImg = pygame.image.load("ticTacToeButton.png")

# Background Sound
backgroundSound = pygame.mixer.Sound("ticTacToeSoundBackground.mp3")
backgroundSound.set_volume(0.05)
backgroundSound.play(-1)
piecePlaced = mixer.Sound("ticTacToeSoundPiece.mp3")
winSound = mixer.Sound("ticTacToeSoundWin.mp3")
winSound.set_volume(0.3)


def fontSize(x):
    return pygame.font.Font('freesansbold.ttf', x)


# State of the Board
images = [crossImg, circleImg, crossImg, circleImg, crossImg, circleImg, crossImg, circleImg, crossImg, circleImg]
board = [["topLeft", "empty"], ["topCenter", "empty"], ["topRight", "empty"],
         ["middleLeft", "empty"], ["middleCenter", "empty"], ["middleRight", "empty"],
         ["bottomLeft", "empty"], ["bottomCenter", "empty"], ["bottomRight", "empty"]]

# Positions of Pieces
location = {"topLeft": (60, 80), "topCenter": (268, 80), "topRight": (465, 80),
            "middleLeft": (60, 283), "middleCenter": (268, 283), "middleRight": (465, 283),
            "bottomLeft": (60, 480), "bottomCenter": (268, 480), "bottomRight": (465, 480)}

# Positions of Lines
line = [(horizontalLine, (70, -115)), (horizontalLine, (70, 90)), (horizontalLine, (70, 290)),
        (verticalLine, (-130, 90)), (verticalLine, (73, 90)), (verticalLine, (270, 90)),
        (crossRightLine, (70, 85)), (crossLeftLine, (70, 85))]

# Score
score = [0, 0]


def checkWin():
    for i in range(9):
        if board[i][1]!="empty":
            screen.blit(board[i][1], location[board[i][0]])
    for i in range(3):
        if board[3 * i][1]==board[3 * i + 1][1]==board[3 * i + 2][1]!="empty":
            win(i)  # Horizontal
            return True
        if board[i][1]==board[i + 3][1]==board[i + 6][1]!="empty":
            win(3 + i)  # Vertical
            return True
    for i in range(2):
        if board[2 * i][1]==board[4][1]==board[8 - 2 * i][1]!="empty":
            win(6 + i)  # Cross
            return True


def win(i):
    screen.blit(line[i][0], line[i][1])
    mainMessage("win")


def againButton():
    againMessage = fontSize(38).render("Play Again", True, (0, 0, 0))
    screen.blit(againMessage, (730, 550))
    screen.blit(againButtonImg, (700, 440))


def resetGame():
    c = 0
    images.clear()
    images.append(crossImg)
    for i in range(9):
        board[i][1] = "empty"
        if c % 2==0:
            images.append(circleImg)
        else:
            images.append(crossImg)
        c += 1


def mainMessage(state):
    screen.blit(bgMenu, (680, 0))
    if len(images) % 2 == 0 and state == "normal":
        turn = "Player 1"
        piece = circleImg
    else:
        turn = "Player 2"
        piece = crossImg

    if len(images) % 2 == 1 and state == "win":
        turn = "Player 1"
    else:
        turn = "Player 2"

    if state=="normal":
        playerTurnMove = fontSize(64).render("Move", True, (0, 0, 0))
        screen.blit(playerTurnMove, (745, 120))
        screen.blit(piece, (765, 210))
        playerTurnPlayer = fontSize(64).render(turn, True, (0, 0, 0))
        screen.blit(playerTurnPlayer, (700, 30))
    if state=="win":
        winMessage = fontSize(72).render("WINS", True, (0, 0, 0))
        screen.blit(winMessage, (735, 200))
        againButton()
        playerTurnPlayer = fontSize(64).render(turn, True, (0, 0, 0))
        screen.blit(playerTurnPlayer, (700, 30))
    if state=="draw":
        drawMessage = fontSize(72).render("Draw", True, (0, 0, 0))
        screen.blit(drawMessage, (740, 150))
        againButton()

    playerOneScore = fontSize(42).render('Player 1: ' + str(score[0]), True, (0, 0, 0))
    playerTwoScore = fontSize(42).render('Player 2: ' + str(score[1]), True, (0, 0, 0))
    screen.blit(playerOneScore, (720, 370))
    screen.blit(playerTwoScore, (720, 425))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

        if event.type == pygame.MOUSEBUTTONUP:
            mousePos = pygame.mouse.get_pos()
            if not checkWin():
                if 30 < mousePos[0] < 220:
                    rowLoc = "Left"
                if 253 < mousePos[0] < 406:
                    rowLoc = "Center"
                if 439 < mousePos[0] < 628:
                    rowLoc = "Right"

                if 40 < mousePos[1] < 233:
                    colLoc = "top"
                if 267 < mousePos[1] < 423:
                    colLoc = "middle"
                if 457 < mousePos[1] < 642:
                    colLoc = "bottom"

                try:
                    loc = colLoc + rowLoc
                except NameError:
                    pass

                for i in range(9):
                    try:
                        if board[i][0]==loc and board[i][1]=="empty":
                            board[i][1] = images.pop()
                            piecePlaced.play()
                            if checkWin():
                                winSound.play()
                    except NameError:
                        pass

            if checkWin() or (not checkWin() and len(images)==1):
                if 705 < mousePos[0] < 955 and 440 < mousePos[1] < 615:
                    resetGame()
            if checkWin() and len(images) != 1 :
                score[(len(images)+1) % 2] += 1

    screen.blit(bgImg, (0, 0))
    checkWin()
    mainMessage("normal")
    if not checkWin() and len(images)==1:
        mainMessage("draw")

    pygame.display.update()
