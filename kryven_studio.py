import streamlit as st
import requests
import json
import re
from datetime import datetime

# --- Sprach- und Konfigurationseinstellungen ---

LANGUAGES = {
    "de": {
        "page_title": "Kryven AI Studio",
        "settings_title": "⚙️ Einstellungen",
        "api_key_label": "Kryven API-Key",
        "api_key_help": "Dein API-Key von kryven.cc",
        "language_label": "Sprache",
        "mode_label": "Modus",
        "mode_t2i": "Text zu Bild",
        "mode_i2v": "Bild zu Video",
        "main_title": "🎨 Kryven AI Studio",
        "main_caption": "Erstelle hochwertige Bilder und Videos basierend auf der offiziellen Kryven API.",
        "t2i_header": "Text zu Bild / Bild zu Bild",
        "prompt_label": "Was möchtest du erstellen? (Prompt)",
        "prompt_placeholder_t2i": "Ein Astronaut reitet auf einem Pferd im Weltall...",
        "model_type_label": "Modell-Typ",
        "model_type_help": "`a2e` ist Standard, `seedream` für Img2Img empfohlen.",
        "aspect_ratio_label": "Seitenverhältnis",
        "i2i_url_label": "Optionale Bild-URL (für Bild-zu-Bild)",
        "i2i_url_placeholder": "https://example.com/my-image.jpg",
        "generate_btn_image": "🚀 Bild generieren",
        "i2v_header": "Bild zu Video",
        "i2v_url_label": "URL des zu animierenden Bildes",
        "i2v_url_placeholder": "https://example.com/static-image.jpg",
        "i2v_prompt_label": "Optionale Anweisungen für die Animation",
        "i2v_prompt_placeholder": "Das Wasser fällt aggressiv nach unten...",
        "generate_btn_video": "🚀 Video generieren",
        "error_api_key": "Bitte gib zuerst deinen API-Key in der Seitenleiste ein!",
        "warning_prompt": "Bitte gib einen Prompt ein.",
        "warning_init_image": "Bitte gib eine URL für das zu animierende Bild ein.",
        "spinner_text": "Kryven KI arbeitet... Bitte warten.",
        "success_generation": "Erfolgreich generiert!",
        "generated_image_caption": "Generiertes Bild:",
        "download_button": "Herunterladen",
        "download_failed": "Download fehlgeschlagen:",
        "error_no_url": "Konnte keine URL in der API-Antwort finden.",
        "error_invalid_response": "Ungültige oder leere Antwort von der API erhalten.",
        "info_credits": "Hinweis: Credits werden bei jeder erfolgreichen Generierung auf kryven.cc abgebucht. Video-Generierung kostet 30.000 Tokens.",
        "disclaimer": "Dies ist ein inoffizielles Community-Projekt und steht in keiner Verbindung zum Kryven-Team."
    },
    "en": {
        "page_title": "Kryven AI Studio",
        "settings_title": "⚙️ Settings",
        "api_key_label": "Kryven API Key",
        "api_key_help": "Your API key from kryven.cc",
        "language_label": "Language",
        "mode_label": "Mode",
        "mode_t2i": "Text to Image",
        "mode_i2v": "Image to Video",
        "main_title": "🎨 Kryven AI Studio",
        "main_caption": "Create high-quality images and videos based on the official Kryven API.",
        "t2i_header": "Text to Image / Image to Image",
        "prompt_label": "What do you want to create? (Prompt)",
        "prompt_placeholder_t2i": "An astronaut riding a horse in space...",
        "model_type_label": "Model Type",
        "model_type_help": "`a2e` is standard, `seedream` is recommended for Img2Img.",
        "aspect_ratio_label": "Aspect Ratio",
        "i2i_url_label": "Optional Image URL (for Image-to-Image)",
        "i2i_url_placeholder": "https://example.com/my-image.jpg",
        "generate_btn_image": "🚀 Generate Image",
        "i2v_header": "Image to Video",
        "i2v_url_label": "URL of the image to animate",
        "i2v_url_placeholder": "https://example.com/static-image.jpg",
        "i2v_prompt_label": "Optional instructions for the animation",
        "i2v_prompt_placeholder": "The water is crashing down aggressively...",
        "generate_btn_video": "🚀 Generate Video",
        "error_api_key": "Please enter your API key in the sidebar first!",
        "warning_prompt": "Please enter a prompt.",
        "warning_init_image": "Please enter a URL for the image to animate.",
        "spinner_text": "Kryven AI is working... Please wait.",
        "success_generation": "Successfully generated!",
        "generated_image_caption": "Generated Image:",
        "download_button": "Download",
        "download_failed": "Download failed:",
        "error_no_url": "Could not find a URL in the API response.",
        "error_invalid_response": "Received an invalid or empty response from the API.",
        "info_credits": "Note: Credits are deducted from kryven.cc for each successful generation. Video generation costs 30,000 tokens.",
        "disclaimer": "This is an unofficial community project and is not affiliated with the Kryven team."
    }
}

# Initialisiere den Session State
if "lang" not in st.session_state:
    st.session_state.lang = "en"
if "generation_result" not in st.session_state:
    st.session_state.generation_result = None
if "last_prompt" not in st.session_state:
    st.session_state.last_prompt = ""

# Lade die aktuelle Sprache
lang = LANGUAGES[st.session_state.lang]

st.set_page_config(page_title=lang["page_title"], page_icon="🎨", layout="wide")

# API-Endpunkte
IMAGE_API_URL = "https://kryven.cc/v1/images/generate"
VIDEO_API_URL = "https://kryven.cc/v1/videos/generate"

