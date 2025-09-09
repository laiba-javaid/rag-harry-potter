# ⚡ Magical Harry Potter RAG Assistant 🧙‍♂️

> *"Wit beyond measure is man's greatest treasure"* — Ravenclaw House  
> *"Words are, in my not-so-humble opinion, our most inexhaustible source of magic."* — Dumbledore  

The **Magical Harry Potter RAG Assistant** is an AI-powered Retrieval-Augmented Generation (RAG) system designed to answer questions about the magical world of Harry Potter.  
It combines modern **LLMs, embeddings, and vector search** to provide accurate, context-aware, and interactive responses straight from the Harry Potter universe.

---

## ✨ Features

- 🔮 **Ask the Magical Oracle**: Query the AI with any Harry Potter-related question.  
- 📚 **Knowledge Stats**:  
  - 7 Books processed  
  - 1000+ Knowledge Chunks  
  - AI-Powered retrieval  
- 🪄 **Magical Query Categories**:
  - Character Analysis  
  - Plot & Events  
  - Trivia & Details  
  - World Building  
- ⚡ **Advanced Magical Features**:
  - Context Retrieval: Finds relevant passages  
  - Smart Summarization: Condenses complex information  
  - Query Optimization: Improves retrieval strategy  
  - Response Enhancement: Adds magical formatting  

---

## 📸 Screenshots

### Home Interface  
![Home](./screenshots/home.png)

### Magical Response Area  
![Response](./screenshots/response.png)

### Query Categories & Features  
![Categories](./screenshots/categories.png)

---

## 🛠️ Tech Stack

- **Frontend**: Gradio (UI with magical Harry Potter-themed design)  
- **Backend**: Python, FastAPI/Django (customizable)  
- **Vector DB**: ChromaDB for storing embeddings  
- **Models**: Hugging Face Transformers + Groq API (for LLM inference)  
- **Deployment**: Localhost / Cloud (Vercel, Streamlit Cloud, or Docker)  

---

## 🚀 Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/laiba-javaid/rag-harry-potter.git
cd rag-harry-potter
```
### 2️⃣ Create Virtual Environment & Install Dependencies
```bash
python -m venv venv
source venv/bin/activate   # On Mac/Linux
venv\Scripts\activate      # On Windows

pip install -r requirements.txt
```
### 3️⃣ Run the Project
```bash
python run.py
```
- This will launch the app at http://127.0.0.1:7860.
---
## 🧪 Usage

- Type your Harry Potter-related question in the Ask the Magical Oracle box.

- Click Cast Question Spell to generate an AI-powered magical response.

- Explore random questions, or dive into Character Analysis, Plot & Events, Trivia, and World Building.

- Enjoy interactive responses enriched with magical formatting.
---

## 🔐 API Keys & Secrets

This project uses:

#### Hugging Face API Key

#### Groq API Key

- 👉 Store your keys in an .env file:
```bash
HUGGINGFACE_API_KEY=your_key_here
GROQ_API_KEY=your_key_here
```

Never commit secrets to GitHub. Use .gitignore to exclude .env.
---
## 🙌 Acknowledgments

⚡ Gradio
 for the UI framework

📚 ChromaDB
 for vector search

🤗 Hugging Face
 for models & embeddings

🪄 The magical world of J.K. Rowling's Harry Potter for inspiration
---
💛 Made with magic & AI by [Laiba Javaid] 🧙‍♀️⚡
