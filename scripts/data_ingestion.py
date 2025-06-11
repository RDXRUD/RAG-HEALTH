import os
import sys
import base64
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import fitz  # PyMuPDF
import pdfplumber
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.document_loaders import TextLoader, UnstructuredMarkdownLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from helpers.image_llm import descriptor, upload_to_imgbb

# Load environment variables
load_dotenv()

# === Settings ===
CHROMA_PATH = os.getenv("CHROMA_DB_DIR", "./vector_store")
DOCS_PATH = "./data/"
EMBED_MODEL = "all-MiniLM-L6-v2"

# === Embedding model ===
embedder = HuggingFaceEmbeddings(model_name=EMBED_MODEL, cache_folder="./models")

# === Extract text + images ===
def extract_text_images_from_pdf(path):
    docs = []
    pdf = fitz.open(path)
    image_output_dir = "data/extracted_images"
    os.makedirs(image_output_dir, exist_ok=True)

    for i, page in enumerate(pdf):
        # Extract text
        text = page.get_text().strip()
        if text:
            docs.append(Document(
                page_content=text,
                metadata={
                    "type": "Text",
                    "page_number": i + 1,
                    "source": path
                }
            ))

        # Extract and describe images
        images = page.get_images(full=True)
        for img_index, img in enumerate(images):
            xref = img[0]
            base_image = pdf.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image.get("ext", "png")
            image_b64 = base64.b64encode(image_bytes).decode("utf-8")

            local_filename = f"page_{i+1}_img_{img_index+1}.{image_ext}"
            local_path = os.path.join(image_output_dir, local_filename)

            # Save locally
            with open(local_path, "wb") as f:
                f.write(image_bytes)

            try:
                public_url = upload_to_imgbb(local_path)
                description = descriptor(public_url)
            except Exception as e:
                print(f"⚠️ Error processing image on page {i+1}: {e}")
                description = "Image description unavailable due to error."

            # Add image document with description
            docs.append(Document(
                page_content=description,
                metadata={
                    "type": "Image",
                    "page_number": i + 1,
                    "source": path,
                    "image_name": local_filename,
                    "image_ext": image_ext,
                    "image_base64": image_b64,
                    "imgbb_url": public_url
                }
            ))

    print(f"✅ Extracted {len(docs)} text+image elements from {path}")
    return docs

# === Extract tables ===
def extract_tables_from_pdf(path):
    docs = []
    with pdfplumber.open(path) as pdf:
        for i, page in enumerate(pdf.pages):
            tables = page.extract_tables()
            for table in tables:
                table_text = "\n".join([", ".join(cell if cell is not None else "" for cell in row) for row in table if row])
                if table_text.strip():
                    docs.append(Document(
                        page_content=table_text,
                        metadata={"type": "Table", "page_number": i + 1, "source": path}
                    ))
    print(f"✅ Extracted {len(docs)} table elements from {path}")
    return docs

# === Load all documents ===
def load_documents(directory):
    all_docs = []
    for file in os.listdir(directory):
        path = os.path.join(directory, file)
        if file.endswith(".pdf"):
            all_docs += extract_text_images_from_pdf(path)
            all_docs += extract_tables_from_pdf(path)
        elif file.endswith(".txt"):
            all_docs += TextLoader(path).load()
        elif file.endswith(".md"):
            all_docs += UnstructuredMarkdownLoader(path).load()
        else:
            continue
    print(f"📚 Loaded total {len(all_docs)} documents from {directory}")
    return all_docs

# === Chunking ===
def chunk_documents(docs):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.split_documents(docs)
    print(f"🔗 Split into {len(chunks)} chunks")
    return chunks

# === Store Embeddings ===
def store_embeddings(chunks):
    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embedder,
        persist_directory=CHROMA_PATH
    )
    print(f"✅ Stored {len(chunks)} chunks in ChromaDB at {CHROMA_PATH}")

# === Main Flow ===
if __name__ == "__main__":
    print("🚀 Starting ingestion pipeline (fitz + pdfplumber)...")
    docs = load_documents(DOCS_PATH)
    chunks = chunk_documents(docs)
    store_embeddings(chunks)
    
            