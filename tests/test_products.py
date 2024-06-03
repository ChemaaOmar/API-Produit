import unittest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app import models, crud, schemas

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

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
        cls.client = TestClient(app)

    def setUp(self):
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        self.test_product_id = self.add_test_product()

    def add_test_product(self):
        product = schemas.ProductCreate(name="Test Product", description="Test Description", price=10.0, stock=100)
        db = TestingSessionLocal()
        db_product = crud.create_product(db, product)
        db.commit()
        db.refresh(db_product)
        db.close()
        print(f"Added test product with ID: {db_product.id}")
        return db_product.id

    def test_create_product(self):
        response = self.client.post(
            "/products/",
            json={"name": "New Product", "description": "New Description", "price": 15.0, "stock": 50},
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["name"], "New Product")
        self.assertEqual(data["description"], "New Description")
        self.assertEqual(data["price"], 15.0)
        self.assertEqual(data["stock"], 50)
        self.assertIn("id", data)

    def test_read_product(self):
        response = self.client.get(f"/products/{self.test_product_id}")
        print(f"GET /products/{self.test_product_id} response: {response.json()} with status code: {response.status_code}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        print(f"Product data: {data}")
        self.assertEqual(data["name"], "Test Product")
        self.assertEqual(data["description"], "Test Description")
        self.assertEqual(data["price"], 10.0)
        self.assertEqual(data["stock"], 100)
        self.assertEqual(data["id"], self.test_product_id)

    def test_read_products(self):
        response = self.client.get("/products/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(len(data) > 0)

    def test_delete_product(self):
        response = self.client.delete(f"/products/{self.test_product_id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["id"], self.test_product_id)
        self.assertEqual(data["name"], "Test Product")
        self.assertEqual(data["description"], "Test Description")
        self.assertEqual(data["price"], 10.0)
        self.assertEqual(data["stock"], 100)

if __name__ == '__main__':
    unittest.main()
