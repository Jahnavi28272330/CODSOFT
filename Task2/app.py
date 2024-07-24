from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Initialize the empty board
board = [['' for _ in range(3)] for _ in range(3)]

def is_winner(board, player):
    # Check rows, columns, and diagonals for a win
    for i in range(3):
        if all([cell == player for cell in board[i]]):
            return True
        if all([board[j][i] == player for j in range(3)]):
            return True
    if all([board[i][i] == player for i in range(3)]):
        return True
    if all([board[i][2-i] == player for i in range(3)]):
        return True
    return False

def is_draw(board):
    return all([all([cell != '' for cell in row]) for row in board])

def minimax(board, depth, is_maximizing):
    if is_winner(board, 'O'):
        return 10
    if is_winner(board, 'X'):
        return -10
    if is_draw(board):
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    board[i][j] = 'O'
                    score = minimax(board, depth + 1, False)
                    board[i][j] = ''
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    board[i][j] = 'X'
                    score = minimax(board, depth + 1, True)
                    board[i][j] = ''
                    best_score = min(score, best_score)
        return best_score

def best_move():
    best_score = -float('inf')
    move = (0, 0)
    for i in range(3):
        for j in range(3):
            if board[i][j] == '':
                board[i][j] = 'O'
                score = minimax(board, 0, False)
                board[i][j] = ''
                if score > best_score:
                    best_score = score
                    move = (i, j)
    return move

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def move():
    global board
    data = request.json
    row, col = data['row'], data['col']

    if board[row][col] == '':
        board[row][col] = 'X'
        if is_winner(board, 'X'):
            return jsonify(status='win', winner='X', board=board)
        if is_draw(board):
            return jsonify(status='draw', board=board)

        # AI makes a move
        ai_row, ai_col = best_move()
        board[ai_row][ai_col] = 'O'
        if is_winner(board, 'O'):
            return jsonify(status='win', winner='O', board=board)
        if is_draw(board):
            return jsonify(status='draw', board=board)

        return jsonify(status='continue', board=board)

    return jsonify(status='invalid', board=board)

@app.route('/reset', methods=['POST'])
def reset():
    global board
    board = [['' for _ in range(3)] for _ in range(3)]
    return jsonify(status='reset', board=board)

if __name__ == '__main__':
    app.run(debug=True)
