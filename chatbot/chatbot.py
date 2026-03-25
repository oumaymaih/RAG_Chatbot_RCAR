import logging 
from chatbot.retriever import get_retriever, search

def ask_chatbot(query: str, llm, k: int = 5) -> str:
    """ Pipeline RAG :
    - Initialise le retriever
    - Recherche via search
    - Construit le contexte
    - Génère la réponse avec le LLM
    """
    logging.info(f"💬 Query reçue : {query}") 
    
    # Étape 1 : Initialiser le retriever
    retriever = get_retriever()
    if retriever is None:
        logging.error("❌ Retriever indisponible.")
        return "Erreur interne : la base de connaissances n'est pas disponible."

    # Étape 2 : Recherche des documents
    relevant_docs = search(query, retriever)
    if not relevant_docs:
        return "Je n'ai trouvé aucune information pertinente pour répondre à cette question."

    # Étape 3 : Construire le contexte
    context = "\n\n".join([doc.page_content for doc in relevant_docs])
    logging.info(f"📚 Contexte construit à partir de {len(relevant_docs)} documents.")

    # Étape 4 : Créer le prompt final 
    final_prompt = (f""" Tu es un assistant intelligent de la RCAR. 
                Réponds à la question ci-dessous en donnant une réponse claire, directe et facile à comprendre, 
                en 3 phrases maximum, sans salutation ni style e-mail.
                 Voici des informations extraites de la base de connaissances : 
                {context} Question : {query} """)

    # Étape 5 : Appel au LLM
    try:
        response = llm.invoke(final_prompt)
        answer = response.content.strip()
        logging.info("✅ Réponse générée avec succès.")
    except Exception as e:
        logging.exception("❌ Erreur lors de la génération de la réponse.")
        return f"Erreur lors de la génération de la réponse : {str(e)}"
    return answer


# --- Test en standalone --- 
if __name__ == "__main__": 
    from chatbot.config import get_llm 
    logging.basicConfig(level=logging.INFO) 
    llm = get_llm() 
    query_test = "C'est quoi la RCAR ?" 
    print(ask_chatbot(query_test, llm))