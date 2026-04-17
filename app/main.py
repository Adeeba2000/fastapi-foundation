from fastapi import FastAPI
from app.database import engine, Base
from app.routers import user
import app.models as models

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(user.router)
