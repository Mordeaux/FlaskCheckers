import json, os
directory = os.path.dirname(__file__)

def newGame():
    game = {"turn":1, "mustMove":False, "winner":False}
    board = []
    for i in range(8):
        column = []
        for j in range(8):
            if (i+j)%2 == 0:
                column.append(0)
            elif j < 3:
                column.append({"player":1, "king":False})
            elif j > 4:
                column.append({"player":2, "king":False})
            else:
                column.append(3)
        board.append(column)
    game["board"] = board
    return json.dumps(game)

def tryMove(gameJSON, playerMoving, fromTup, toTup):
    game = json.loads(gameJSON)
    if game["turn"] != playerMoving:
        return gameJSON
    elif game["board"][toTup[0]][toTup[1]] != 3:
        return gameJSON
    elif game["board"][fromTup[0]][fromTup[1]]["player"] != playerMoving:
        return gameJSON
    if game["mustMove"] and game["mustMove"] != list(fromTup):
        return gameJSON
    else:
        return makeMove(game, playerMoving, fromTup, toTup)

def makeMove(game, playerMoving, fromTup, toTup):
    direction = 1
    if playerMoving == 2:
        direction = -1
    if fromTup[1] + direction == toTup[1] and toTup[0] in [fromTup[0]-1, fromTup[0]+1]:
        return setMove(game, fromTup, toTup)
    elif fromTup[1] + direction*2 == toTup[1] and toTup[0] in [fromTup[0]-2, fromTup[0]+2]:
        betweenTup = (fromTup[0]+((toTup[0]-fromTup[0])/2), fromTup[1]+direction)
        between = game["board"][betweenTup[0]][betweenTup[1]]
        if between == 3:
            return json.dumps(game)
        elif between["player"] == playerMoving:
            return json.dumps(game)
        else:
            return setJumpMove(game, fromTup, toTup, betweenTup)
    elif game["board"][fromTup[0]][fromTup[1]]["king"]:
        return makeKingMove(game, playerMoving, fromTup, toTup)
    else:
        return json.dumps(game)

def setMove(game, fromTup, toTup):
    game["board"][toTup[0]][toTup[1]] = game["board"][fromTup[0]][fromTup[1]] 
    game["board"][fromTup[0]][fromTup[1]] =  3
    if toTup[1] in [0, 7]:
        game["board"][toTup[0]][toTup[1]]["king"] = True
    if game["turn"] == 2:
        game["turn"] = 1
    else:
        game["turn"] = 2
    return json.dumps(game)

def setJumpMove(game, fromTup, toTup, betweenTup):
    game["mustMove"] = False
    game["board"][toTup[0]][toTup[1]] = game["board"][fromTup[0]][fromTup[1]] 
    game["board"][fromTup[0]][fromTup[1]] =  3
    game["board"][betweenTup[0]][betweenTup[1]] = 3
    if toTup[1] in [0, 7]:
        game["board"][toTup[0]][toTup[1]]["king"] = True
    again = canMoveAgain(game, fromTup, toTup)
    if game["turn"] == 2 and not again:
        game["turn"] = 1
    elif not again:
        game["turn"] = 2
    elif again:
        game["mustMove"] = toTup
    game["winner"] = checkWinner(game)
    return json.dumps(game)       

def canMoveAgain(game, fromTup, toTup):
    king = False
    if game["board"][toTup[0]][toTup[1]]["king"]:
        king = True
    choices = range(8)
    clearY = toTup[1]+(toTup[1]-fromTup[1])
    if clearY not in choices and not king:
        return False
    betweenY = toTup[1]+((toTup[1]-fromTup[1])/2)
    clearLeftX = toTup[0] - 2
    clearRightX = toTup[0] + 2
    clearLeft = False
    clearRight = False
    if clearY in choices:
        clearLeft = clearLeftX in choices and game["board"][clearLeftX][clearY] == 3
        clearRight = clearRightX in choices and game["board"][clearRightX][clearY] == 3
    if not clearLeft and not clearRight and not king:
        return False
    betweenLeft = 3
    betweenRight = 3
    if clearLeft:
        betweenLeft = game["board"][toTup[0]-1][betweenY]
    if clearRight:
        betweenRight = game["board"][toTup[0]+1][betweenY]
    if betweenLeft == 3 and betweenRight == 3 and not king:
        return False
    player = game["board"][toTup[0]][toTup[1]]["player"]
    oppLeft = betweenLeft != 3 and betweenLeft["player"] != player
    oppRight = betweenRight != 3 and betweenRight["player"] != player
    if clearLeft and oppLeft:
        return True
    elif clearRight and oppRight:
        return True
    elif king:
        return canKingMoveAgain(game, fromTup, toTup)
    else:
        return False





