"""
Chess AI Environment Setup Script
This script sets up the Python environment for your RL chess engine.
"""

import os
import subprocess
import sys

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            return True
        else:
            print(f"❌ {description} failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} failed with exception: {e}")
        return False

def check_python_version():
    """Check if Python version is suitable."""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor} is suitable")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor} is too old. Need Python 3.8+")
        return False

def setup_virtual_environment():
    """Create and activate virtual environment."""
    venv_path = "myenv"
    
    if os.path.exists(venv_path):
        print(f"✅ Virtual environment '{venv_path}' already exists")
        return True
    
    print(f"\n🏗️  Creating virtual environment '{venv_path}'...")
    
    # Create virtual environment
    if run_command(f"python -m venv {venv_path}", "Creating virtual environment"):
        print(f"✅ Virtual environment created at: {os.path.abspath(venv_path)}")
        return True
    else:
        print("❌ Failed to create virtual environment")
        return False

def install_packages():
    """Install required packages."""
    venv_python = os.path.join("myenv", "Scripts", "python.exe")
    venv_pip = os.path.join("myenv", "Scripts", "pip.exe")
    
    if not os.path.exists(venv_python):
        print("Virtual environment not found. Using system Python...")
        venv_python = "python"
        venv_pip = "pip"
    else:
        # Use absolute paths to avoid issues
        venv_python = os.path.abspath(venv_python)
        venv_pip = os.path.abspath(venv_pip)
    
    print(f"\n📦 Installing packages...")
    
    # Upgrade pip first
    run_command(f'{venv_pip} install --upgrade pip', "Upgrading pip")
    
    # Install from requirements.txt
    if os.path.exists("requirements.txt"):
        run_command(f'{venv_pip} install -r requirements.txt', "Installing from requirements.txt")
    else:
        # Install packages individually
        packages = [
            "pygame", "chess", "numpy", "tensorflow", 
            "kivy", "matplotlib", "scikit-learn"
        ]
        
        for package in packages:
            run_command(f'{venv_pip} install {package}', f"Installing {package}")
    
    return True

def test_imports():
    """Test if all required packages can be imported."""
    venv_python = os.path.join("myenv", "Scripts", "python.exe")
    if not os.path.exists(venv_python):
        venv_python = "python"
    
    print(f"\n🧪 Testing package imports...")
    
    test_script = '''
import sys
packages = {
    "pygame": "Pygame",
    "chess": "Python Chess",
    "numpy": "NumPy", 
    "tensorflow": "TensorFlow",
    "kivy": "Kivy",
    "matplotlib": "Matplotlib",
    "sklearn": "Scikit-learn"
}

success_count = 0
for package, name in packages.items():
    try:
        __import__(package)
        print(f"✅ {name} imported successfully")
        success_count += 1
    except ImportError as e:
        print(f"❌ {name} import failed: {e}")

print(f"\\n📊 Import Results: {success_count}/{len(packages)} packages imported successfully")
'''
    
    with open("test_imports.py", "w") as f:
        f.write(test_script)
    
    run_command(f'"{venv_python}" test_imports.py', "Testing package imports")
    
    # Clean up
    if os.path.exists("test_imports.py"):
        os.remove("test_imports.py")

def create_activation_script():
    """Create scripts to easily activate the environment."""
    
    # Windows batch script
    batch_script = '''@echo off
echo Activating Chess AI Environment...
call myenv\\Scripts\\activate.bat
echo Environment activated! You can now run:
echo   python custom_game.py
echo   python train_rl.py
echo   python kvgui.py
cmd /k
'''
    
    with open("activate_env.bat", "w") as f:
        f.write(batch_script)
    
    # PowerShell script
    ps_script = '''Write-Host "Activating Chess AI Environment..." -ForegroundColor Green
& ".\\myenv\\Scripts\\Activate.ps1"
Write-Host "Environment activated! You can now run:" -ForegroundColor Yellow
Write-Host "  python custom_game.py" -ForegroundColor Cyan
Write-Host "  python train_rl.py" -ForegroundColor Cyan
Write-Host "  python kvgui.py" -ForegroundColor Cyan
'''
    
    with open("activate_env.ps1", "w") as f:
        f.write(ps_script)
    
    print("✅ Created activation scripts:")
    print("   - activate_env.bat (for Command Prompt)")
    print("   - activate_env.ps1 (for PowerShell)")

def main():
    print("="*60)
    print("     CHESS AI - REINFORCEMENT LEARNING ENVIRONMENT SETUP")
    print("="*60)
    
    # Check Python version
    if not check_python_version():
        print("\\n❌ Setup failed: Python version too old")
        return
    
    # Setup virtual environment
    if not setup_virtual_environment():
        print("\\n❌ Setup failed: Could not create virtual environment")
        return
    
    # Install packages
    install_packages()
    
    # Test imports
    test_imports()
    
    # Create activation scripts
    create_activation_script()
    
    print("\\n" + "="*60)
    print("🎉 SETUP COMPLETE!")
    print("="*60)
    print("\\nYour RL Chess Engine environment is ready!")
    print("\\nTo use your chess engine:")
    print("1. Run 'activate_env.bat' (Command Prompt) or 'activate_env.ps1' (PowerShell)")
    print("2. Then run any of these:")
    print("   - python custom_game.py    (Play chess)")
    print("   - python train_rl.py       (Train with RL)")
    print("   - python kvgui.py          (GUI interface)")
    print("   - python train_selector.py (Choose training method)")
    print("\\nFor your research paper, you can now correctly say:")
    print("✅ 'Reinforcement Learning Chess Engine'")
    print("✅ 'Q-learning with experience replay'")
    print("✅ 'Epsilon-greedy exploration strategy'")

if __name__ == "__main__":
    main()
