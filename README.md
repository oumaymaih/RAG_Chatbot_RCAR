# RCAR Chatbot

Intelligent chatbot based on the **RAG (Retrieval-Augmented Generation)** approach to answer questions about the **Régime Collectif d’Allocation de Retraite (RCAR)**.  
This project was developed as part of an internship at **CDG (Caisse de Dépôt et de Gestion)**.
---

## Features

- Answer questions about RCAR: rules, centers, contacts, offers.
- Contextual search using **VectorDB (FAISS)**.
- Interactive user interface with **Streamlit**.
- Quick suggestions for frequent questions.
- Multi-language support: French, English, Arabic.

---

## Project Structure


RCAR-Chatbot/
│

├── README.md

├── SETUP.md 

├── requirements.txt

├── .gitignore

├── .env.example

├── ui_version.py

├── rag.ipynb

├── data/ 

├── assets/ 

└── chatbot/ 

- **SETUP.md** Instructions d'installation et exécution
- **data/**: CSV files 
- **assets/** Logos and images 
- **chatbot/**: Python scripts for LLM configuration, VectorDB creation, and chatbot queries. (BACKEND)
- **ui_version.py**: Streamlit interface.  
- **rag.ipynb**: Notebook for experiments and testing.  
- **assets/**: Images and logos used in the interface.  

---

## Data

All CSV files included contain only public information from RCAR/CDG (centers, contacts, offers, news).
No personal or sensitive information is included.

---

## Disclaimer

This project was developed as part of an internship at **CDG (Caisse de Dépôt et de Gestion)**.

It is based on publicly available data and is shared for educational and demonstration purposes only.

No confidential or proprietary information is included.
