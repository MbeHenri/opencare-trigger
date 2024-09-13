from datetime import datetime
import time
import urllib.parse
from triggers.config import get_mongodb_client

from triggers.doctor.utils import get_doctors
from triggers.patient import combinaisons
from triggers.patient.utils import get_patients
from triggers.room.utils import create_room, insert_user_to_talk, add_user_room


def main():
    print(f"[Room] [{datetime.now()}] init")
    waiting_time = 100

    # loop of the server

    # connection to mongo
    client = get_mongodb_client()
    db = client["opencare"]
    collection = db["rooms"]

    while True:
        print(f"[Room] [{datetime.now()}] start synchronisation")

        # get doctors
        doctors = get_doctors()

        for recherche in combinaisons:
            # Encod search text
            encoded_term = urllib.parse.quote(recherche, safe="")

            # get patients
            patients = get_patients(encoded_term)

            for doctor in doctors:
                for patient in patients:
                    # creation du patient et du docteur dans talk
                    insert_user_to_talk(
                        doctor["identifier"], doctor["person"]["display"]
                    )
                    insert_user_to_talk(
                        patient["patientIdentifier"]["identifier"],
                        patient["person"]["display"],
                    )
                    # on verifie s'il n'existe pas de reunion enregistré dans mongo
                    exist = collection.find_one(
                        {
                            "uuidDoctor": doctor["uuid"],
                            "uuidPatient": patient["uuid"],
                        }
                    )
                    # si non on la crée dans talk et on la renseigne dans mongo
                    if exist is None:
                        token = create_room(
                            f"Consultation ({doctor['person']['display']} / {patient['person']['display']})"
                        )

                        if token is not None:
                            add_user_room(
                                token, patient["patientIdentifier"]["identifier"]
                            )
                            add_user_room(token, doctor["identifier"])
                            collection.insert_one(
                                {
                                    "uuidPatient": patient["uuid"],
                                    "uuidDoctor": doctor["uuid"],
                                    "tokenRoom": token,
                                }
                            )
                    else:
                        print(
                            f"[Room] [talk] [{datetime.now()}] create {exist['tokenRoom']} error"
                        )

        # client.close()
        print(f"[Room] [{datetime.now()}] end synchronisation")

        # waiting
        time.sleep(waiting_time)
