import subprocess
import sys
import os

def run_command(command, capture_output=False):
    """Führt einen Shell-Befehl aus."""
    try:
        if capture_output:
            return subprocess.check_output(command, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace').strip()
        
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace')
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())
        rc = process.poll()
        return rc
    except FileNotFoundError:
        print(f"Error: Command '{command[0]}' not found. Make sure Git and Python/Pip are in the system's PATH.")
        return -1 if not capture_output else None
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e.output}")
        return -1 if not capture_output else None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return -1 if not capture_output else None

def check_for_updates():
    """Prüft, ob eine neue Version im Git-Repository verfügbar ist."""
    print("Checking for updates...")
    
    # 1. Fetch the latest info from the remote
    if run_command(["git", "fetch"]) != 0:
        print("Could not fetch updates from the remote repository. Aborting.")
        return False, True # Return error

    # 2. Get local and remote commit hashes
    local_hash = run_command(["git", "rev-parse", "HEAD"], capture_output=True)
    remote_hash = run_command(["git", "rev-parse", "@{u}"], capture_output=True)
    
    if local_hash is None or remote_hash is None:
        print("Could not determine local or remote version. Aborting.")
        return False, True # Return error

    if local_hash == remote_hash:
        print("You are already on the latest version.")
        return False, False # No update, no error
    else:
        print("A new version is available.")
        return True, False # Update available, no error

def main():
    """Führt den Update-Prozess aus."""
    print("=====================================")
    print("=== Kryven AI Studio Updater      ===")
    print("=====================================\n")

    update_available, error = check_for_updates()

    if error:
        sys.exit(1)
        
    if not update_available:
        sys.exit(0)

    # Ask for confirmation
    choice = input("\nDo you want to perform the update now? [y/n]: ").lower().strip()
    if choice not in ['y', 'yes']:
        print("Update cancelled by user.")
        sys.exit(0)

    print("\nStep 1: Resetting local changes (git reset --hard)...")
    if run_command(["git", "reset", "--hard", "origin/main"]) != 0:
        print("\nError resetting the repository. Aborting.")
        sys.exit(1)
    print("-> Local changes successfully reset.\n")

    print("Step 2: Pulling the latest version (git pull)...")
    if run_command(["git", "pull"]) != 0:
        print("\nError pulling the latest version. Aborting.")
        sys.exit(1)
    print("-> Latest version successfully pulled.\n")

    print("Step 3: Updating Python dependencies (pip install)...")
    if run_command([sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "--upgrade"]) != 0:
        print("\nWarning: Failed to update dependencies. The application might still work.")
    else:
        print("-> Dependencies successfully updated.\n")

    print("=====================================")
    print("=== Update completed successfully!  ===")
    print("=====================================\n")
    print("You can now start the application as usual:")
    print("python -m streamlit run kryven_studio.py")

if __name__ == "__main__":
    # We need to be in the script's directory for git commands to work correctly
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()