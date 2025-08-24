# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_cohere import ChatCohere
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from dotenv import load_dotenv
import os

# Load env
load_dotenv()

app = FastAPI()

# Request & Response Models
class ChatRequest(BaseModel):
    prompt: str
    session_id: str

class ChatResponse(BaseModel):
    answer: str

# Cohere LLM
llm = ChatCohere(
    cohere_api_key=os.getenv("COHERE_API_KEY"),
    model="command-r-plus"
)

# Chat history in memory
chat_histories = {}

@app.post("/chat", response_model=ChatResponse)
async def chat_with_cohere(request: ChatRequest):
    # Get history for session
    history = chat_histories.get(request.session_id, [])

    # Add system message only once per session
    if not history:
        history.append(SystemMessage(content="You are Ezz, a helpful chatbot. Always introduce yourself as Ezz when starting a conversation."))

    # Add user input
    history.append(HumanMessage(content=request.prompt))

    # Call Cohere
    response = llm.invoke(history)

    # Extract bot answer
    answer = response.content

    # Save reply to history
    history.append(AIMessage(content=answer))
    chat_histories[request.session_id] = history

    return ChatResponse(answer=answer)
