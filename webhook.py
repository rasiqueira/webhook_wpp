from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

API_URL = "https://backend-langchain.onrender.com/api/v1/prediction/c5fca50f-daea-4f07-bf9c-e5e07e91b509"
SECOND_API_URL = "https://v5.chatpro.com.br/chatpro-75d0d0c616/api/v1/send_message"

class Message(BaseModel):
    Type: str
    IsSync: bool
    Body: dict

@app.post("/webhook")
def webhook_handler(message: Message):
    # Verifica se o valor de Type é "received_message"
    print(message)
    print(message.Type)
    if message.Type != "receveid_message":
        return {"message": "Invalid message type"}
    else:
        print('executing action')
        # Extrai o texto da mensagem recebida
        text = message.Body["Text"]
        number = message.Body["Info"]["RemoteJid"].split('@')[0]
    
        # Envia o texto para a primeira API
        payload = {"question": text}
        print(payload)
        response = requests.post(API_URL, json=payload)
        print(response)
        output = response.json()
        print(output)
        if '55' in number:
            number = number.split('55')[1]
        # Envia a resposta da primeira API para a segunda API
        payload = {
            "number": number,
            "message": output
        }
        print(payload)
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
             "Authorization": "96281d9769d81f97886a4f6b994b7e1a"
        }
        response = requests.post(SECOND_API_URL, headers=headers, json=payload)
        print(response)
        print(response.text)

        return response.json()

