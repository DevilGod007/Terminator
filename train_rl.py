import os
import chess
import chess.pgn
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.optimizers import Adam
from collections import deque
import random

TRAIN_FOLDER = "train"
MODEL_PATH = "chess_model_complex.keras"  # Use native Keras format

class RLChessAgent:
    def __init__(self, load_existing=True):
        self.model = self.build_model()
        self.target_model = self.build_model()
        self.memory = deque(maxlen=10000)  # Experience replay buffer
        self.epsilon = 0.9  # Exploration rate
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.01
        self.gamma = 0.95  # Discount factor
        self.learning_rate = 0.001
        
        if load_existing and os.path.exists(MODEL_PATH):
            try:
                self.model = tf.keras.models.load_model(MODEL_PATH, compile=False)
                self.model.compile(optimizer=Adam(learning_rate=self.learning_rate), 
                                 loss="mse", metrics=["mae"])
                print(f"Loaded existing model from {MODEL_PATH}")
            except Exception as e:
                print(f"Error loading model: {e}. Creating new model.")
                self.model = self.build_model()
        
        # Copy weights to target model
        self.update_target_model()
    
    def build_model(self):
        """Build the neural network model for RL."""
        model = Sequential([
            Dense(128, activation="relu", input_shape=(8*8*12,)),
            Dense(64, activation="relu"),
            Dense(32, activation="relu"),
            Dense(1, activation="linear")  # Q-value output
        ])
        
        model.compile(optimizer=Adam(learning_rate=self.learning_rate), 
                     loss="mse", metrics=["mae"])
        return model
    
    def update_target_model(self):
        """Copy weights from main model to target model."""
        self.target_model.set_weights(self.model.get_weights())
    
    def remember(self, state, action, reward, next_state, done):
        """Store experience in replay buffer."""
        self.memory.append((state, action, reward, next_state, done))
    
    def choose_move(self, board, training=True):
        """Choose move with epsilon-greedy exploration."""
        legal_moves = list(board.legal_moves)
        if not legal_moves:
            return None
        
        if training and random.random() < self.epsilon:
            # EXPLORATION: Try random moves
            return random.choice(legal_moves)
        else:
            # EXPLOITATION: Use current best knowledge
            return self.get_best_move(board)
    
    def get_best_move(self, board):
        """Get best move from current policy."""
        legal_moves = list(board.legal_moves)
        if not legal_moves:
            return None
        
        best_move = None
        best_value = float('-inf')
        
        for move in legal_moves:
            board.push(move)
            state = self.board_to_input(board)
            value = self.model.predict(state, verbose=0)[0][0]
            board.pop()
            
            if value > best_value:
                best_value = value
                best_move = move
        
        return best_move
    
    def board_to_input(self, board):
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
    
    def replay_train(self, batch_size=32):
        """Train the model on a batch of experiences."""
        if len(self.memory) < batch_size:
            return
        
        batch = random.sample(self.memory, batch_size)
        states = np.array([e[0] for e in batch])
        actions = np.array([e[1] for e in batch])
        rewards = np.array([e[2] for e in batch])
        next_states = np.array([e[3] for e in batch])
        dones = np.array([e[4] for e in batch])
        
        # Reshape states
        states = states.reshape(batch_size, -1)
        next_states = next_states.reshape(batch_size, -1)
        
        # Current Q-values
        current_q_values = self.model.predict(states, verbose=0)
        
        # Next Q-values from target model
        next_q_values = self.target_model.predict(next_states, verbose=0)
        
        # Calculate target Q-values
        target_q_values = current_q_values.copy()
        for i in range(batch_size):
            if dones[i]:
                target_q_values[i][0] = rewards[i]
            else:
                target_q_values[i][0] = rewards[i] + self.gamma * np.max(next_q_values[i])
        
        # Train the model
        self.model.fit(states, target_q_values, epochs=1, verbose=0)
        
        # Decay epsilon
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