def makeKingMove(game, playerMoving, fromTup, toTup):
    direction = -1
    if playerMoving == 2:
        direction = 1
    if fromTup[1] + direction == toTup[1] and toTup[0] in [fromTup[0]-1, fromTup[0]+1]:
        return setMove(game, fromTup, toTup)
    elif fromTup[1] + direction*2 == toTup[1] and toTup[0] in [fromTup[0]-2, fromTup[0]+2]:
        betweenTup = (fromTup[0]+((toTup[0]-fromTup[0])/2), fromTup[1]+direction)
        between = game["board"][betweenTup[0]][betweenTup[1]]
        if between == 3:
            return json.dumps(game)
        elif between["player"] == playerMoving:
            return json.dumps(game)
        else:
            return setJumpMove(game, fromTup, toTup, betweenTup)
    else:
        return json.dumps(game)

   
   


def canKingMoveAgain(game, fromTup, toTup):
    choices = range(8)
    clearY = toTup[1]-(toTup[1]-fromTup[1])
    if clearY not in choices:
        return False
    betweenY = toTup[1]-((toTup[1]-fromTup[1])/2)
    clearLeftX = toTup[0] - 2
    clearRightX = toTup[0] + 2
    clearLeft = clearLeftX in choices and game["board"][clearLeftX][clearY] == 3
    clearRight = clearRightX in choices and game["board"][clearRightX][clearY] == 3
    if not clearLeft and not clearRight:
        return False
    betweenLeft = 3
    betweenRight = 3
    if clearLeft:
        betweenLeft = game["board"][toTup[0]-1][betweenY]
    if clearRight:
        betweenRight = game["board"][toTup[0]+1][betweenY]
    if betweenLeft == 3 and betweenRight == 3:
        return False
    player = game["board"][toTup[0]][toTup[1]]["player"]
    oppLeft = betweenLeft != 3 and betweenLeft["player"] != player
    oppRight = betweenRight != 3 and betweenRight["player"] != player
    if clearLeft and oppLeft:
        return True
    elif clearRight and oppRight:
        return True
    else:
        return False

def checkWinner(game):
    moves = getAvailableMoves(game)
    if moves: return False
    else:
        if game['turn'] == 1: return 'away'
        else: return 'home'
#can we check the winner based only on the available moves function?
#    player1 = False
#    player2 = False
#    for i in range(8):
#        if not player1 or not player2:
#            for j in range(8):
#                if game["board"][i][j] not in [3, 0]:
#                    if game["board"][i][j]['player'] == 1:
#                        player1 = True
#                    elif game["board"][i][j]['player'] == 2:
#                        player2 = True
#    if not player1:
#        return 'away'
#    elif not player2:
#        return 'home'
#    else:
#        moves = getAvailableMoves(game)
#        if moves: return False
#        else:
#            if game['turn'] == 1: return 'away'
#            if game['turn'] == 2: return 'home'


def getAvailableMoves(game):
    """I have no idea what the appropriate low-weight algorithm is for this, but technically 
    if your opponent has no available moves you should win."""
    playerMoving = game['turn']
    moves = []
    for i in range(8):
        for j in range(8):
            if game['board'][i][j] not in [3, 0]:
                if game['board'][i][j]['player'] == playerMoving:
                    available = availableMoves(game, i, j)
                    if available:
                        moves += available
    return moves



def availableMoves(game, i, j):
    king = game['board'][i][j]['king']
    player = game['board'][i][j]['player']
    direction = [1]
    if player == 2: direction = [-1]
    if king: direction = [1, -1]
    moves = []
    for y in direction:
        for x in [1, -1]:
            if i+x in range(8) and j+y in range(8):
                if game['board'][i+x][j+y] == 3:
                    moves.append(((i,j), (i+x, j+y)))
                elif game['board'][i+x][j+y]['player'] != player and i+x*2 in range(8) and j+y*2 in range(8):
                    if game['board'][i+x*2][j+y*2] == 3:
                        moves.append(((i,j), (i+x*2, j+x*2))) 
    return moves



