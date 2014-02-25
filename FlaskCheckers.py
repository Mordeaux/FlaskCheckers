import string, random, os, json
from flask import Blueprint, render_template, request
from logic import makeMove, newGame, getAvailableMoves

directory = os.path.dirname(__file__)
DATA_DIR = os.path.join(directory, 'data')
if not os.path.exists(DATA_DIR):
    os.mkdir(DATA_DIR)

checkers = Blueprint('checkers', __name__, template_folder='templates', static_folder='static')

@checkers.route('/')
def game():
    team = 'home'
    gameID = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for i in range(6))
    if request.args.get('game'):
        gameID = request.args.get('game')
        team = 'away'
    if team == 'home':
        with open(os.path.join(DATA_DIR, gameID+'.json'), 'w') as f:
            f.write(json.dumps(newGame()))
    return render_template('FlaskCheckers.html', team=team, gameID=gameID)

@checkers.route('/loadJson')
def loadJson():
    gameID = request.args.get('game')
    with open(os.path.join(DATA_DIR, gameID+'.json'), 'r') as f:
        gameJSON = f.read()
    return gameJSON

@checkers.route('/move')
def move():
    gameID = request.args.get('game')
    fromTup = [int(i) for i in list(request.args.get('from'))]
    toTup = [int(i) for i in list(request.args.get('to'))]
    with open(os.path.join(DATA_DIR, gameID+'.json'), 'r') as f:
        game = json.loads(f.read())
    gameJSON = json.dumps(makeMove(game, fromTup, toTup))
    with open(os.path.join(DATA_DIR,  gameID+'.json'), 'w') as f:
        f.write(gameJSON)
    return gameJSON

@checkers.route('/isTurn')
def isTurn():
    gameID = request.args.get('game')
    player = request.args.get('player')
    with open(os.path.join(DATA_DIR, gameID+'.json'), 'r') as f:
        turn = json.loads(f.read())['turn']
    isTurn = lambda:'true' if turn == 1 and player == 'home' or turn == 2 and player == 'away' else 'false'
    return isTurn()

@checkers.route('/noJump')
def noJump():
    gameID = request.args.get('game')
    player = request.args.get('player')
    with open(os.path.join(DATA_DIR, gameID+'.json'), 'r') as f:
        game = json.loads(f.read())
    game['turn'] = 2 if player == 'home' else 1
    game['move'] = getAvailableMoves(game)
    gameJSON = json.dumps(game)
    with open(os.path.join(DATA_DIR, gameID+'.json'), 'w') as f:
        f.write(gameJSON)
    return gameJSON
