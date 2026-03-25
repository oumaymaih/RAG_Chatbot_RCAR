import logging
import requests
from dotenv import dotenv_values
from langchain_mistralai import ChatMistralAI

def get_llm():
    """
    Charge le LLM Mistral avec gestion d'erreurs pour clé API manquante ou invalide.
    """
    try:
        env_values = dotenv_values("C:/Users/info/OneDrive/Desktop/RAG_Chatbot_RCAR/.env")
        mistral_api_key = env_values.get("MISTRAL_API_KEY", None)

        # Vérification de la présence de la clé API
        if not mistral_api_key:
            logging.error("❌ MISTRAL_API_KEY manquant dans app.env !")
            raise ValueError("MISTRAL_API_KEY manquant dans app.env !")

        # Initialisation du modèle
        llm = ChatMistralAI(
            mistral_api_key=mistral_api_key,
            model="mistral-small",
            temperature=0.5
        )

        # 🔹 Test rapide pour valider la clé
        try:
            llm.invoke("ping")  # prompt minimal pour déclencher une erreur si clé invalide
        except requests.exceptions.HTTPError as http_err:
            status_code = http_err.response.status_code if http_err.response else "N/A"
            if status_code == 401:
                logging.error(f"🚫 Clé API invalide ou expirée ! (Code {status_code})")
            else:
                logging.error(f"Erreur HTTP {status_code} lors de l'appel à Mistral : {http_err}")
            return None

        # Tout est bon
        logging.info("✅ LLM Mistral initialisé avec succès.")
        return llm

    except ValueError as e:
        logging.error(f"⚠️ Erreur de configuration : {e}")
        return None

    except Exception as e:
        logging.exception(f"⚠️ Erreur lors de l'initialisation du LLM : {e}")
        return None