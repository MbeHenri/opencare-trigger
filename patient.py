import requests
from os import getenv
from pymongo import MongoClient
import bcrypt
from dotenv import load_dotenv
from datetime import datetime

# chargement des variables d'environnements
load_dotenv()


environ = {
    "O3_HOST": getenv("O3_HOST", "localhost"),
    "O3_PORT": getenv("O3_PORT"),
    "O3_USER": getenv("O3_USER", "user"),
    "O3_PASSWORD": getenv("O3_PASSWORD", "example"),
    "MONGO_HOST": getenv("MONGO_HOST", "localhost"),
    "MONGO_PORT": getenv("MONGO_PORT", "27017"),
    "BASE_PASSWORD_PATIENT": getenv("BASE_PASSWORD_PATIENT", "123456"),
    "MONGO_USER": getenv("MONGO_USER"),
    "MONGO_PASSWORD": getenv("MONGO_PASSWORD"),
}


# Fonction pour récupérer les patients depuis OpenMRS
def get_patients(search: str):
    # initialisation
    host = environ["O3_HOST"]
    port = environ["O3_PORT"]
    if port:
        openmrs_url = f"http://{host}/openmrs"
    else:
        openmrs_url = f"http://{host}:{port}/openmrs"
    openmrs_username = environ["O3_USER"]
    openmrs_password = environ["O3_PASSWORD"]

    # Construction de l'URL
    # url = f'http://your-openmrs-url/ws/rest/v1/patient?q={encoded_term}'

    response = requests.get(
        f"{openmrs_url}/ws/rest/v1/patient?q={search}&v=custom:(uuid,patientIdentifier:(identifier),person:(display))",
        auth=(openmrs_username, openmrs_password),
    )
    response.raise_for_status()
    return response.json()["results"]


# insertion des patients dans la base de données du portail des patients
def insert_patients(patients, client: MongoClient):
    # initialisation
    db = client["opencare"]
    collection = db["patients"]

    # Hashage du mot de passe
    password = environ["BASE_PASSWORD_PATIENT"]
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    for patient in patients:
        patient["username"] = patient["patientIdentifier"]["identifier"]
        patient["password"] = hashed_password
        # Utilisation de l'identifiant du patient comme filtre
        filter_query = {"uuid": patient["uuid"]}
        # Utilisation de l'opérateur $set pour mettre à jour les autres champs du patient
        update_query = {"$set": patient}
        # Utilisation de 'upsert=True' pour insérer ou mettre à jour le document
        collection.update_one(filter_query, update_query, upsert=True)
        print(f" [{datetime.now()}] sync Identifier({patient['username']})")


def get_mongodb_client():
    host = environ["MONGO_HOST"]
    port = environ["MONGO_PORT"]
    user = environ["MONGO_USER"]
    password = environ["MONGO_PASSWORD"]
    
    auth_str = user and password if  f"{user}:{password}@" else ""
    mongo_url = f"mongodb://{auth_str}{host}:{port}/"

    # connexion à mongoDB
    client = MongoClient(mongo_url)

    return client
