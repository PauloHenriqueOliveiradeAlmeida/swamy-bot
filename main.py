from db import Db
from scrapper import find_linkedin_jobs
from whatsapp_bot import send_group_message
import random
from dotenv import load_dotenv
import os
from flask import Flask, request

WELCOME_PHRASES = [
    "ALOU ALOU MEU POVO",
    "AOOOOOOOOOOOOOOOOOOOOOOOOOOOBA A TODOS DESSE GRUPO",
    "BOM DIA, BOA TARDE E BOA NOITE A TODOS OS AMIGOS COMPANHEIROS AQUI PRESENTES",
    "SWAMY BOT CHEGANDO COM VAGUINHA FRESQUINHA NA REGIÃO DE SOROCITY"
]

NOT_JOBS_PHRASES = [
    "Sem vaguinhas nessa noite :( (talvez seja domingo a noite?)",
    "HTTP STATUS: 404 - SEM VAGA POR HOJE PESSOAL",
    "Nessa noite os RH's nos abandonaram, assim como nosso(a) amado(a)",
    "Não tem vaga por hoje e nem gracinha de frase que tenta ser engraçada",
    "Não tiraram o escorpião do bolso pra contratar gente hoje, paciência galera"
]

load_dotenv()
GROUP_ID = os.getenv("WHATSAPP_JOBS_GROUP_ID")

def get_jobs_and_send():
    if not GROUP_ID:
        raise Exception("WHATSAPP_JOBS_GROUP_ID or WHATSAPP_API_TOKEN not found in .env")

    jobs = find_linkedin_jobs()
    print(f"Encontrei {len(jobs)} vagas")

    if (len(jobs) == 0):
        send_group_message(GROUP_ID, random.choice(NOT_JOBS_PHRASES))
        return

    db = Db()
    db_jobs = get_db_jobs(db, jobs)
    new_jobs = get_new_jobs(db_jobs, jobs)
    if len(new_jobs) == 0:
        send_group_message(GROUP_ID, random.choice(NOT_JOBS_PHRASES))
        return
    print(f"Encontrei {len(new_jobs)} novas vagas")
    db.set_many({job['link']: job['link'] for job in new_jobs})

    random_phrase = random.choice(WELCOME_PHRASES)
    send_group_message(GROUP_ID, random_phrase)
    for job in new_jobs:
        message = get_job_message(job)
        send_group_message(GROUP_ID, message)

    print("Vagas enviadas")

app = Flask(__name__)

def get_db_jobs(db: Db, jobs: list[dict[str, str]]) -> list[str]:
    return db.get_many([job['link'] for job in jobs])

def get_new_jobs(db_jobs: list[str], jobs: list[dict[str, str]]):
    return [job for job in jobs if job['link'] not in db_jobs]

def get_job_message(job: dict[str, str]) -> str:
     return f"""
*{job['title']} | {job['company']}*
Localidade: {job['location']}


Link de candidatura: {job['link']}
        """


@app.route('/send-jobs', methods=['HEAD'])
def send_jobs():
    authorization = request.headers.get('Authorization')
    if authorization != os.getenv("SECRET_KEY"):
        return '', 401
    get_jobs_and_send()
    return '', 204
