import time
import urllib.parse
from dotenv import load_dotenv

# import random
import itertools

from patient import get_patients, insert_patients


# Générer toutes les combinaisons possibles de deux caractères
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

# Mélanger aléatoirement les combinaisons
# random.shuffle(combinaisons)

waiting_time = 10

# chargement des variables d'environnements
load_dotenv()

# Boucle d'écoute des changements
while True:
    patients = []
    for i in range(len(combinaisons)):
        # Terme de recherche
        recherche = combinaisons[i]

        # Encodage du terme de recherche
        encoded_term = urllib.parse.quote(recherche, safe="")

        patients.extend(get_patients(encoded_term))

    # insertion et actualisation des données dans la BD des patients
    insert_patients(patients)

    print("Synchronisation des patients terminée avec succès.")

    # Attendre un temps avant de relancer
    time.sleep(waiting_time)
