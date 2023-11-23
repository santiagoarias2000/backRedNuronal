from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://databasehitdata:bichis162332@basehitdata.cwikakhedlsx.us-east-1.rds.amazonaws.com:5432/db_movies"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
print(engine)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
