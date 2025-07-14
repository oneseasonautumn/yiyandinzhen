import subprocess
import sys
import os

def install_packages(requirements):
    for package in requirements:
        print(f"Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def create_virtualenv(env_name="venv"):
    if not os.path.exists(env_name):
        print(f"Creating virtual environment: {env_name}")
        subprocess.check_call([sys.executable, "-m", "venv", env_name])
        print(f"✅ Virtual environment created in ./{env_name}")
    else:
        print(f"Virtual environment '{env_name}' already exists.")

def main():
    use_venv = input("Do you want to create/use a virtual environment? (y/n): ").lower().startswith("y")
    
    if use_venv:
        create_virtualenv()
        activate_cmd = "venv\\Scripts\\activate" if os.name == "nt" else "source venv/bin/activate"
        print(f"\nTo activate the virtual environment, run:\n  {activate_cmd}")
        print("Then re-run this script inside the virtual environment.")
        return

    print("Installing required packages globally...")
    install_packages(["opencv-python"])

    print("\n✅ Environment setup complete!")

if __name__ == "__main__":
    main()
