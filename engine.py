import sys
import chess
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
import random  # Add import for random fallback
import os     # Add import for file operations

# Load trained neural network model with explicit loss function
MODEL_PATH = "chess_model_complex.h5"

# Try to load existing model, create new one if not found
try:
    if os.path.exists(MODEL_PATH):
        model = tf.keras.models.load_model(MODEL_PATH, compile=False)
        print(f"Loaded existing model from {MODEL_PATH}")
    else:
        print(f"Model file {MODEL_PATH} not found. Creating new model...")
        # Create a new model with the same architecture as train_rl.py
        model = Sequential([
            Dense(128, activation="relu", input_shape=(8*8*12,)),
            Dense(64, activation="relu"),
            Dense(32, activation="relu"),
            Dense(1, activation="linear")
        ])
        model.save(MODEL_PATH)  # Keep original format
        print(f"New model created and saved to {MODEL_PATH}")
        
except Exception as e:
    print(f"Error loading model: {e}")
    print("Creating new model...")
    # Create a simple fallback model
    model = Sequential([
        Dense(128, activation="relu", input_shape=(8*8*12,)),
        Dense(64, activation="relu"),
        Dense(1, activation="linear")
    ])
    model.save(MODEL_PATH)  # Keep original format
    print(f"Fallback model created and saved to {MODEL_PATH}")

# Manually compile after loading
model.compile(optimizer="adam", loss="mse", metrics=["mae"])

# RL Agent parameters
EPSILON = 0.1  # Exploration rate for RL inference
EXPLORATION_ENABLED = False  # Set to True for continued learning during play

def board_to_input(board):
    """Convert board state to input format for the neural network."""
    input_array = np.zeros((8, 8, 12), dtype=np.float32)
    piece_map = board.piece_map()
    piece_to_index = {
        chess.PAWN: 0,
        chess.KNIGHT: 1,
        chess.BISHOP: 2,
        chess.ROOK: 3,
        chess.QUEEN: 4,
        chess.KING: 5,
    }
    for square, piece in piece_map.items():
        row, col = divmod(square, 8)
        index = piece_to_index[piece.piece_type] + (6 if piece.color == chess.BLACK else 0)
        input_array[row, col, index] = 1
    return input_array.flatten().reshape(1, -1)

def evaluate_moves(board):
    """Evaluate all legal moves using the neural network (RL version)."""
    
    # Check for all possible game ending conditions based on chess rules
    if board.is_checkmate():
        winner = "White" if board.turn == chess.BLACK else "Black"
        print(f"info string CHECKMATE! {winner} wins!", file=sys.stderr)
        return None
    
    if board.is_stalemate():
        print("info string STALEMATE! Game is a draw.", file=sys.stderr)
        return None
    
    if board.is_insufficient_material():
        print("info string DRAW! Insufficient material to checkmate.", file=sys.stderr)
        return None
    
    if board.is_seventyfive_moves():
        print("info string DRAW! 75-move rule - no capture or pawn move in 75 moves.", file=sys.stderr)
        return None
    
    if board.is_fivefold_repetition():
        print("info string DRAW! Position repeated 5 times.", file=sys.stderr)
        return None
    
    # Check for optional draw conditions
    if board.can_claim_fifty_moves():
        print("info string DRAW can be claimed! 50-move rule.", file=sys.stderr)
    
    if board.can_claim_threefold_repetition():
        print("info string DRAW can be claimed! Threefold repetition.", file=sys.stderr)
    
    # Check if current player is in check
    if board.is_check():
        current_player = "White" if board.turn == chess.WHITE else "Black"
        print(f"info string CHECK! {current_player} king is in check.", file=sys.stderr)
    
    legal_moves = list(board.legal_moves)
    if not legal_moves:
        print("info string No legal moves available!", file=sys.stderr)
        return None

    # RL exploration: sometimes choose random moves
    if EXPLORATION_ENABLED and random.random() < EPSILON:
        return random.choice(legal_moves)

    # Use neural network to evaluate moves
    input_data = []
    move_map = {}

    # Batch all legal moves for faster evaluation
    for move in legal_moves:
        board.push(move)
        input_data.append(board_to_input(board))
        move_map[len(input_data) - 1] = move
        board.pop()

    input_data = np.vstack(input_data)  # Stack inputs for batch prediction

    try:
        # Get Q-values for all moves
        scores = model.predict(input_data, verbose=0).flatten()  # Batch prediction
        best_move_index = np.argmax(scores)
        return move_map[best_move_index]
    except Exception as e:
        print(f"info string Neural network evaluation failed: {e}", file=sys.stderr)
        # Fallback to a random move
        return random.choice(legal_moves)

def uci_loop():
    """Main UCI loop for the chess engine."""
    board = chess.Board()
    print("id name NeuralChessEngine")
    print("id author YourName")
    print("uciok")
    
    while True:
        try:
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
        except Exception as e:
            print(f"info string Error: {e}", file=sys.stderr)

if __name__ == "__main__":
    uci_loop()