
import math

board = [" " for _ in range(9)]


def print_board():
    print()
    print(board[0] + " | " + board[1] + " | " + board[2])
    print("--+---+--")
    print(board[3] + " | " + board[4] + " | " + board[5])
    print("--+---+--")
    print(board[6] + " | " + board[7] + " | " + board[8])
    print()


def check_winner():
    winning_positions = [
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6)
    ]

    for a, b, c in winning_positions:
        if board[a] == board[b] == board[c] and board[a] != " ":
            return board[a]

    if " " not in board:
        return "Draw"

    return None


def minimax(board, depth, maximizing, alpha, beta):
    result = check_winner()

    if result == "O":
        return 10 - depth

    if result == "X":
        return depth - 10

    if result == "Draw":
        return 0

    if maximizing:
        best_score = -math.inf

        for i in range(9):
            if board[i] == " ":
                board[i] = "O"

                score = minimax(
                    board,
                    depth + 1,
                    False,
                    alpha,
                    beta
                )

                board[i] = " "

                best_score = max(best_score, score)
                alpha = max(alpha, best_score)

                if beta <= alpha:
                    break

        return best_score

    else:
        best_score = math.inf

        for i in range(9):
            if board[i] == " ":
                board[i] = "X"

                score = minimax(
                    board,
                    depth + 1,
                    True,
                    alpha,
                    beta
                )

                board[i] = " "

                best_score = min(best_score, score)
                beta = min(beta, best_score)

                if beta <= alpha:
                    break

        return best_score


def best_move():
    best_score = -math.inf
    move = -1

    for i in range(9):
        if board[i] == " ":
            board[i] = "O"

            score = minimax(
                board,
                0,
                False,
                -math.inf,
                math.inf
            )

            board[i] = " "

            if score > best_score:
                best_score = score
                move = i

    return move


print("Tic-Tac-Toe")
print("You are X")
print("AI is O")

while True:
    print_board()

    try:
        player_move = int(input("Enter your move (1-9): ")) - 1

        if player_move < 0 or player_move > 8:
            print("Enter a number from 1 to 9.")
            continue

        if board[player_move] != " ":
            print("That position is already taken.")
            continue

    except ValueError:
        print("Please enter a number.")
        continue

    board[player_move] = "X"

    result = check_winner()

    if result is not None:
        print_board()

        if result == "X":
            print("You win!")
        else:
            print("It's a draw!")

        break

    ai_move = best_move()
    board[ai_move] = "O"

    print("AI chose position:", ai_move + 1)

    result = check_winner()

    if result is not None:
        print_board()

        if result == "O":
            print("AI wins!")
        else:
            print("It's a draw!")

        break