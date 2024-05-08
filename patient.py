import requests
from os import getenv
from pymongo import MongoClient
import bcrypt

environ = {
    "O3_HOST": getenv("O3_HOST", "localhost"),
    "O3_PORT": getenv("O3_PORT", "8080"),
    "O3_USER": getenv("O3_USER", "user"),
    "O3_PASSWORD": getenv("O3_PASSWORD", "example"),
    "MONGO_HOST": getenv("MONGO_HOST", "localhost"),
    "MONGO_PORT": getenv("MONGO_PORT", "27017"),
    "BASE_PASSWORD_PATIENT": getenv("BASE_PASSWORD_PATIENT", "123456"),
}

# Fonction pour récupérer les patients depuis OpenMRS
def get_patients(search: str):
    # initialisation
    host = environ["O3_HOST"]
    port = environ["O3_PORT"]
    if port == "":
        openmrs_url = f"http://{host}/openmrs"
    else:
        openmrs_url = f"http://{host}:{port}/openmrs"
    openmrs_username = environ["O3_USER"]
    openmrs_password = environ["O3_PASSWORD"]

    # Construction de l'URL
    # url = f'http://your-openmrs-url/ws/rest/v1/patient?q={encoded_term}'

    response = requests.get(
        f'{openmrs_url}/ws/rest/v1/patient?q={search}&v=full&limit=1"',
        auth=(openmrs_username, openmrs_password),
    )
    response.raise_for_status()
    return response.json()["results"]

# insertion des patients dans la base de données du portail des patients
def insert_patients(patients):

    # initialisation
    host = environ["MONGO_HOST"]
    port = environ["MONGO_PORT"]

    if port == "":
        mongo_url = f"mongodb://{host}/"
    else:
        mongo_url = f"mongodb://{host}:{port}/"

    password = environ["BASE_PASSWORD_PATIENT"]
    mongo_database = "opencare"
    mongo_collection = "patients"

    # connexion à mongoDB
    client = MongoClient(mongo_url)
    db = client[mongo_database]
    collection = db[mongo_collection]

    # Hashage du mot de passe
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    for patient in patients:
        patient["username"] = patient["identifiers"][0]["identifier"]
        patient["password"] = hashed_password
        # Utilisation de l'identifiant du patient comme filtre
        filter_query = {"uuid": patient["uuid"]}
        # Utilisation de l'opérateur $set pour mettre à jour les autres champs du patient
        update_query = {"$set": patient}
        # Utilisation de 'upsert=True' pour insérer ou mettre à jour le document
        collection.update_one(filter_query, update_query, upsert=True)

    client.close()
