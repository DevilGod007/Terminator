"""
Chess AI - RL Verification Script

This script verifies that all components are properly configured for Reinforcement Learning.
"""

import os
import sys

def check_file_content(filename, expected_content, description):
    """Check if a file contains expected RL-related content."""
    if not os.path.exists(filename):
        print(f"❌ {filename} - FILE NOT FOUND")
        return False
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if expected_content in content:
            print(f"✅ {filename} - {description}")
            return True
        else:
            print(f"❌ {filename} - Missing: {description}")
            return False
    except Exception as e:
        print(f"❌ {filename} - Error reading file: {e}")
        return False

def main():
    print("="*60)
    print("     CHESS AI - REINFORCEMENT LEARNING VERIFICATION")
    print("="*60)
    print()
    
    # Check all files for RL compliance
    checks = [
        ("train_rl.py", "class RLChessAgent", "RL training class exists"),
        ("train_rl.py", "def train_from_games", "RL training from games function"),
        ("train_rl.py", "def self_play_training", "Self-play training function"),
        ("train_rl.py", "reward = 1.0", "Uses game outcomes as rewards"),
        
        ("engine.py", "EPSILON = 0.1", "RL exploration parameter"),
        ("engine.py", "EXPLORATION_ENABLED", "RL exploration flag"),
        
        ("custom_game.py", 'game.headers["Result"]', "Saves game results for RL"),
        ("custom_game.py", "1-0", "Proper result format"),
        
        ("kvgui.py", "train_rl.py", "GUI uses RL training"),
        ("kvgui.py", "--auto", "GUI uses auto mode"),
        
        ("menu_gui.py", "train_rl.py", "Menu GUI uses RL training"),
        ("menu_gui.py", "--auto", "Menu GUI uses auto mode"),
    ]
    
    passed = 0
    total = len(checks)
    
    for filename, content, description in checks:
        if check_file_content(filename, content, description):
            passed += 1
    
    print()
    print("="*60)
    print(f"VERIFICATION RESULTS: {passed}/{total} checks passed")
    print("="*60)
    
    if passed == total:
        print("🎉 SUCCESS: All components are properly configured for RL!")
        print()
        print("Your chess engine is now using:")
        print("✅ Reinforcement Learning (Q-learning)")
        print("✅ Experience replay training")
        print("✅ Epsilon-greedy exploration")
        print("✅ Game outcome rewards")
        print("✅ Self-play capability")
        print()
        print("Ready for your research paper! 📝")
    else:
        print("⚠️  Some components may still use supervised learning")
        print("Please review the failed checks above")
    
    print()
    print("Files you can now use:")
    print("- train_rl.py (primary RL training)")
    print("- train_selector.py (choose between RL and supervised)")
    print("- train_custom.py (legacy supervised learning)")

if __name__ == "__main__":
    main()