# --- Styling ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #ff4b4b; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- API-Funktionen ---
def call_kryven_api(api_key, endpoint, payload):
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
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
    if not prompt_text: return "generated_media"
    s = re.sub(r'[^a-z0-9\s]', '', prompt_text.lower())
    s = re.sub(r'\s+', '_', s).strip('_')
    return s[:50]

# --- UI-Funktionen ---
def display_result():
    if st.session_state.generation_result:
        result_type = st.session_state.generation_result["type"]
        result_url = st.session_state.generation_result["url"]
        prompt_text = st.session_state.last_prompt
        st.success(lang["success_generation"])
        
        if result_type == "image":
            st.image(result_url, caption=f"{lang['generated_image_caption']} {prompt_text}", use_container_width=True)
            try:
                res = requests.get(result_url)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                file_name = f"{timestamp}_{create_safe_filename(prompt_text)}.png"
                st.download_button(lang["download_button"], res.content, file_name, "image/png")
            except requests.exceptions.RequestException as e:
                st.warning(f"{lang['download_failed']} {e}")
        elif result_type == "video":
            st.video(result_url)
            try:
                res = requests.get(result_url)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                file_name = f"{timestamp}_{create_safe_filename(prompt_text)}.mp4"
                st.download_button(lang["download_button"], res.content, file_name, "video/mp4")
            except requests.exceptions.RequestException as e:
                st.warning(f"{lang['download_failed']} {e}")

# --- Sidebar ---
st.sidebar.title(lang["settings_title"])
api_key = st.sidebar.text_input(lang["api_key_label"], type="password", help=lang["api_key_help"])

lang_options_map = {"Deutsch": "de", "English": "en"}
lang_display_options = list(lang_options_map.keys())
# Finde den Index der aktuell ausgewählten Sprache für die Anzeige
current_lang_display = next(key for key, value in lang_options_map.items() if value == st.session_state.lang)
selected_lang_index = lang_display_options.index(current_lang_display)

# Erstelle die Selectbox
selected_language_display = st.sidebar.selectbox(
    lang["language_label"],
    lang_display_options,
    index=selected_lang_index
)

# Aktualisiere die Sprache im State, falls sie sich geändert hat
new_lang_code = lang_options_map[selected_language_display]
if st.session_state.lang != new_lang_code:
    st.session_state.lang = new_lang_code
    st.rerun()

st.sidebar.divider()
mode_options = [lang["mode_t2i"], lang["mode_i2v"]]
mode = st.sidebar.radio(lang["mode_label"], mode_options)

st.sidebar.divider()
st.sidebar.markdown(f"<small>{lang['disclaimer']}</small>", unsafe_allow_html=True)

# --- Hauptbereich ---
st.title(lang["main_title"])
st.caption(lang["main_caption"])

payload = {}
endpoint = ""
generate_btn_label = ""

if mode == lang["mode_t2i"]:
    st.header(lang["t2i_header"])
    prompt = st.text_area(lang["prompt_label"], placeholder=lang["prompt_placeholder_t2i"], height=150)
    col1, col2 = st.columns(2)
    with col1:
        model_type = st.selectbox(lang["model_type_label"], ["a2e", "seedream"], help=lang["model_type_help"])
    with col2:
        aspect_ratio = st.selectbox(lang["aspect_ratio_label"], ["16:9", "1:1", "9:16", "4:3", "3:2"])
    input_image_url = st.text_input(lang["i2i_url_label"], placeholder=lang["i2i_url_placeholder"])
    endpoint = IMAGE_API_URL
    payload = {"prompt": prompt, "model_type": model_type, "aspect_ratio": aspect_ratio}
    if input_image_url: payload["input_images"] = [input_image_url]
    generate_btn_label = lang["generate_btn_image"]

elif mode == lang["mode_i2v"]:
    st.header(lang["i2v_header"])
    init_image_url = st.text_input(lang["i2v_url_label"], placeholder=lang["i2v_url_placeholder"])
    prompt = st.text_area(lang["i2v_prompt_label"], placeholder=lang["i2v_prompt_placeholder"], height=100)
    endpoint = VIDEO_API_URL
    payload = {"init_image": init_image_url}
    if prompt: payload["prompt"] = prompt
    generate_btn_label = lang["generate_btn_video"]

# --- Generierungs-Logik ---
_, col_btn, _ = st.columns([1, 1, 1])
with col_btn:
    if st.button(generate_btn_label):
        is_valid = True
        if not api_key:
            st.error(lang["error_api_key"])
            is_valid = False
        if mode == lang["mode_t2i"] and not payload.get("prompt"):
            st.warning(lang["warning_prompt"])
            is_valid = False
        if mode == lang["mode_i2v"] and not payload.get("init_image"):
            st.warning(lang["warning_init_image"])
            is_valid = False
        if is_valid:
            with st.spinner(lang["spinner_text"]):
                api_response = call_kryven_api(api_key, endpoint, payload)
                if api_response and "data" in api_response and api_response["data"]:
                    url = api_response["data"][0].get("url")
                    if url:
                        result_type = "video" if mode == lang["mode_i2v"] else "image"
                        st.session_state.generation_result = {"type": result_type, "url": url}
                        st.session_state.last_prompt = payload.get("prompt", "")
                    else:
                        st.error(lang["error_no_url"])
                        st.session_state.generation_result = None
                else:
                    st.error(lang["error_invalid_response"])
                    st.session_state.generation_result = None
            st.rerun()

# Zeige das Ergebnis aus dem Session State an
display_result()

st.divider()
st.info(lang["info_credits"])