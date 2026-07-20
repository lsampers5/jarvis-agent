from fastapi import FastAPI
from pydantic import BaseModel
from agent import run_agent_turn

app = FastAPI()

# In-memory conversation storage (resets when server restarts)
conversations = {}

class ChatRequest(BaseModel):
    session_id: str
    message: str

@app.post("/chat")
def chat (request: ChatRequest):
    try:
        if request.session_id not in conversations:
            conversations[request.session_id] = [
                {"role": "system", "content": "You are Jarvis, a helpful personal assistant. Be concise and friendly."}
            ]

        messages = conversations[request.session_id]
        messages.append({"role": "user", "content": request.message})
        messages = run_agent_turn(messages)
        conversations[request.session_id] = messages

        return {"reply": messages[-1]["content"]}
    except Exception as e:
        print(f"\n[SERVER ERROR] {type(e).__name__}: {e}\n")
        return {"Reply": None}