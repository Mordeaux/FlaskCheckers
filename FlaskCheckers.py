import string, random, os, json
from flask import Blueprint, render_template, send_file, request, redirect
from logic import *

directory = os.path.dirname(__file__)
DATA_DIR = os.path.join(directory, 'data')
if not os.path.exists(DATA_DIR):
    os.mkdir(DATA_DIR)



checkers = Blueprint('checkers', __name__, template_folder='templates', static_folder='static')



@checkers.route('/')
def game():
    team = 'home'
    gameID = ''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(8))
    if request.args.get('game'):
        gameID = request.args.get('game')
        team = 'away'
    if team == 'home':
        with open(os.path.join(DATA_DIR, gameID+'.json'), 'w') as f:
            f.write(newGame())
    return render_template('FlaskCheckers.html', team=team, gameID=gameID)

@checkers.route('/loadJson')
def loadJson():
    gameID = request.args.get('game')
    with open(os.path.join(DATA_DIR, gameID+'.json'), 'r') as f:
        gameJSON = f.read()
    return gameJSON

@checkers.route('/move')
def move():
    playerMoving = 1
    gameID = request.args.get('game')
    fromTup = tuple([int(i) for i in list(request.args.get('from'))])
    toTup = tuple([int(i) for i in list(request.args.get('to'))])
    if request.args.get('player') == 'away':
        playerMoving = 2
    with open(os.path.join(DATA_DIR, gameID+'.json'), 'r') as f:
        gameJSON = f.read()
    nGameJSON = move(gameJSON, playerMoving, fromTup, toTup)
    if gameJSON == nGameJSON:
        return 'false'
    with open(os.path.join(DATA_DIR,  gameID+'.json'), 'w') as f:
        f.write(nGameJSON)
    return nGameJSON

@checkers.route('/isTurn')
def isTurn():
    gameID = request.args.get('game')
    player = request.args.get('player')
    with open(os.path.join(DATA_DIR, gameID+'.json'), 'r') as f:
        turn = json.loads(f.read())['turn']
    if turn == 1 and player == 'home':
        return 'true'
    if turn == 2 and player == 'away':
        return 'true'
    else:
        return 'false'

@checkers.route('/noJump')
def noJump():
    gameID = request.args.get('game')
    player = request.args.get('player')
    with open(os.path.join(DATA_DIR, gameID+'.json'), 'r') as f:
        game = json.loads(f.read())
    game['mustMove'] = False
    game['turn'] = 1
    if player == 'home':
        game['turn'] = 2
    gameJSON = json.dumps(game)
    with open(os.path.join(DATA_DIR, gameID+'.json'), 'w') as f:
        f.write(gameJSON)
    return gameJSON
