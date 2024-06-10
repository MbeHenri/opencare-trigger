from datetime import datetime
import time
import urllib.parse

# import random
import itertools
from .utils import get_patients, insert_patients, insert_patients_odoo

from triggers.config import get_mongodb_client, get_odoo_client


def main():
    print(f"[Patient] [{datetime.now()}] init")
    # generate all base search text
    tableau = [
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
    ]
    combinaisons = ["".join(paire) for paire in itertools.permutations(tableau, 2)]

    # shuffle randomly the combinations
    # random.shuffle(combinaisons)
    # time to sleep
    waiting_time = 10

    # loop of the server

    # connection to mongo
    client = get_mongodb_client()

    # connection to odoo
    models, uid = get_odoo_client()

    while True:
        print(f"[Patient] [{datetime.now()}] start synchronisation")

        for recherche in combinaisons:
            # Encod search text
            encoded_term = urllib.parse.quote(recherche, safe="")

            # get patients
            patients = get_patients(encoded_term)

            # insert and update patients
            insert_patients(patients, client)

            # insert patients as customers
            insert_patients_odoo(patients, models, uid)

        # client.close()
        print(f"[Patient] [{datetime.now()}] end synchronisation")

        # waiting
        time.sleep(waiting_time)
