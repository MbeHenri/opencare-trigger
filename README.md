# opencare-trigger

Service de synchronisation multi-thread pour le projet OpenCare (OMRS3). Il interroge OpenMRS 3 en continu et provisionne les données vers MongoDB, Odoo et Jitsi.

## Fonctionnement

Le service lance des threads indépendants qui tournent en boucle :

| Trigger     | Intervalle | Description                                                                                   |
| ----------- | ---------- | --------------------------------------------------------------------------------------------- |
| **patient** | 10s        | Recherche les patients OpenMRS, synchronise vers MongoDB et crée les clients Odoo             |
| **service** | 10s        | Récupère les services de rendez-vous OpenMRS, crée les produits dans Odoo                     |
| **room**    | 100s       | Construit les noms de room Jitsi (`OpenTMSRoom<Docteur><Patient>`) et les stocke dans MongoDB |

## Systèmes externes

| Système   | Protocole             | Rôle                                           |
| --------- | --------------------- | ---------------------------------------------- |
| OpenMRS 3 | REST API              | Source des données patients/providers/services |
| MongoDB   | pymongo               | Stockage local des patients et noms de rooms   |
| Odoo      | XML-RPC               | Gestion des clients et produits/services       |
| Jitsi     | Convention de nommage | Visioconférence (pas d'appel API)              |

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

Copier `example.env` vers `.env` et renseigner les variables :

| Variable                | Description                       | Défaut      |
| ----------------------- | --------------------------------- | ----------- |
| `O3_URL`                | URL OpenMRS 3                     | —           |
| `O3_USER`               | Utilisateur OpenMRS               | —           |
| `O3_PASSWORD`           | Mot de passe OpenMRS              | —           |
| `MONGO_URL`             | URL de connexion MongoDB          | —           |
| `BASE_PASSWORD_PATIENT` | Mot de passe de base des patients | `123456`    |
| `ODOO_URL`              | URL Odoo                          | —           |
| `ODOO_DB`               | Base de données Odoo              | —           |
| `ODOO_USER`             | Utilisateur Odoo                  | —           |
| `ODOO_API_KEY`          | Clé API / mot de passe Odoo       | —           |
| `ODOO_CODE_SERVICE`     | Code de base des services         | `OPENCARES` |
| `ODOO_PRICE_SERVICE`    | Prix de base d'un service         | `1500`      |

## Lancement

```bash
python server.py
```

## Docker

```bash
docker build -t opencare-trigger .
docker run --env-file ./example.env opencare-trigger
```
