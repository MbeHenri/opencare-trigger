from os import getenv
from dotenv import load_dotenv
from pymongo import MongoClient
import xmlrpc.client

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
    "ODOO_HOST": getenv("ODOO_HOST"),
    "ODOO_PORT": getenv("ODOO_PORT"),
    "ODOO_USER": getenv("ODOO_USER"),
    "ODOO_DB": getenv("ODOO_DB"),
    "ODOO_PASSWORD": getenv("ODOO_API_KEY"),
    "ODOO_CODE_SERVICE": getenv("ODOO_CODE_SERVICE", "OPENCARES"),
    "ODOO_PRICE_SERVICE": getenv("ODOO_PRICE_SERVICE", 1500),
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


def get_odoo_client():
    # Odoo API endpoint URLs
    host = environ["ODOO_HOST"]
    port = environ["ODOO_PORT"]
    if port:
        ODOO_URL = f"http://{host}:{port}"
    else:
        ODOO_URL = f"http://{host}"

    ODOO_DB = environ["ODOO_DB"]
    ODOO_USERNAME = environ["ODOO_USER"]
    ODOO_PASSWORD = environ["ODOO_PASSWORD"]

    # Connect to Odoo API
    common = xmlrpc.client.ServerProxy("{}/xmlrpc/2/common".format(ODOO_URL))
    uid = common.authenticate(ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD, {})
    models = xmlrpc.client.ServerProxy("{}/xmlrpc/2/object".format(ODOO_URL))

    return models, uid
