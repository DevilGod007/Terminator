# ♟️ Self Learning Chess Engine

## 🧠 Overview

**Self Learning Chess Engine** is a Reinforcement Learning–based Chess AI that improves over time by learning from gameplay results.

The engine combines:

- Reinforcement Learning (Q-Learning)
- Neural Networks (TensorFlow / Keras)
- python-chess for board logic
- Kivy GUI for interactive gameplay

The AI learns from:
- Human vs AI games  
- Self-play training  
- Win / Loss / Draw outcomes  

Over time, the engine improves its move selection using reward-based learning.
note:do not use venv for this project
---

## 📦 Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/self-learning-chess-engine.git
cd self-learning-chess-engine
pip install -r requirements.txt
python kvgui.py
or
python menu_gui.py

