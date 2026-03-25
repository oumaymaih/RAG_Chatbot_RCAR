import streamlit as st
from pathlib import Path
from chatbot.config import get_llm
from chatbot.retriever import get_retriever
from chatbot.chatbot import ask_chatbot
from datetime import datetime
import uuid

# Bibliothèque d'icones
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
""", unsafe_allow_html=True)

# ---------- CONFIGURATION ----------
st.set_page_config(page_title="RCAR | Chatbot", page_icon="C:/Users/info/OneDrive/Desktop/RAG_Chatbot_RCAR/assets/logo.png", layout="wide")

# ---------- CSS PERSONNALISÉ ----------
st.markdown("""
<style>
    /* === Couleurs principales === */
    :root {
        --primary-green: #2ecc71;
        --primary-green-dark: #27ae60;
        --bg-light: #f8fdf9;
    }

    /* === Boutons === */
    .stButton>button {
        background: linear-gradient(135deg, var(--primary-green), var(--primary-green-dark));
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 12px;
        font-size: 15px;
        font-weight: 500;
        transition: all 0.2s ease-in-out;
        box-shadow: 0px 2px 6px rgba(0,0,0,0.15);
    }
    .stButton>button:hover {
        background: var(--primary-green-dark);
        transform: translateY(-2px);
        box-shadow: 0px 4px 12px rgba(0,0,0,0.2);
    }

    /* === Sidebar === */
    section[data-testid="stSidebar"] {
        background: var(--bg-light);
        backdrop-filter: blur(8px);
        border-right: 2px solid var(--primary-green);
        padding-top: 0px !important;
    }
    .sidebar-title {
        font-size: 18px;
        font-weight: bold;
        color: black;
        margin-top: 20px;
    }
            
    /* === Chat bubbles === */
    .suggestion_title {
        font-size: 18px;
        font-weight: bold;
        color: black;
        margin-top: 20px;
    }


    /* === Chat bubbles === */
    .chat-bubble-user {
        background: var(--primary-green);
        color: white;
        padding: 10px 16px;
        border-radius: 18px 18px 4px 18px;
        margin: 6px 0;
        max-width: 80%;
    }
    .chat-bubble-bot {
        background: #ecfdf5;
        color: #333;
        padding: 10px 16px;
        border-radius: 18px 18px 18px 4px;
        margin: 6px 0;
        max-width: 80%;
        border: 1px solid #d1fae5;
    }

    /* === Input Chat === */
    div[data-baseweb="input"] > input {
        border-radius: 12px;
        border: 2px solid var(--primary-green);
    }

    /* === Animation apparitions === */
    .chat-bubble-user, .chat-bubble-bot {
        animation: fadeIn 0.3s ease-in-out;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
</style>
""", unsafe_allow_html=True)

# ---------- INITIALISATION DES STATES ----------
if "llm" not in st.session_state:
    st.session_state.llm = get_llm()
if "retriever" not in st.session_state:
    st.session_state.retriever = get_retriever()
if "conversations" not in st.session_state:
    st.session_state.conversations = {}
if "current_conv" not in st.session_state:
    conv_id = str(uuid.uuid4())
    st.session_state.current_conv = conv_id
    st.session_state.conversations[conv_id] = []
if "language" not in st.session_state:
    st.session_state.language = "Français"
if "conv_titles" not in st.session_state:
    st.session_state.conv_titles = {}

# ---------- PATHS ----------
LOGO_PATH = Path("C:/Users/info/OneDrive/Desktop/RAG_Chatbot_RCAR/assets/background.png")  

# ---------- SIDEBAR ----------
with st.sidebar:
    st.image(str(LOGO_PATH), width=100)
    
    # st.markdown("<div class='sidebar-title'>📌 Menu</div>", unsafe_allow_html=True)

    # Nouveau chat
    if st.button("+ Nouveau chat"):
        conv_id = str(uuid.uuid4())
        st.session_state.current_conv = conv_id
        st.session_state.conversations[conv_id] = []
        st.session_state.conv_titles[conv_id] = f"Chat - {datetime.now().strftime('%d/%m %H:%M')}"

    # Sélecteur de langue
    st.markdown("<div class='sidebar-title'><i class='fa-solid fa-globe'></i> Langue des réponses</div>", unsafe_allow_html=True)

    # selectbox sans label (label='')
    st.session_state.language = st.selectbox(
        "",
        ["Français", "Anglais", "Arabe"],
        index=["Français", "Anglais", "Arabe"].index(st.session_state.language),
        label_visibility="collapsed"  # masque le label par défaut
    )
    # Liste des conversations
    st.markdown("<div class='sidebar-title'><i class='fa-solid fa-comments'></i> Conversations</div>", unsafe_allow_html=True)
    for conv_id, messages in st.session_state.conversations.items():
        if conv_id not in st.session_state.conv_titles:
            if messages:
                first_msg = messages[0][1][:20] + "..."
                st.session_state.conv_titles[conv_id] = first_msg
            else:
                st.session_state.conv_titles[conv_id] = f"Chat - {datetime.now().strftime('%d/%m %H:%M')}"

        if st.button(f" {st.session_state.conv_titles[conv_id]}", key=f"load_{conv_id}"):
            st.session_state.current_conv = conv_id

        # new_title = st.text_input(
        #     f"Renommer {conv_id[:4]}",
        #     value=st.session_state.conv_titles[conv_id],
        #     key=f"rename_{conv_id}"
        # )
        # st.session_state.conv_titles[conv_id] = new_title

    if st.button(" Supprimer conversation"):
        st.session_state.conversations[st.session_state.current_conv] = []
        st.session_state.conv_titles[st.session_state.current_conv] = f"Chat - {datetime.now().strftime('%d/%m %H:%M')}"

# ---------- AFFICHAGE LOGO PRINCIPAL CENTRÉ ----------
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image(str(LOGO_PATH), width=320)

# ---------- SUGGESTIONS RAPIDES ----------
st.markdown("<div class='suggestion_title'><h4>Suggestions rapides</h4></div>", unsafe_allow_html=True)

# CSS pour boutons suggestions (vert clair) + bulles chat
st.markdown("""
<style>
    /* --- Boutons suggestions --- */
    div[data-testid="stHorizontalBlock"] button {
        background-color: #b9fbc0 !important; /* Vert clair */
        color: white !important;
        border: 1px solid #27ae60 !important;
        border-radius: 12px !important;
        padding: 10px 20px !important;
        font-size: 15px !important;
        font-weight: 500 !important;
    }
    div[data-testid="stHorizontalBlock"] button:hover {
        background-color: #2ecc71 !important; /* Vert foncé au survol */
        color: white !important;
        transform: translateY(-2px);
    }

    /* --- Bulles de chat --- */
    .chat-container {
        display: flex;
        flex-direction: column;
        margin: 8px 0;
    }
    .chat-bubble {
        max-width: 70%;
        padding: 10px 16px;
        border-radius: 18px;
        margin: 4px;
        font-size: 15px;
        font-weight: 400;
        line-height: 1.4;
        word-wrap: break-word;
    }
    .chat-user {
        align-self: flex-end;
        border-bottom-right-radius: 4px;
        background: var(--primary-green);
        color: white;
        padding: 10px 16px;
        border-radius: 18px 18px 4px 18px;
        margin: 6px 0;
        max-width: 80%;

    }
    .chat-bot {
        align-self: flex-start;
        border-bottom-left-radius: 4px;
        background: #ecfdf5;
        color: #333;
        padding: 10px 16px;
        border-radius: 18px 18px 18px 4px;
        margin: 6px 0;
        max-width: 80%;
        border: 1px solid #d1fae5;
    }
</style>
""", unsafe_allow_html=True)

# Réponses statiques pour suggestions rapides
static_responses = {
    "Centres RCAR": "Le RCAR dispose de 4 centres régionaux, à Rabat, Casablanca, Jerada et Laâyoune chacun ouvert de 8h30 à 16h30.",
    "Contact RCAR": "Vous pouvez contacter le RCAR via le numéro 0537-56-99-00 ou par email à contact@rcar.ma.",
    "Offres RCAR": "Le RCAR propose des offres liées à la retraite, la pension et d’autres services sociaux pour les adhérents."
}

# Suggestions rapides
suggestions = {
    "Centres RCAR": "Donne moi des informations sur les Centres de RCAR",
    "Contact RCAR": "Donne moi des informations sur le Contact RCAR",
    "Offres RCAR": "Donne moi des informations sur les Offres RCAR"
}

col1, col2, col3 = st.columns(3)
for (label, query), col in zip(suggestions.items(), [col1, col2, col3]):
    with col:
        if st.button(label, key=f"sugg_{label}", use_container_width=True):
            with st.spinner("🤖 Veuillez patienter..."):
                response = static_responses[label]  # ✅ réponse directe sans rag

            # Historique conversation
            st.session_state.conversations[st.session_state.current_conv].append(("user", query))
            st.session_state.conversations[st.session_state.current_conv].append(("bot", response))

# ---------- CHAT ----------
user_input = st.chat_input("Posez votre question...")

if user_input:
    with st.spinner("🤖 Veuillez patienter..."):
        lang_instruction = f"Réponds strictement en {st.session_state.language.lower()}."
        full_query = f"{user_input}\n\n{lang_instruction}"
        response = ask_chatbot(full_query, st.session_state.llm)

    st.session_state.conversations[st.session_state.current_conv].append(("user", user_input))
    st.session_state.conversations[st.session_state.current_conv].append(("bot", response))

    if len(st.session_state.conversations[st.session_state.current_conv]) == 2:
        st.session_state.conv_titles[st.session_state.current_conv] = user_input[:20] + "..."

# ---------- AFFICHAGE HISTORIQUE ----------
for role, text in st.session_state.conversations[st.session_state.current_conv]:
    if role == "user":
        st.markdown(f"<div class='chat-container'><div class='chat-bubble chat-user'>{text}</div></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-container'><div class='chat-bubble chat-bot'>{text}</div></div>", unsafe_allow_html=True)
