# import requests
from datetime import datetime
from triggers.config import environ


# Fonction pour récupérer les services depuis OpenMRS
def get_services():
    # initialisation
    """host = environ["O3_HOST"]
    port = environ["O3_PORT"]
    if port:
        openmrs_url = f"http://{host}:{port}/openmrs"
    else:
        openmrs_url = f"http://{host}/openmrs"

    openmrs_username = environ["O3_USER"]
    openmrs_password = environ["O3_PASSWORD"]

    response = requests.get(
        f"{openmrs_url}/ws/rest/v1/patient?q={search}&v=custom:(uuid,patientIdentifier:(identifier),person:(display))",
        auth=(openmrs_username, openmrs_password),
    )
    response.raise_for_status()"""
    return [
        {"name": "Pédiatrie", "uuid": "7ba3aa21-cc56-47ca-bb4d-a60549f666c0"},
        {"name": "Ophtalmologie", "uuid": "8a46c3db-bbb2-4eaf-b87e-1e7385317513"},
        {"name": "Dentiste", "uuid": "136b3011-ccf2-416f-8c3d-5b878e2624bb"},
        {"name": "Chirurgie", "uuid": "3e00d85d-a118-414d-a7fe-5e8d6f164482"},
        {"name": "Généraliste", "uuid": "475a8d54-02ef-4925-857a-2423f0e926d8"},
    ]


def insert_services_odoo(services, models, uid):
    for service in services:
        product_name = service["name"]
        product_barcode = "{}#{}".format(environ["ODOO_CODE_SERVICE"], service["uuid"])

        product_id = models.execute_kw(
            environ["ODOO_DB"],
            uid,
            environ["ODOO_PASSWORD"],
            "product.template",
            "search",
            [[["barcode", "=", product_barcode]]],
        )

        if product_id:
            print(
                f"[Service] [odoo] [{datetime.now()}] sync Identifier({service['name']}) exist"
            )
        else:
            product_id = models.execute_kw(
                environ["ODOO_DB"],
                uid,
                environ["ODOO_PASSWORD"],
                "product.template",
                "create",
                [
                    {
                        "name": product_name,
                        "barcode": product_barcode,
                        "type": "service",  # 'product', 'consu', 'service'
                        "list_price": float(
                            environ["ODOO_PRICE_SERVICE"]
                        ),  # Selling price
                    }
                ],
            )
            print(
                f"[Service] [odoo] [{datetime.now()}] sync Identifier({service['name']}) created"
            )
