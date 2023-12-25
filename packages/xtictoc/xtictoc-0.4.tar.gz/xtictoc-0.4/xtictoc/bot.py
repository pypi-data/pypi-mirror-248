import random

def get_strategic_bot_move(board, player):
    # Implement your strategic bot logic here
    # For simplicity, let's use random moves as an example
    available_moves = [(i, j) for i in range(3) for j in range(3) if board[i][j] == " "]
    return random.choice(available_moves)