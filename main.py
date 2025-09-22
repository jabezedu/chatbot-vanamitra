from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from google.genai import Client
import os

app = FastAPI()

# Allow frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the client with API key from environment
client = Client(api_key=os.getenv("GEMINI_API_KEY"))

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data.get("message", "")

    # Generate a response using chats.create
    response = client.chats.create(
        model="gemini-2.0-flash",
        messages=[{"author": "user", "content": [{"type": "text", "text": user_message}]}]
    )

    # Extract the reply text
    reply_text = response.output[0].content[0].text

    return {"reply": reply_text}
