
# 🧠 RAG-HEALTH: WHO-focused Retrieval-Augmented Generation System
project link: https://drive.google.com/file/d/1e15xKkPw1KtUhfN2a43LJ2b7T8nXV2RV/view?usp=drive_link

RAG-HEALTH is an end-to-end intelligent question-answering system designed for the healthcare domain. It leverages **Retrieval-Augmented Generation (RAG)** to retrieve information from trusted documents and generate accurate, explainable answers using state-of-the-art LLMs via the **Groq API**.

This system supports multimodal content (text, tables, and images) and is built to enable public access to healthcare knowledge using AI in a safe, transparent, and modular way.

---

## 🌐 Key Features

- 🔍 **Vector-based document retrieval** using ChromaDB and MiniLM embeddings
- 🤖 **LLM-powered answer generation** with Groq's LLaMA3 models
- 🖼️ **Image-to-text captioning** using ImgBB and Vision LLM
- 📊 **PDF extraction for tables, text, and images**
- ⚙️ **Microservice architecture** using FastAPI
- 🧩 **Workflow orchestration** using `n8n`

---

## 📁 Directory Structure

```
RAG-HEALTH/
│
├── data/                         # Source PDF files
├── helpers/                      # Core modules for embedding, retrieval, and LLM
│   ├── context_builder.py
│   ├── db_init.py
│   ├── image_llm.py
│   ├── prompt_builder.py
│   ├── text_llm.py
│
├── scripts/                      # Utility and automation scripts
│   ├── data_ingestion.py        # Extracts content and indexes it
│   ├── RAG_HEALTH.json          # n8n workflow config
│
├── services/                     # API layer (FastAPI microservices)
│   ├── retriever.py             # Context fetcher
│   ├── main.py                  # LLM responder
│
├── ui/                           # Streamlit frontend
│   ├── chat.py
│
├── vector_store/                # Persisted Chroma vector DB
├── .env                         # API keys and environment variables
├── requirements.txt
└── README.md
```

---

## 🧪 How It Works

1. **PDF Ingestion**:  
   - `scripts/data_ingestion.py` extracts **text**, **images**, and **tables**.
   - Images are uploaded to ImgBB and captioned using Groq's LLM Vision model.
   - All content is split into semantic chunks and stored in **Chroma** with metadata.

2. **Query Flow**:
   - User enters a healthcare query (e.g., *"What are sterilization guidelines before surgery?"*).
   - The `retriever` service searches Chroma for relevant document chunks.
   - The `main` service sends the prompt to **Groq LLaMA3** API and returns the answer.

3. **Multimodal Understanding**:
   - Tables and images from PDFs are treated as context via captions or markdown rendering.

4. **n8n Workflow**:
   - The entire query → retrieval → response flow is orchestrated using **n8n**.

---

## 🔁 n8n Workflow (Visual Overview)

```
Trigger Node (Webhook /query)
    ↓
HTTP Node → POST /retrieve
    ↓
HTTP Node → POST /ask
    ↓
Respond to Webhook
```

- Webhook Endpoint: `/query`
- Expected Body:
```json
{
  "query": "Explain laparoscopic sterilization steps."
}
```

- Intermediate Responses:
  - `/retrieve` → `{ context, question }`
  - `/ask` → `{ answer, sources, context }`

---

## 💻 Running Locally

### 1. Clone the Repository

```bash
git clone https://github.com/yourname/RAG-HEALTH
cd RAG-HEALTH
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Create a `.env` file with the following:

```env
GROQ_API_KEY=your_groq_key
IMGBB_API_KEY=your_imgbb_key
HUGGINGFACEHUB_API_TOKEN=your_huggingface_token
CHROMA_DB_DIR=./vector_store
```

### 4. Ingest Documents

```bash
python scripts/data_ingestion.py
```

### 5. Start Backend Services

```bash
# In one terminal
uvicorn services.retriever:app --port 8000

# In another terminal
uvicorn services.main:app --port 8001
```

### 6. Start n8n

- Import `scripts/RAG_HEALTH.json` into your n8n dashboard
- Start the workflow manually or via API trigger

### 7. (Optional) Launch Streamlit UI

```bash
streamlit run ui/chat.py
```

---

## 🤖 Technologies Used

| Layer         | Technology                         |
|---------------|------------------------------------|
| LLM           | Groq LLaMA3-70B via OpenAI API     |
| Embeddings    | HuggingFace `all-MiniLM-L6-v2`     |
| Vector Store  | Chroma DB                          |
| Backend       | FastAPI                            |
| Frontend      | Streamlit                          |
| Image Upload  | ImgBB                              |
| Orchestration | n8n                                |
| Parsing PDFs  | PyMuPDF (fitz), pdfplumber         |

---

## 🧠 Prompt Design

```txt
[Context]
- Chunked and cleaned healthcare-relevant paragraphs
- Captions from PDF images and tables

[Question]
12 Healthy habits?.

[Answer]
(Generated using Groq LLM)
```

---

## 🔮 Future Enhancements

- [x] Image + table support
- [x] Text-to-prompt automation
- [ ] Session-level memory
- [ ] Incremental PDF updates
- [ ] Integrated query analytics dashboard
- [ ] Slack / Discord bot interface
- [ ] Speech-to-text input with Whisper

---

## 🧑‍⚕️ Ideal Use Cases

- WHO guidelines
- Precautions during catastrophe


---

## 📃 License

This project is licensed under the **MIT License**.

---
