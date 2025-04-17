import os
import logging
from typing import List, Tuple, Optional
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import gradio as gr

# --- Logging Configuration ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Environment Variables ---
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    logger.error("GEMINI_API_KEY not set.")
    raise RuntimeError("Please set GEMINI_API_KEY in your .env file.")

# --- Gemini Setup (via google.generativeai) ---
try:
    import google.generativeai as genai
except ImportError:
    raise ImportError(
        "Please install the Gemini SDK: pip install google-generativeai")

genai.configure(api_key=GEMINI_API_KEY)

# Load the Gemini model
model = genai.GenerativeModel("models/gemini-2.0-flash")

# --- FastAPI App ---
app = FastAPI(
    title="Gemini Chatbot API & Gradio UI",
    description="API endpoint and Gradio UI for the Gemini-powered chatbot.",
    version="1.0.0"
)

# --- Pydantic Models ---


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str

# --- Chat Logic ---


def get_gemini_reply(user_message: str, history: Optional[List[Tuple[str, str]]] = None) -> str:
    logger.info(f"User message: {user_message}")

    if not user_message:
        return "Please provide a message."

    try:
        # Optional: Add conversation history if needed in future
        response = model.generate_content(user_message)
        reply = response.text
        logger.info(f"Model reply: {reply}")
        return reply
    except Exception as e:
        logger.error(f"Gemini API error: {e}", exc_info=True)
        return "Sorry, an error occurred while contacting the AI model."

# --- API Endpoints ---


@app.get("/", include_in_schema=False)
async def root():
    return {"message": "Welcome to the Gemini Chatbot. Access the UI at /gradio or the API docs at /docs."}


@app.post("/chat", response_model=ChatResponse, tags=["API"])
async def chat_endpoint(request: ChatRequest):
    reply = get_gemini_reply(request.message)
    if reply.startswith(("Sorry", "Please provide")):
        raise HTTPException(status_code=400, detail=reply)
    return ChatResponse(reply=reply)


@app.get("/health", status_code=200, tags=["Health"])
async def health_check():
    return JSONResponse(content={"status": "ok"}, status_code=200)

# # --- Gradio UI ---
gradio_app = gr.ChatInterface(
    fn=get_gemini_reply,
    title="Gemini Chatbot",
    description="Chat with the Gemini 2.0 Flash model via Gemini API.",
    theme="soft",
    examples=[
        "What is the capital of France?",
        "Explain the concept of recursion.",
        "Write a short poem about clouds."
    ],
    cache_examples=False,
    type="messages",  # ✅ use messages format (role + content)
)

# Mount updated app
app = gr.mount_gradio_app(app, gradio_app, path="/gradio")

# --- Run with Uvicorn ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080,
                log_level="info", reload=True)
