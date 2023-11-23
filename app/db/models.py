from app.db.database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime


class Movies(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    gender = Column(String)
    image = Column(String)
