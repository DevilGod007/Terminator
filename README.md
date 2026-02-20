# Chess AI - Reinforcement Learning Conversion

## Overview
Your chess engine has been converted from **Supervised Learning** to **Reinforcement Learning**!

## Key Changes Made

### 1. New RL Training File: `train_rl.py`
- **RLChessAgent class**: Implements Q-learning with experience replay
- **Exploration vs Exploitation**: Uses epsilon-greedy strategy
- **Game outcome learning**: Learns from wins/losses/draws instead of move numbers
- **Self-play capability**: Can train by playing against itself

### 2. Updated Engine: `engine.py`
- Added exploration during gameplay (optional)
- Now interprets neural network outputs as Q-values
- Better move selection based on value estimates

### 3. Enhanced Game Saving: `custom_game.py`
- Properly saves game results (1-0, 0-1, 1/2-1/2) for RL training
- Results are used as reward signals

### 4. Updated GUI: `kvgui.py`
- Now calls RL training instead of supervised training
- Seamless integration with new training method

## How Reinforcement Learning Works

### Before (Supervised Learning):
```python
# Learned from move patterns
evaluation = board.fullmove_number  # Simple heuristic
model.fit(board_positions, evaluations)
```

### After (Reinforcement Learning):
```python
# Learns from game outcomes
if game_result == "1-0":
    reward = 1.0    # Win
elif game_result == "0-1":
    reward = -1.0   # Loss
else:
    reward = 0.0    # Draw

# Updates Q-values based on rewards
agent.update_policy(game_moves, reward)
```

## Training Options

### Option 1: Train from Existing Games
```bash
python train_rl.py
# Choose option 1
```
- Uses games you've already played
- Learns from human vs AI games
- Faster initial training

### Option 2: Self-Play Training
```bash
python train_rl.py
# Choose option 2
```
- AI plays against itself
- Discovers new strategies
- More advanced training method

## Key RL Concepts Implemented

### 1. **Q-Learning**
- Neural network predicts Q-values (expected future rewards)
- Updates based on actual game outcomes

### 2. **Experience Replay**
- Stores game experiences in memory buffer
- Trains on random batches for stability

### 3. **Epsilon-Greedy Exploration**
- 90% exploitation (use best known moves)
- 10% exploration (try random moves)
- Epsilon decays over time

### 4. **Reward Discounting**
- Future rewards are discounted by gamma (0.95)
- Moves closer to game end have higher impact

## Model Architecture

```python
# RL Neural Network
Sequential([
    Dense(128, activation="relu"),  # Input layer
    Dense(64, activation="relu"),   # Hidden layer
    Dense(32, activation="relu"),   # Hidden layer  
    Dense(1, activation="linear")   # Q-value output
])
```

## Training Process

1. **Play Games**: AI plays games (against human or itself)
2. **Store Experiences**: Each move and outcome is stored
3. **Sample Batch**: Random batch of experiences selected
4. **Calculate Targets**: Q-values updated based on rewards
5. **Train Network**: Neural network learns from batch
6. **Repeat**: Process continues with new games

## Performance Improvements

With RL training, your chess engine now:
- ✅ **Learns from actual game outcomes**
- ✅ **Explores new strategies**
- ✅ **Adapts to opponent patterns**
- ✅ **Improves through self-play**
- ✅ **Uses proper reward signals**


## Files Overview

| File | Purpose | Type |
|------|---------|------|
| `train_rl.py` | RL training implementation | New |
| `train_custom.py` | Original supervised learning | Original |
| `engine.py` | Chess engine with RL support | Updated |
| `custom_game.py` | Game interface with proper results | Updated |
| `kvgui.py` | GUI with RL training | Updated |
| `train_selector.py` | Choose training method | New |

## Usage

1. **Play games**: Use the GUI to play against AI
2. **Train with RL**: Games automatically trigger RL training
3. **Self-play**: Run `train_rl.py` for advanced training
4. **Compare**: You can still use supervised learning if needed


