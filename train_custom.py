import os
import chess
import chess.pgn
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.optimizers import Adam

TRAIN_FOLDER = "train"
MODEL_PATH = "chess_model_complex.h5"

def parse_pgn_file(pgn_path):
    """Extracts board positions and evaluation values from a PGN file."""
    data = []
    
    with open(pgn_path, "r") as pgn_file:
        while True:
            game = chess.pgn.read_game(pgn_file)
            if game is None:
                break  # End of file

            board = game.board()
            for move in game.mainline_moves():
                board.push(move)  # Play the move
                
                # Convert board state to input array
                input_array = np.zeros((8, 8, 12))
                piece_map = board.piece_map()
                
                for square, piece in piece_map.items():
                    row, col = divmod(square, 8)
                    input_array[row, col, piece.piece_type - 1] = 1 if piece.color == chess.WHITE else -1
                
                # Use game outcome as reward (RL approach)
                result = game.headers.get("Result", "*")
                if result == "1-0":  # White wins
                    evaluation = 1.0
                elif result == "0-1":  # Black wins  
                    evaluation = -1.0
                elif result == "1/2-1/2":  # Draw
                    evaluation = 0.0
                else:
                    evaluation = 0.0  # Unknown result
                
                data.append((input_array.flatten(), evaluation))
    
    return data

def load_pgn_data(train_folder):
    """Reads all PGN files in the train folder and extracts training data."""
    all_data = []
    
    for file in os.listdir(train_folder):
        if file.endswith(".pgn"):
            file_path = os.path.join(train_folder, file)
            print(f"Processing {file_path}...")
            all_data.extend(parse_pgn_file(file_path))
    
    if not all_data:
        print("No valid PGN data found!")
        return None, None
    
    X_train = np.array([x[0] for x in all_data])
    y_train = np.array([x[1] for x in all_data])
    
    return X_train, y_train

# Load training data from PGN files
X_train, y_train = load_pgn_data(TRAIN_FOLDER)

if X_train is None:
    print("Training aborted due to missing data.")
    exit()

# Define Neural Network Model
model = Sequential([
    Dense(128, activation="relu", input_shape=(8*8*12,)),
    Dense(64, activation="relu"),
    Dense(1, activation="linear")  # Single value output
])

model.compile(optimizer=Adam(learning_rate=0.001), loss="mse", metrics=["mae"])

# Train Model
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.1)

# Save Model
model.save(MODEL_PATH)
print(f"Model saved to {MODEL_PATH}")

