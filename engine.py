import sys
import chess
import numpy as np
import tensorflow as tf

# Load trained neural network model with explicit loss function
MODEL_PATH = "chess_model.h5"
model = tf.keras.models.load_model(MODEL_PATH, compile=False)  # Avoid compiling at load

# Manually compile after loading
model.compile(optimizer="adam", loss="mse", metrics=["mae"])

def board_to_input(board):
    """Convert board state to input format for the neural network."""
    input_array = np.zeros((8, 8, 12))
    piece_map = board.piece_map()
    for square, piece in piece_map.items():
        row, col = divmod(square, 8)
        input_array[row, col, piece.piece_type - 1] = 1 if piece.color == chess.WHITE else -1
    return input_array.flatten().reshape(1, -1)

def evaluate_moves(board):
    """Evaluate all legal moves using the neural network."""
    best_move = None
    best_score = -np.inf
    for move in board.legal_moves:
        board.push(move)
        input_data = board_to_input(board)
        score = model.predict(input_data, verbose=0)[0][0]  # Suppress TensorFlow output
        board.pop()
        if score > best_score:
            best_score = score
            best_move = move
    return best_move

def uci_loop():
    board = chess.Board()
    print("id name NeuralChessEngine")
    print("id author YourName")
    print("uciok")
    
    while True:
        command = input().strip()
        if command == "uci":
            print("uciok")
        elif command == "isready":
            print("readyok")
        elif command.startswith("position"):
            parts = command.split()
            if "startpos" in parts:
                board = chess.Board()
            elif "fen" in parts:
                fen_index = parts.index("fen") + 1
                board = chess.Board(" ".join(parts[fen_index:fen_index+6]))
            if "moves" in parts:
                moves_index = parts.index("moves") + 1
                for move in parts[moves_index:]:
                    board.push_uci(move)
        elif command.startswith("go"):
            best_move = evaluate_moves(board)
            if best_move:
                print(f"bestmove {best_move.uci()}")
        elif command == "quit":
            break

if __name__ == "__main__":
    uci_loop()
