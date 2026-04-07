import subprocess
import sys

def run_command(command):
    """Führt einen Shell-Befehl aus und gibt den Output live aus."""
    try:
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
        print(f"Fehler: Befehl '{command[0]}' nicht gefunden. Stelle sicher, dass Git und Python/Pip im Systempfad sind.")
        return -1
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")
        return -1

def main():
    """Führt den Update-Prozess aus."""
    print("=====================================")
    print("=== Kryven AI Studio Updater      ===")
    print("=====================================\n")

    print("Schritt 1: Lokale Änderungen zurücksetzen (git reset --hard)...")
    if run_command(["git", "reset", "--hard"]) != 0:
        print("\nFehler beim Zurücksetzen des Repositories. Abbruch.")
        sys.exit(1)
    print("-> Lokale Änderungen erfolgreich zurückgesetzt.\n")

    print("Schritt 2: Neueste Version vom Server holen (git pull)...")
    if run_command(["git", "pull"]) != 0:
        print("\nFehler beim Herunterladen der neuesten Version. Abbruch.")
        sys.exit(1)
    print("-> Neueste Version erfolgreich heruntergeladen.\n")

    print("Schritt 3: Python-Abhängigkeiten aktualisieren (pip install)...")
    # sys.executable stellt sicher, dass der richtige Python-Interpreter verwendet wird
    if run_command([sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "--upgrade"]) != 0:
        print("\nFehler beim Aktualisieren der Abhängigkeiten.")
        # Dies wird nicht als fataler Fehler behandelt, da die App möglicherweise trotzdem läuft
    else:
        print("-> Abhängigkeiten erfolgreich aktualisiert.\n")

    print("=====================================")
    print("=== Update erfolgreich abgeschlossen! ===")
    print("=====================================\n")
    print("Du kannst die Anwendung jetzt wie gewohnt starten:")
    print("python -m streamlit run kryven_studio.py")

if __name__ == "__main__":
    main()