# Kryven AI Studio 🎨

Ein einfaches, aber leistungsstarkes Web-Frontend für die Kryven AI Media Generation API, erstellt mit Streamlit. Diese Anwendung ermöglicht die intuitive Erstellung von Bildern und Videos über eine grafische Benutzeroberfläche.

## Features

-   **Text-zu-Bild Generierung:** Erstelle Bilder aus Textbeschreibungen.
-   **Bild-zu-Bild Generierung:** Modifiziere ein vorhandenes Bild basierend auf einem Prompt.
-   **Bild-zu-Video Generierung:** Animiere ein statisches Bild zu einem 4-sekündigen Videoclip.
-   **Dynamische Dateinamen:** Heruntergeladene Dateien erhalten automatisch einen Zeitstempel und einen aussagekräftigen Namen.
-   **Persistente Ergebnisse:** Das zuletzt generierte Ergebnis bleibt auch bei Änderungen an den Einstellungen sichtbar.

## Installation

1.  **Klone das Repository:**
    ```bash
    git clone <repository-url>
    cd <repository-folder>
    ```

2.  **Installiere die Abhängigkeiten:**
    Stelle sicher, dass du Python 3.8+ installiert hast.
    ```bash
    pip install -r requirements.txt
    ```

## Ausführung

1.  **API-Key bereitstellen:**
    Du benötigst einen API-Key von [kryven.cc](https://kryven.cc).

2.  **Starte die Streamlit-Anwendung:**
    Führe den folgenden Befehl im Terminal aus:
    ```bash
    streamlit run kryven_studio.py
    ```

3.  **Benutze die Anwendung:**
    -   Öffne die angezeigte URL in deinem Browser.
    -   Gib deinen Kryven API-Key in der Seitenleiste ein.
    -   Wähle den gewünschten Modus, fülle die Felder aus und starte die Generierung!

## Konfiguration

Alle Einstellungen können direkt über die Seitenleiste der Anwendung vorgenommen werden:

-   **Kryven API-Key:** Dein persönlicher Schlüssel für die API-Authentifizierung.
-   **Modus:** Wähle zwischen "Text zu Bild" und "Bild zu Video".
-   **Modell-Typ (für Bilder):** Wähle das zu verwendende Modell (`a2e` oder `seedream`).
-   **Seitenverhältnis (für Bilder):** Definiere das Format des generierten Bildes.
-   **Bild-URL (optional):** Gib eine URL für Bild-zu-Bild-Transformationen an.
-   **URL des zu animierenden Bildes (für Videos):** Die Quelle für die Videoerstellung.