# config.py
import os
from dotenv import load_dotenv

# Charger les variables depuis le fichier .env
load_dotenv()

# URL de connexion RabbitMQ
RABBITMQ_URL = os.getenv("RABBITMQ_URL")

if not RABBITMQ_URL:
    raise ValueError("La variable RABBITMQ_URL n'est pas définie dans le fichier .env")
