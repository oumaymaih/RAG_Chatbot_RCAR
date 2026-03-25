# RAG_Chatbot_RCAR Setup Instructions

## 1. Clone the repository

```bash
git clone https://github.com/your-username/RAG-Chatbot-RCAR.git
cd RAG-Chatbot-RCAR

## 2. Create a virtual environment (optional but recommended)
```bash
python -m venv venv
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate     # Windows

## 3. Install dependencies
```bash
pip install -r requirements.txt

## 4. Create .env file
Copy .env.example to .env and fill in your API keys:

```bash
cp .env.example .env   # Linux / Mac
copy .env.example .env # Windows

## 5. Run the chatbot
```bash
streamlit run ui_version.py

Open your browser at the address shown (usually http://localhost:8501).

Ask your questions in the input field to get contextual answers.