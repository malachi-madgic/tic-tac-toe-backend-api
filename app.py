from flask import Flask, request, jsonify

app = Flask(__name__)

# Initialize the game board
board = [' ' for _ in range(9)]
current_player = 'X'

# Check for a win or draw
winning_combinations = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
    [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
    [0, 4, 8], [2, 4, 6]              # diagonals
]

def check_winner():
    for combo in winning_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] != ' ':
            return board[combo[0]]
    if ' ' not in board:
        return 'Draw'
    return None

@app.route('/board', methods=['GET'])
def get_board():
    return jsonify({'board': board, 'current_player': current_player})

@app.route('/move', methods=['POST'])
def make_move():
    global current_player
    data = request.get_json()
    position = data.get('position')

    if position is None or not (0 <= position < 9):
        return jsonify({'error': 'Invalid position'}), 400

    if board[position] != ' ':
        return jsonify({'error': 'Position already taken'}), 400

    board[position] = current_player

    winner = check_winner()
    if winner:
        return jsonify({'board': board, 'winner': winner})

    current_player = 'O' if current_player == 'X' else 'X'
    return jsonify({'board': board, 'current_player': current_player})

if __name__ == '__main__':
    app.run(debug=True)
