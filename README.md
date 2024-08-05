# API Products

API Products est une application API REST développée avec FastAPI et SQLAlchemy pour gérer des produits. Elle permet de créer, lire, mettre à jour et supprimer des produits.

## Table des matières

- [Installation](#installation)
- [Utilisation](#utilisation)
- [Endpoints de l'API](#endpoints-de-lapi)
- [Tests](#tests)
- [Collection Postman](#collection-postman)
- [Docker](#utilisation-de-docker)

## Installation

### Prérequis

- Python 3.10 ou plus récent
- [pip](https://pip.pypa.io/en/stable/installation/)
- [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html) (optionnel mais recommandé)

### Étapes d'installation

1. Clonez le dépôt :

    ```sh
    git clone https://github.com/ChemaaOmar/API-Produit.git
    cd API-Produit
    ```

2. Créez et activez un environnement virtuel :

    ```sh
    python -m venv env
    source env/bin/activate  # Sur Windows utilisez `env\Scripts\activate`
    ```

3. Installez les dépendances :

    ```sh
    pip install -r requirements.txt
    ```

4. Lancez l'application :

    ```sh
    uvicorn app.main:app --reload
    ```

L'application sera disponible à l'adresse [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Utilisation

### Endpoints de l'API

#### Créer un produit

- **URL** : `/products/`
- **Méthode** : `POST`
- **Corps de la requête** :

    ```json
    {
        "name": "Test Product",
        "description": "Test Description",
        "price": 10.0,
        "stock": 100
    }
    ```

#### Lire un produit spécifique

- **URL** : `/products/{id}`
- **Méthode** : `GET`

#### Lire tous les produits

- **URL** : `/products/`
- **Méthode** : `GET`

#### Supprimer un produit

- **URL** : `/products/{id}`
- **Méthode** : `DELETE`

## Tests

### Exécuter les tests unitaires

Pour exécuter les tests unitaires, utilisez la commande suivante :

```sh
python -m unittest discover tests
```

## Collection Postman

Vous pouvez utiliser la collection Postman fournie pour tester l'API. Importez le fichier `API_Products.postman_collection.json` dans Postman.

### Example de fichier JSON pour la Collection Postman

```json 
{
  "info": {
    "name": "API Products",
    "_postman_id": "d1c1aab3-45d5-4a89-bf6e-95c35be4c4bb",
    "description": "Collection for testing API Products",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Create Product",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json",
            "type": "text"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n    \"name\": \"Test Product\",\n    \"description\": \"Test Description\",\n    \"price\": 10.0,\n    \"stock\": 100\n}"
        },
        "url": {
          "raw": "http://127.0.0.1:8000/products/",
          "protocol": "http",
          "host": [
            "127",
            "0",
            "0",
            "1"
          ],
          "port": "8000",
          "path": [
            "products"
          ]
        }
      },
      "response": []
    },
    {
      "name": "Get Product",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "http://127.0.0.1:8000/products/{PRODUCT_ID}",
          "protocol": "http",
          "host": [
            "127",
            "0",
            "0",
            "1"
          ],
          "port": "8000",
          "path": [
            "products",
            "1"
          ]
        }
      },
      "response": []
    },
    {
      "name": "Get Products",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "http://127.0.0.1:8000/products/",
          "protocol": "http",
          "host": [
            "127",
            "0",
            "0",
            "1"
          ],
          "port": "8000",
          "path": [
            "products"
          ]
        }
      },
      "response": []
    },
    {
      "name": "Delete Product",
      "request": {
        "method": "DELETE",
        "header": [],
        "url": {
          "raw": "http://127.0.0.1:8000/products/{PRODUCT_ID_TO_DELETE}",
          "protocol": "http",
          "host": [
            "127",
            "0",
            "0",
            "1"
          ],
          "port": "8000",
          "path": [
            "products",
            "1"
          ]
        }
      },
      "response": []
    }
  ]
}
```

## Utilisation de Docker

### Construire l'image Docker

Assurez-vous d'être à la racine du projet où se trouve le `Dockerfile` et exécutez les commandes suivantes :

# Build app
docker-compose build

# Run app
docker-compose up

# Stop app
docker-compose down

