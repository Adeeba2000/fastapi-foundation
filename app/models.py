from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    age = Column(Integer)
    city = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)
    hashed_password = Column(String)