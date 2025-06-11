import os
import requests
from dotenv import load_dotenv

load_dotenv()

def load_parameters():
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    IMGBB_API_KEY = os.getenv("IMGBB_API_KEY")  # You must set this
    GROQ_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"
    MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"

    if not GROQ_API_KEY or not IMGBB_API_KEY:
        raise ValueError("Missing GROQ_API_KEY or IMGBB_API_KEY in .env")
    
    return GROQ_API_KEY, IMGBB_API_KEY, GROQ_ENDPOINT, MODEL

def upload_to_imgbb(image_path: str) -> str:
    _, IMGBB_API_KEY, _, _ = load_parameters()

    with open(image_path, "rb") as file:
        image_data = file.read()

    response = requests.post(
        "https://api.imgbb.com/1/upload",
        params={"key": IMGBB_API_KEY},
        files={"image": image_data}
    )

    if response.status_code == 200:
        return response.json()['data']['url']
    else:
        raise RuntimeError(f"❌ ImgBB upload failed: {response.text}")

def descriptor(image_url: str, prompt: str = "What's in this image?") -> str:
    GROQ_API_KEY, _, GROQ_ENDPOINT, MODEL = load_parameters()

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }

    payload = {
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url
                        }
                    }
                ]
            }
        ],
        "model": MODEL,
        "temperature": 1,
        "max_completion_tokens": 1024,
        "top_p": 1,
        "stream": False,
        "stop": None
    }

    response = requests.post(GROQ_ENDPOINT, json=payload, headers=headers)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        raise RuntimeError(f"❌ GROQ API error: {response.status_code} - {response.text}")

# 🚀 Example usage
if __name__ == "__main__":
    local_image_path = "./images/sample.jpg"  # Replace with your path
    try:
        print("📤 Uploading image...")
        image_url = upload_to_imgbb(local_image_path)
        print(f"🌐 Uploaded to: {image_url}")

        print("🤖 Generating description...")
        description = descriptor(image_url)
        print(f"\n📝 Description:\n{description}")
    except Exception as e:
        print(e)