def parse_pgn_file_rl(pgn_path):
    """Extract game data for reinforcement learning training."""
    game_data = []
    
    with open(pgn_path, "r") as pgn_file:
        while True:
            game = chess.pgn.read_game(pgn_file)
            if game is None:
                break
            
            # Get game result
            result = game.headers.get("Result", "*")
            if result == "*":
                continue  # Skip unfinished games
            
            # Convert result to reward
            if result == "1-0":  # White wins
                reward = 1.0
            elif result == "0-1":  # Black wins
                reward = -1.0
            else:  # Draw
                reward = 0.0
            
            # Extract game moves
            board = game.board()
            moves = []
            for move in game.mainline_moves():
                state = board_to_input_simple(board)
                moves.append((state, move))
                board.push(move)
            
            game_data.append((moves, reward))
    
    return game_data

def board_to_input_simple(board):
    """Simple board to input conversion."""
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
    return input_array.flatten()

def train_from_games():
    """Train the RL agent from played games."""
    agent = RLChessAgent()
    
    # Load game data
    all_game_data = []
    for file in os.listdir(TRAIN_FOLDER):
        if file.endswith(".pgn"):
            file_path = os.path.join(TRAIN_FOLDER, file)
            print(f"Processing {file_path}...")
            all_game_data.extend(parse_pgn_file_rl(file_path))
    
    if not all_game_data:
        print("No game data found for training!")
        return
    
    print(f"Training on {len(all_game_data)} games...")
    
    # Train from game outcomes
    for game_moves, final_reward in all_game_data:
        for i, (state, move) in enumerate(game_moves):
            # Calculate discounted reward
            steps_to_end = len(game_moves) - i - 1
            discounted_reward = final_reward * (agent.gamma ** steps_to_end)
            
            # Get next state
            if i < len(game_moves) - 1:
                next_state = game_moves[i + 1][0]
                done = False
            else:
                next_state = state  # Terminal state
                done = True
            
            # Store experience
            agent.remember(state, move, discounted_reward, next_state, done)
    
    # Train on experiences
    print("Training neural network...")
    for epoch in range(50):
        agent.replay_train()
        if epoch % 10 == 0:
            print(f"Epoch {epoch}, Epsilon: {agent.epsilon:.3f}")
    
    # Update target model
    agent.update_target_model()
    
    # Save model
    agent.model.save(MODEL_PATH, save_format='keras')
    print(f"RL model saved to {MODEL_PATH}")

def self_play_training(num_games=100):
    """Train through self-play."""
    agent = RLChessAgent()
    
    print(f"Starting self-play training for {num_games} games...")
    
    for game_num in range(num_games):
        board = chess.Board()
        game_moves = []
        
        # Play a complete game
        move_count = 0
        while not board.is_game_over() and move_count < 200:  # Limit game length
            state = agent.board_to_input(board).flatten()
            move = agent.choose_move(board, training=True)
            
            if move is None:
                break
            
            game_moves.append((state, move))
            board.push(move)
            move_count += 1
        
        # Determine game result
        result = board.result()
        if result == "1-0":
            reward = 1.0
        elif result == "0-1":
            reward = -1.0
        else:
            reward = 0.0
        
        # Store experiences
        for i, (state, move) in enumerate(game_moves):
            steps_to_end = len(game_moves) - i - 1
            discounted_reward = reward * (agent.gamma ** steps_to_end)
            
            if i < len(game_moves) - 1:
                next_state = game_moves[i + 1][0]
                done = False
            else:
                next_state = state
                done = True
            
            agent.remember(state, move, discounted_reward, next_state, done)
        
        # Train periodically
        if game_num % 10 == 0:
            agent.replay_train()
            agent.update_target_model()
            print(f"Game {game_num}, Result: {result}, Epsilon: {agent.epsilon:.3f}")
    
    # Final training
    for _ in range(20):
        agent.replay_train()
    
    agent.model.save(MODEL_PATH, save_format='keras')
    print(f"Self-play training completed. Model saved to {MODEL_PATH}")

if __name__ == "__main__":
    print("Chess RL Training")
    
    # Check if running from GUI (no interactive input available)
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--auto":
        # Auto mode: train from existing games
        train_from_games()
    else:
        # Interactive mode
        print("1. Train from existing games")
        print("2. Self-play training")
        choice = input("Choose training mode (1 or 2): ")
        
        if choice == "1":
            train_from_games()
        elif choice == "2":
            self_play_training()
        else:
            print("Invalid choice. Training from existing games...")
            train_from_games()
