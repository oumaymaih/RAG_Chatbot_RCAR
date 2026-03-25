# création du retriever + recherche 
# chatbot/retriever.py

import logging
from chatbot.vectorDB import build_or_load_vector_db
from chatbot.logging_config import configure_logging

# Configurer logging
configure_logging(
    log_file="C:/Users/info/OneDrive/Desktop/RAG_Chatbot_RCAR/app.log",
    log_to_console=False
)

def get_retriever(k=5):
    """
    Crée et retourne un retriever LangChain à partir de la VectorDB.
    """
    vector_db = build_or_load_vector_db()

    if vector_db is None:
        logging.error("❌ Impossible de créer le retriever : VectorDB introuvable.")
        return None

    retriever = vector_db.as_retriever(search_kwargs={"k": k}, similarity_metric="cosine")
    logging.info(f"✅ Retriever créé avec succès (k={k})")
    return retriever


def search(query, retriever):
    """
    Effectue une recherche et affiche les chunks trouvés.
    """
    if retriever is None:
        logging.error("❌ Recherche impossible : retriever non initialisé.")
        return []

    try:
        # Résultats : liste de Document (même si texte brut à la base, LangChain les ré-emballe en Document)
        results = retriever.invoke(query)  # 🔑 nouvelle API LangChain 0.2+ = de meme que get_relevent_documents  
        logging.info(f"\n📄 Nombre de résultats trouvés : {len(results)}")

        for i, doc in enumerate(results, 1):
            # doc.page_content contient ton texte brut
            # doc.metadata contient le chemin/source
            logging.info(f"\n--- Résultat {i} ---")
            logging.info(f"Source : {doc.metadata.get('source', 'Inconnue')}")
            logging.info(f"Contenu : {doc.page_content[:200]}...")  # aperçu

        logging.info(f"🔍 Recherche effectuée pour : '{query}' ({len(results)} résultats)")
        return results

    except Exception as e:
        logging.error(f"❌ Erreur lors de la recherche : {e}")
        return []


# Test en standalone
if __name__ == "__main__":
    r = get_retriever(k=5)
    search("le délai de traitement du dossier au mois juillet", r)