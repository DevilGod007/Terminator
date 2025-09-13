"""
Chess AI Training Selector

This script helps you choose between supervised learning and reinforcement learning training.
"""
import os
import sys

def main():
    print("="*60)
    print("           CHESS AI TRAINING SELECTOR")
    print("="*60)
    print()
    print("Your chess engine can be trained in two ways:")
    print()
    print("1. SUPERVISED LEARNING (Original approach)")
    print("   - Learns from move patterns in PGN files")
    print("   - Uses move numbers as training targets")
    print("   - Faster training, more stable")
    print("   - File: train_custom.py")
    print()
    print("2. REINFORCEMENT LEARNING (New approach)")
    print("   - Learns from game outcomes (win/loss/draw)")
    print("   - Uses exploration and exploitation")
    print("   - More advanced, potentially stronger")
    print("   - File: train_rl.py")
    print()
    print("="*60)
    
    while True:
        choice = input("Choose training method (1 for Supervised, 2 for RL): ").strip()
        
        if choice == "1":
            print("\nRunning SUPERVISED LEARNING training...")
            os.system("python train_custom.py")
            break
        elif choice == "2":
            print("\nRunning REINFORCEMENT LEARNING training...")
            os.system("python train_rl.py")
            break
        else:
            print("Please enter 1 or 2")

if __name__ == "__main__":
    main()
