"""
Chess AI Environment Checker
Quick check to see if your environment is properly set up.
"""

import os
import sys

def check_environment():
    print("Chess AI Environment Check")
    print("=" * 40)
    
    # Check Python version
    version = sys.version_info
    print(f"Python Version: {version.major}.{version.minor}.{version.micro}")
    if version.major >= 3 and version.minor >= 8:
        print("✅ Python version OK")
    else:
        print("❌ Python version too old (need 3.8+)")
    
    # Check virtual environment
    venv_path = os.path.join("myenv", "Scripts", "python.exe")
    if os.path.exists(venv_path):
        print("✅ Virtual environment found")
    else:
        print("❌ Virtual environment not found")
        print("   Run: python setup_env.py")
    
    # Check key files
    key_files = [
        "train_rl.py",
        "engine.py", 
        "custom_game.py",
        "requirements.txt"
    ]
    
    print("\nKey Files:")
    for file in key_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} missing")
    
    # Check packages
    print("\nPackage Check:")
    packages = {
        "chess": "Python Chess",
        "numpy": "NumPy",
        "tensorflow": "TensorFlow",
        "pygame": "Pygame",
        "h5py": "HDF5 Support"
    }
    
    for package, name in packages.items():
        try:
            __import__(package)
            print(f"✅ {name}")
        except ImportError:
            print(f"❌ {name} not installed")
    
    print("\n" + "=" * 40)
    print("If any items show ❌, run: python setup_env.py")

if __name__ == "__main__":
    check_environment()
