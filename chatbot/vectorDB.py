# vectorDB_from_txt.py

import os
import csv
import logging
from pathlib import Path
from statistics import mean

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from chatbot.logging_config import configure_logging

# ------------ CONFIG ------------
DATA_DIR = Path("C:/Users/info/OneDrive/Desktop/RAG_Chatbot_RCAR/data/csv_files")
TXT_DIR = Path("C:/Users/info/OneDrive/Desktop/RAG_Chatbot_RCAR/data/txt_files")
VECTOR_DB_PATH = Path("C:/Users/info/OneDrive/Desktop/RAG_Chatbot_RCAR/vector_db")

# ------------ STEP 1 : Convert CSV → TXT ------------
def csv_to_txt(csv_path: Path, txt_path: Path):
    """Convertit un CSV en texte brut et le sauvegarde en .txt"""
    try:
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            lines = [" ".join(row).strip() for row in reader if any(row)]
            text = "\n".join(lines)

        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(text)

        logging.info(f"✅ Fichier converti : {csv_path.name} → {txt_path.name} ({len(lines)} lignes)")
    except Exception as e:
        logging.error(f"❌ Erreur conversion {csv_path.name} → {e}")

def convert_all_csv_to_txt():
    TXT_DIR.mkdir(parents=True, exist_ok=True)
    for file in DATA_DIR.glob("*.csv"):
        txt_file = TXT_DIR / (file.stem + ".txt")
        csv_to_txt(file, txt_file)

# ------------ STEP 2 : Chunking ------------
def chunk_texts():
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    all_chunks = []

    for txt_file in TXT_DIR.glob("*.txt"):
        with open(txt_file, "r", encoding="utf-8") as f:
            text = f.read().strip()

        if not text:
            logging.warning(f"⚠️ Fichier vide ignoré : {txt_file.name}")
            continue

        chunks = splitter.split_text(text)
        chunk_stats = [len(c) for c in chunks]

        logging.info(
            f"📂 {txt_file.name} → {len(chunks)} chunks, "
            f"longueur moyenne : {mean(chunk_stats):.1f} caractères"
        )

        # Ajouter source dans metadata
        for chunk in chunks:
            all_chunks.append({"text": chunk, "metadata": {"source": txt_file.name}})

    return all_chunks

# ------------ STEP 3 : Embeddings + VectorDB ------------
def build_or_load_vector_db(chunks=None):
    """
    Charge la VectorDB si elle existe déjà,
    sinon la construit à partir des chunks fournis.
    """
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # --- Si la DB existe déjà → on la recharge
    if VECTOR_DB_PATH.exists():
        try:
            vector_db = FAISS.load_local(VECTOR_DB_PATH, embeddings, allow_dangerous_deserialization=True)
            logging.info(f"📂 VectorDB chargée depuis {VECTOR_DB_PATH} ({vector_db.index.ntotal} vecteurs)")
            return vector_db
        except Exception as e:
            logging.error(f"❌ Erreur chargement VectorDB : {e}. Reconstruction forcée...")

    # --- Sinon → on doit avoir des chunks pour construire
    if not chunks:
        logging.error("❌ Impossible de construire la VectorDB : aucun chunk fourni.")
        return None

    try:
        texts = [c["text"] for c in chunks]
        metadatas = [c["metadata"] for c in chunks]

        vector_db = FAISS.from_texts(texts, embeddings, metadatas=metadatas)
        logging.info(f"✅ VectorDB construite avec {vector_db.index.ntotal} vecteurs")

        vector_db.save_local(VECTOR_DB_PATH)
        logging.info(f"💾 VectorDB sauvegardée dans : {VECTOR_DB_PATH}")
        return vector_db
    except Exception as e:
        logging.error(f"❌ Erreur création VectorDB : {e}")
        return None


# ------------ MAIN PIPELINE ------------
if __name__ == "__main__":
    configure_logging("C:/Users/info/OneDrive/Desktop/RAG_Chatbot_RCAR/app.log")

    logging.info("🚀 Démarrage pipeline VectorDB (CSV → TXT → Chunks → Embeddings)")

    # 1. Convertir CSV → TXT
    #convert_all_csv_to_txt()

    # 2. Chunking
    chunks = chunk_texts()

    # 3. Build or Load VectorDB
    db = build_or_load_vector_db(chunks)

    if db:
        logging.info("🎯 VectorDB prête à être utilisée.")
    else:
        logging.error("❌ Échec préparation VectorDB.")