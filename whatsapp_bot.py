import os
import requests
from dotenv import load_dotenv

load_dotenv()
BASE_URL = os.getenv("WHATSAPP_BASE_URL")
API_TOKEN = os.getenv("WHATSAPP_API_TOKEN")

def send_group_message(group_id: str, message: str):
    if not BASE_URL or not API_TOKEN:
        raise Exception("WHATSAPP_BASE_URL or WHATSAPP_API_TOKEN not found in .env")
    response = requests.post(f"{BASE_URL}/messages/text",
        json={
            "to": group_id,
            "body": message
        },
        headers={
            "Authorization": f"Bearer {API_TOKEN}"
        }
    )

    if response.status_code != 200:
        raise Exception(f"Error sending message: {response.text}")

    print(response.text)

