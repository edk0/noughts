from flask import Flask, request, session

import noughts

app = Flask(__name__)
app.secret_key = 'this is just an example'

page = """
<html><head><title>noughts</title></head>
<body>
<p>
{message}
</p>
<form method="POST" action=".">
<table>
{board}
</table>
<hr>
<input type="submit" name="reset" value="Reset">{other_player}
</form>
"""

def render_tile(board, x, y):
    v = board[x,y]
    if v == noughts.Tile.EMPTY:
        return f'<button name="tile" value="{x},{y}">&nbsp;</button>'
    else:
        return v._name_

def render_row(board, y):
    return ''.join(
        f"<td>{render_tile(board, x, y)}</td>" for x in range(3))

def render_board(board):
    return ''.join(
        f"<tr>{render_row(board, y)}</tr>" for y in range(3))

@app.route('/', methods=['GET', 'POST'])
def ttt():
    message = ''
    skip = False
    if 'board' in session:
        board = noughts.Board(session['board'])
    else:
        board = noughts.Board('')
    if request.method == 'POST':
        if 'tile' in request.form and not board.winner:
            x, y = request.form['tile'].split(',')
            if board[int(x),int(y)] is noughts.Tile.EMPTY:
                board = board.replace(int(x), int(y), board.next)
            else:
                skip = True
                message = "You can't move there!"
        elif 'skip' in request.form:
            if board.spaces == 9:
                board = board.make_best_move().board
            skip = True
        elif 'reset' in request.form:
            board = noughts.Board('')
    if not skip and not board.winner and board.spaces > 0 and board.spaces < 9:
        board = board.make_best_move().board
    if board.winner:
        message = f"{board.winner._name_} wins the game!"
    elif board.spaces == 0:
        message = "We drew, try again?"
    elif board.spaces == 9:
        message = "Make your move!"
    session['board'] = board.serialize()
    if board.spaces == 9:
        other_player = '<input type="submit" name="skip" value="I want to be O">'
    else:
        other_player = ''
    return page.format(message=message, board=render_board(board), other_player=other_player)

