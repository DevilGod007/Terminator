import os
import subprocess
import tkinter as tk
from tkinter import messagebox

# Virtual environment Python path
VENV_PYTHON = os.path.join(os.getcwd(), "venv", "Scripts", "python.exe")

# Function to run the chess game and train afterward
def run_custom_game():
    messagebox.showinfo("Starting Game", "The chess game will now start.")
    subprocess.run([VENV_PYTHON, "custom_game.py"])  # Run the game with venv
    messagebox.showinfo("Training Model", "Game finished! Training the model now...")
    subprocess.run([VENV_PYTHON, "train_custom.py"])  # Train after game

# Function to run only the training script
def run_training():
    messagebox.showinfo("Training Model", "Training the model now...")
    subprocess.run([VENV_PYTHON, "train_custom.py"])  # Run training with venv

# Function to quit the application
def quit_app():
    root.quit()

# Create the main window
root = tk.Tk()
root.title("Chess AI Menu")
root.geometry("400x300")
root.configure(bg="#2C3E50")

# Header label
label = tk.Label(root, text="Chess AI Menu", font=("Arial", 20, "bold"), fg="white", bg="#2C3E50")
label.pack(pady=20)

# Buttons
btn_start = tk.Button(root, text="Start Game", font=("Arial", 14), width=20, bg="#3498DB", fg="white",
                      command=run_custom_game)
btn_start.pack(pady=10)

btn_setup = tk.Button(root, text="Setup (Train Model)", font=("Arial", 14), width=20, bg="#27AE60", fg="white",
                      command=run_training)
btn_setup.pack(pady=10)

btn_quit = tk.Button(root, text="Quit", font=("Arial", 14), width=20, bg="#E74C3C", fg="white",
                     command=quit_app)
btn_quit.pack(pady=10)

# Run the GUI loop
root.mainloop()
