from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

API_URL = "https://backend-langchain.onrender.com/api/v1/prediction/779e1b80-a836-4914-98ee-c7791f7a2b52"
SECOND_API_URL = "https://v5.chatpro.com.br/instance_id/api/v1/send_message"

class Message(BaseModel):
    Type: str
    IsSync: bool
    Body: dict

@app.post("/webhook")
def webhook_handler(message: Message):
    # Verifica se o valor de Type é "received_message"
    if message.Type != "received_message":
        return {"message": "Invalid message type"}

    # Extrai o texto da mensagem recebida
    text = message.Body["Text"]

    # Envia o texto para a primeira API
    payload = {"question": text}
    response = requests.post(API_URL, json=payload)
    output = response.json()

    # Envia a resposta da primeira API para a segunda API
    payload = {
        "question": output["question"]
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }
    response = requests.post(SECOND_API_URL, headers=headers, json=payload)

    return response.json()