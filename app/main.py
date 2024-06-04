from fastapi import FastAPI
from .database import engine, Base
from .routers import products

app = FastAPI()


Base.metadata.create_all(bind=engine)


app.include_router(products.router)
