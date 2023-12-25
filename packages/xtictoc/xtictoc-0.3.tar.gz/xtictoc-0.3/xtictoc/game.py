from .bot import get_strategic_bot_move
import os

def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 9)

def check_winner(board, player):
    for i in range(3):
        if all(board[i][j] == player for j in range(3)) or all(board[j][i] == player for j in range(3)):
            return True

    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True

    return False

def is_board_full(board):
    return all(cell != " " for row in board for cell in row)

def get_player_move(board, player):
    print_board(board)

    if player == "X":
        row = int(input("Enter row (0, 1, or 2): "))
        col = int(input("Enter column (0, 1, or 2): "))
    else:
        print("Bot is making a move...")
        row, col = get_bot_move(board)

    return row, col

def get_bot_move(board):
    return get_strategic_bot_move(board, "O")

def play_game():
    board = [[" " for _ in range(3)] for _ in range(3)]
    current_player = "X"

    while True:
        row, col = get_player_move(board, current_player)

        if board[row][col] == " ":
            board[row][col] = current_player

            if check_winner(board, current_player):
                print_board(board)
                print(f"{current_player} wins!")
                break
            elif is_board_full(board):
                print_board(board)
                print("It's a tie!")
                break
            else:
                current_player = "O" if current_player == "X" else "X"
        else:
            print("Invalid move. The cell is already occupied. Try again.")

if __name__ == "__main__":
    print("Welcome to Tic-Tac-Toe (XO)!")
    os.system('dir')
    play_game()