def newGame():
    game = {"turn":1, "winner":False}
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
    game['moves'] = getAvailableMoves(game)
    return game

def getAvailableMoves(game):
    moves = []
    for i in range(8):
        for j in range(8):
            if game['board'][i][j] not in [3, 0]:
                if game['board'][i][j]['player'] == game['turn']:
                    available = availableMoves(game, i, j)
                    if available:
                        moves += available
    return moves

def availableMoves(game, i, j):
    king = game['board'][i][j]['king']
    player = game['board'][i][j]['player']
    direction = [1, -1] if king else [1] if player == 1 else [-1]
    moves = []
    for y in direction:
        for x in [1, -1]:
            if i+x in range(8) and j+y in range(8):
                if game['board'][i+x][j+y] == 3:
                    moves.append(((i,j), (i+x, j+y)))
                elif game['board'][i+x][j+y]['player'] != player and i+x*2 in range(8) and j+y*2 in range(8):
                    if game['board'][i+x*2][j+y*2] == 3:
                        moves.append(((i,j), (i+x*2, j+y*2))) 
    return moves

def makeMove(game, fromTup, toTup):
    if [fromTup, toTup] not in game['moves']: return game
    else:
        rep = getRepr(game)
        piece = game['board'][fromTup[0]][fromTup[1]]
        if toTup[1] in [0, 7]: piece['king'] = True
        game['board'][fromTup[0]][fromTup[1]] = 3
        game['board'][toTup[0]][toTup[1]] = piece
        if (fromTup[0] - toTup[0]) % 2 == 1: return nextTurn(game)
        elif (fromTup[0] - toTup[0]) % 2 == 0:
           betweenTup = (fromTup[0] - (fromTup[0] - toTup[0])/2, 
                         fromTup[1] - (fromTup[1] - toTup[1])/2)
           print betweenTup
           game['board'][betweenTup[0]][betweenTup[1]] = 3
           mustMove = []
           for tup in availableMoves(game, toTup[0], toTup[1]):
               if (tup[0][0] - tup[1][0]) % 2 == 0: mustMove.append(tup)
           if not mustMove: return nextTurn(game)
           else:
               game['moves'] = mustMove
               return game

def nextTurn(game):
    prevTurn = game['turn']
    game['turn'] = 2 if prevTurn == 1 else 1
    moves = getAvailableMoves(game)
    if not moves:
        game['winner'] = 'home' if prevTurn == 1 else 'away'
    game['moves'] = moves
    return game    

def getRepr(game):
    rep = ''
    turn = game['turn']
    rangeRover = lambda: range(8) if turn == 1 else range(7, -1, -1)
    flipPlayer = lambda player: str(player) if turn == 1 else '1' if player == 2 else '2'
    board = game['board']
    for x in rangeRover():
        for y in rangeRover():
            if (x+y)%2 == 1:
                square = board[x][y]
                if square == 3: rep += '3'
                elif square['king']: rep += 'k'+flipPlayer(square['player'])
                else: rep += flipPlayer(square['player'])
    return rep
