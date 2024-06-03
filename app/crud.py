import logging
from sqlalchemy.orm import Session
from . import models, schemas

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_products(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Product).offset(skip).limit(limit).all()

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    logger.info(f"Created product with ID: {db_product.id}")
    return db_product

def delete_product(db: Session, product_id: int):
    db_product = get_product(db, product_id)
    if db_product:
        db.delete(db_product)
        db.commit()
        logger.info(f"Deleted product with ID: {product_id}")
    else:
        logger.warning(f"Product with ID {product_id} not found")
