from os import getenv
from dotenv import load_dotenv
from pymongo import MongoClient

# chargement des variables d'environnements
load_dotenv()


environ = {
    "O3_HOST": getenv("O3_HOST"),
    "O3_PORT": getenv("O3_PORT", "80"),
    "O3_USER": getenv("O3_USER"),
    "O3_PASSWORD": getenv("O3_PASSWORD"),
    "MONGO_HOST": getenv("MONGO_HOST"),
    "MONGO_PORT": getenv("MONGO_PORT", "27017"),
    "BASE_PASSWORD_PATIENT": getenv("BASE_PASSWORD_PATIENT", "123456"),
    "MONGO_USER": getenv("MONGO_USER"),
    "MONGO_PASSWORD": getenv("MONGO_PASSWORD"),
}

def get_mongodb_client():
    host = environ["MONGO_HOST"]
    port = environ["MONGO_PORT"]
    user = environ["MONGO_USER"]
    password = environ["MONGO_PASSWORD"]

    auth_str = f"{user}:{password}@" if user and password else ""
    mongo_url = f"mongodb://{auth_str}{host}:{port}/"

    # connexion à mongoDB
    client = MongoClient(mongo_url)

    return client
