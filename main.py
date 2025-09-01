import schedule
from scrapper import find_linkedin_jobs
from whatsapp_bot import send_group_message
import time
import random
from dotenv import load_dotenv
import os

WELCOME_PHRASES = [
    "ALOU ALOU MEU POVO",
    "AOOOOOOOOOOOOOOOOOOOOOOOOOOOBA A TODOS DESSE GRUPO",
    "BOM DIA, BOA TARDE E BOA NOITE A TODOS OS AMIGOS COMPANHEIROS AQUI PRESENTES",
    "SWAMY BOT CHEGANDO COM VAGUINHA FRESQUINHA NA REGIÃO DE SOROCITY"
]

load_dotenv()
GROUP_ID = os.getenv("WHATSAPP_JOBS_GROUP_ID")

def get_jobs_and_send():
    if not GROUP_ID:
        raise Exception("WHATSAPP_JOBS_GROUP_ID or WHATSAPP_API_TOKEN not found in .env")

    print("Buscando vagas")
    jobs = find_linkedin_jobs()
    print(f"Encontrei {len(jobs)} vagas")

    random_phrase = random.choice(WELCOME_PHRASES)
    send_group_message(GROUP_ID, random_phrase)
    for job in jobs:
        message = f"""
*{job['title']} | {job['company']}*
Localidade: {job['location']}


Link de candidatura: {job['link']}
        """
        
        
        send_group_message(GROUP_ID, message)

    print("Vagas enviadas")

schedule.every(23).hours.do(get_jobs_and_send)
while True:
    schedule.run_pending()
    time.sleep(1)
