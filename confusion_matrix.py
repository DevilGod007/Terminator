import chess
import numpy as np
import tensorflow as tf
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

# Load the trained neural network model
MODEL_PATH = "chess_model_complex.h5"
model = tf.keras.models.load_model(MODEL_PATH, compile=False)
model.compile(optimizer="adam", loss="mse", metrics=["mae"])

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

def evaluate_with_nn(board):
    """Evaluate the best move using the neural network."""
    legal_moves = list(board.legal_moves)
    if not legal_moves:
        return None  # No legal moves available

    input_data = []
    move_map = {}

    for move in legal_moves:
        board.push(move)
        input_data.append(board_to_input(board))
        move_map[len(input_data) - 1] = move
        board.pop()

    input_data = np.vstack(input_data)
    scores = model.predict(input_data, verbose=0).flatten()
    best_move_index = np.argmax(scores)
    return move_map[best_move_index].uci()

def evaluate_with_stockfish(board, stockfish_path="D:/stockfish/stockfish-windows-x86-64-avx2.exe"):
    """Evaluate the best move using Stockfish."""
    import chess.engine
    with chess.engine.SimpleEngine.popen_uci(stockfish_path) as engine:
        result = engine.play(board, chess.engine.Limit(time=0.1))
        return result.move.uci()

def generate_confusion_matrix(test_positions, ground_truth_moves):
    """Generate a confusion matrix comparing NN predictions with Stockfish moves."""
    predicted_moves = []

    for fen in test_positions:
        board = chess.Board(fen)
        predicted_move = evaluate_with_nn(board)
        predicted_moves.append(predicted_move)

    # Generate confusion matrix
    labels = list(set(ground_truth_moves + predicted_moves))  # Unique moves
    cm = confusion_matrix(ground_truth_moves, predicted_moves, labels=labels)

    # Display the confusion matrix
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)
    disp.plot(cmap=plt.cm.Blues)
    plt.title("Confusion Matrix: Neural Network vs Stockfish")
    plt.show()

if __name__ == "__main__":
    # Test positions (FEN strings)
    test_positions = [
        "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",  # Starting position
        "r1bqkbnr/pppp1ppp/2n5/4p3/8/3P1NP1/PPP1PP1P/RNBQKB1R w KQkq - 0 3",  # Sample position
        "rnbq1rk1/pppp1ppp/4pn2/8/3P4/2N5/PPP2PPP/R1BQKB1R w KQ - 0 5"  # Another sample
    ]

    # Ground truth moves (from Stockfish or manually defined)
    ground_truth_moves = ["e2e4", "d2d4", "g1f3"]

    # Generate the confusion matrix
    generate_confusion_matrix(test_positions, ground_truth_moves)