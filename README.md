♟️ Self Learning Chess Engine
🧠 Description

Self Learning Chess Engine is a Reinforcement Learning–based Chess AI that improves by learning from gameplay outcomes.

The engine uses:

Reinforcement Learning (Q-Learning)

Neural Networks (TensorFlow / Keras)

python-chess for board logic

Kivy GUI for interactive gameplay

The AI learns from:

Human vs AI games

Self-play training

Win / Loss / Draw results

Over time, the engine improves its move selection using reward-based learning.

📦 Installation
1️⃣ Clone the Repository
git clone <your-repo-url>
cd Terminator
2️⃣ Install Requirements

Install all dependencies from requirements.txt:

pip install -r requirements.txt

Make sure you are using Python 3.10 – 3.12.

▶️ Running the Application

After installing dependencies, run either:

python kvgui.py

OR

python menu_gui.py
🛠️ First Time Setup (IMPORTANT)

When the GUI opens:

Click on "Setup"

Allow the environment setup to complete

Then start playing or training

The setup initializes:

Model structure

Training environment

Required folders

Initial model files

📁 Project Structure
Terminator/
│
├── images/
├── train/
├── engine.py
├── custom_game.py
├── train_rl.py
├── train_custom.py
├── train_model.py
├── train_selector.py
├── kvgui.py
├── menu_gui.py
├── requirements.txt
└── README.md
🔁 Training Modes

The engine supports:

Reinforcement Learning training

Self-play training

Supervised learning (legacy support)

Games are saved in the train/ directory and used for learning.

🚀 Features

♟️ Interactive Chess GUI (Kivy)

🧠 Reinforcement Learning with Q-values

🔁 Experience Replay

🎯 Reward-based training

📊 Model inspection utilities

📈 Confusion matrix & evaluation tools
