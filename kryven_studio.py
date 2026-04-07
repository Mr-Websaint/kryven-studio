import streamlit as st
import requests
import json
import re
from datetime import datetime

# --- Konfiguration & Initialisierung ---

st.set_page_config(page_title="Kryven AI Studio", page_icon="🎨", layout="wide")

# API-Endpunkte (fest codiert gemäss Doku)
IMAGE_API_URL = "https://kryven.cc/v1/images/generate"
VIDEO_API_URL = "https://kryven.cc/v1/videos/generate"

# Initialisiere den Session State
if "generation_result" not in st.session_state:
    st.session_state.generation_result = None
if "last_prompt" not in st.session_state:
    st.session_state.last_prompt = ""

# --- Styling ---

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #ff4b4b;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# --- API-Funktionen ---

def call_kryven_api(api_key, endpoint, payload):
    """Kapselt den API-Aufruf. Gibt die JSON-Antwort bei Erfolg oder None zurück."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(endpoint, data=json.dumps(payload), headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Fehler bei der API-Anfrage: {e}")
        if e.response is not None:
            try:
                st.error(f"API-Antwort (Status {e.response.status_code}): {e.response.json()}")
            except json.JSONDecodeError:
                st.error(f"API-Antwort (Status {e.response.status_code}): {e.response.text}")
        return None

def create_safe_filename(prompt_text):
    """Erstellt einen sicheren und aussagekräftigen Dateinamen aus dem Prompt."""
    if not prompt_text:
        return "generated_media"
    # Entferne nicht-alphanumerische Zeichen und ersetze Leerzeichen durch Unterstriche
    s = re.sub(r'[^a-z0-9\s]', '', prompt_text.lower())
    s = re.sub(r'\s+', '_', s).strip('_')
    # Kürze auf eine vernünftige Länge
    return s[:50]

# --- UI-Funktionen ---

def display_result():
    """Zeigt das im Session State gespeicherte Ergebnis an."""
    if st.session_state.generation_result:
        result_type = st.session_state.generation_result["type"]
        result_url = st.session_state.generation_result["url"]
        prompt_text = st.session_state.last_prompt

        st.success("Erfolgreich generiert!")
        
        if result_type == "image":
            st.image(result_url, caption=f"Generiertes Bild: {prompt_text}", use_container_width=True)
            try:
                res = requests.get(result_url)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                file_name = f"{timestamp}_{create_safe_filename(prompt_text)}.png"
                st.download_button("Bild herunterladen", res.content, file_name, "image/png")
            except requests.exceptions.RequestException as e:
                st.warning(f"Download fehlgeschlagen: {e}")

        elif result_type == "video":
            st.video(result_url)
            try:
                res = requests.get(result_url)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                file_name = f"{timestamp}_{create_safe_filename(prompt_text)}.mp4"
                st.download_button("Video herunterladen", res.content, file_name, "video/mp4")
            except requests.exceptions.RequestException as e:
                st.warning(f"Download fehlgeschlagen: {e}")

# --- Sidebar ---

st.sidebar.title("⚙️ Einstellungen")
api_key = st.sidebar.text_input("Kryven API-Key", type="password", help="Dein API-Key von kryven.cc")
st.sidebar.divider()
mode = st.sidebar.radio("Modus", ["Text zu Bild", "Bild zu Video"])

# --- Hauptbereich ---

st.title("🎨 Kryven AI Studio")
st.caption("Erstelle hochwertige Bilder und Videos basierend auf der offiziellen Kryven API.")

payload = {}
endpoint = ""
generate_btn_label = ""

if mode == "Text zu Bild":
    st.header("Text zu Bild / Bild zu Bild")
    prompt = st.text_area("Was möchtest du erstellen? (Prompt)", placeholder="Ein Astronaut reitet auf einem Pferd im Weltall...", height=150)
    
    col1, col2 = st.columns(2)
    with col1:
        model_type = st.selectbox("Modell-Typ", ["a2e", "seedream"], help="`a2e` ist Standard, `seedream` für Img2Img empfohlen.")
    with col2:
        aspect_ratio = st.selectbox("Seitenverhältnis", ["16:9", "1:1", "9:16", "4:3", "3:2"])

    input_image_url = st.text_input("Optionale Bild-URL (für Bild-zu-Bild)", placeholder="https://example.com/my-image.jpg")

    endpoint = IMAGE_API_URL
    payload = {"prompt": prompt, "model_type": model_type, "aspect_ratio": aspect_ratio}
    if input_image_url:
        payload["input_images"] = [input_image_url]
    
    generate_btn_label = "🚀 Bild generieren"

elif mode == "Bild zu Video":
    st.header("Bild zu Video")
    init_image_url = st.text_input("URL des zu animierenden Bildes", placeholder="https://example.com/static-image.jpg")
    prompt = st.text_area("Optionale Anweisungen für die Animation", placeholder="Das Wasser fällt aggressiv nach unten...", height=100)

    endpoint = VIDEO_API_URL
    payload = {"init_image": init_image_url}
    if prompt:
        payload["prompt"] = prompt
        
    generate_btn_label = "🚀 Video generieren"


# --- Generierungs-Logik ---

_, col_btn, _ = st.columns([1, 1, 1])
with col_btn:
    if st.button(generate_btn_label):
        is_valid = True
        if not api_key:
            st.error("Bitte gib zuerst deinen API-Key in der Seitenleiste ein!")
            is_valid = False
        
        if mode == "Text zu Bild" and not payload.get("prompt"):
            st.warning("Bitte gib einen Prompt ein.")
            is_valid = False
            
        if mode == "Bild zu Video" and not payload.get("init_image"):
            st.warning("Bitte gib eine URL für das zu animierende Bild ein.")
            is_valid = False

        if is_valid:
            with st.spinner(f"Kryven KI arbeitet... Bitte warten."):
                api_response = call_kryven_api(api_key, endpoint, payload)
                
                if api_response and "data" in api_response and api_response["data"]:
                    url = api_response["data"][0].get("url")
                    if url:
                        result_type = "video" if mode == "Bild zu Video" else "image"
                        st.session_state.generation_result = {"type": result_type, "url": url}
                        st.session_state.last_prompt = payload.get("prompt", "")
                    else:
                        st.error("Konnte keine URL in der API-Antwort finden.")
                        st.session_state.generation_result = None
                else:
                    st.error("Ungültige oder leere Antwort von der API erhalten.")
                    st.session_state.generation_result = None
            
            # Trigger a rerun to display the new result immediately
            st.rerun()

# Zeige das Ergebnis aus dem Session State an
display_result()

st.divider()
st.info("Hinweis: Credits werden bei jeder erfolgreichen Generierung auf kryven.cc abgebucht. Video-Generierung kostet 30.000 Tokens.")