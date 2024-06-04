import unittest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
import os

DATABASE_URL = "postgresql://admin:admin@localhost:5432/testdatabase"

engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Configuration du client de test pour utiliser la base de données de test
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

class ProductAPITestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Créer les tables de la base de données de test
        Base.metadata.create_all(bind=engine)
        cls.client = TestClient(app)

    @classmethod
    def tearDownClass(cls):
        # Supprimer les tables de la base de données de test
        Base.metadata.drop_all(bind=engine)

    def test_create_product(self):
        response = self.client.post(
            "/products/",
            json={"name": "Test Product", "description": "Test Description", "price": 10.0, "stock": 100},
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["name"], "Test Product")
        self.assertEqual(data["description"], "Test Description")
        self.assertEqual(data["price"], 10.0)
        self.assertEqual(data["stock"], 100)
        self.assertIn("id", data)

    def test_read_product(self):
        # Créer un produit pour le test
        response = self.client.post(
            "/products/",
            json={"name": "Test Product 2", "description": "Test Description 2", "price": 20.0, "stock": 200},
        )
        product_id = response.json()["id"]

        response = self.client.get(f"/products/{product_id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["name"], "Test Product 2")
        self.assertEqual(data["description"], "Test Description 2")
        self.assertEqual(data["price"], 20.0)
        self.assertEqual(data["stock"], 200)
        self.assertEqual(data["id"], product_id)

    def test_read_products(self):
        response = self.client.get("/products/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)

    def test_delete_product(self):
        # Créer un produit pour le test
        response = self.client.post(
            "/products/",
            json={"name": "Test Product 3", "description": "Test Description 3", "price": 30.0, "stock": 300},
        )
        product_id = response.json()["id"]

        response = self.client.delete(f"/products/{product_id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["id"], product_id)

        # Vérifier que le produit a été supprimé
        response = self.client.get(f"/products/{product_id}")
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    unittest.main()
