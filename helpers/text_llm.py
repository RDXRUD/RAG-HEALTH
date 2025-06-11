import os
import requests
from dotenv import load_dotenv

# Load env variables
load_dotenv()

def load_parameters():
    HF_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
    GROQ_KEY=os.getenv("GROQ_API_KEY")
    MODEL_ID = "mistralai/Mistral-7B-Instruct-v0.3"
    API_URL = f"https://api-inference.huggingface.co/models/{MODEL_ID}"
    
    return HF_TOKEN,API_URL,GROQ_KEY



def query_llm(prompt: str):
    HF_TOKEN,API_URL,GROQ_KEY=load_parameters()
    # headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    # payload = {
    #     "inputs": prompt,
    #     "parameters": {
    #         "max_new_tokens": 512,
    #         "temperature": 0.7,
    #         "do_sample": True
    #     }
    # }
    # response = requests.post(API_URL, headers=headers, json=payload)
    # response.raise_for_status()
    # return response.json()[0]["generated_text"]
    
    headers = {
        "Authorization": f"Bearer {GROQ_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.3-70b-versatile",  # Groq's Mistral-based model
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 512
    }

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json=payload
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]
