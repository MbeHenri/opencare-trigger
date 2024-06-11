import requests
from pymongo import MongoClient
import bcrypt
from datetime import datetime
from triggers.config import environ


# Fonction pour récupérer les patients depuis OpenMRS
def get_patients(search: str):
    # initialisation
    host = environ["O3_HOST"]
    port = environ["O3_PORT"]
    if port:
        openmrs_url = f"http://{host}:{port}/openmrs"
    else:
        openmrs_url = f"http://{host}/openmrs"

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
        print(
            f"[Patient] [patient] [{datetime.now()}] sync Identifier({patient['username']})"
        )


def insert_patients_odoo(patients, models, uid):
    for patient in patients:
        name = "{}".format(patient["person"]["display"])
        code = "{}".format(patient["patientIdentifier"]["identifier"])
        email = "{}@opencare.com".format(patient["patientIdentifier"]["identifier"])

        # Search for the customer by email
        customer_id = models.execute_kw(
            environ["ODOO_DB"],
            uid,
            environ["ODOO_PASSWORD"],
            "res.partner",
            "search",
            [[["ref", "=", code]]],
        )

        if customer_id:
            print(
                f"[Patient] [odoo] [{datetime.now()}] sync Identifier({patient['username']}) exist"
            )
        else:
            customer_id = models.execute_kw(
                environ["ODOO_DB"],
                uid,
                environ["ODOO_PASSWORD"],
                "res.partner",
                "create",
                [
                    {
                        "name": name,
                        "email": email,
                        "ref": code,
                        "customer_rank": 1,
                    }
                ],
            )
            print(
                f"[Patient] [odoo] [{datetime.now()}] sync Identifier({patient['username']}) created"
            )
