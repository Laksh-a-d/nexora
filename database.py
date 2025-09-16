from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# In main.py or crud.py
from cloudinary_config import cloudinary


# ✅ Update with your real credentials
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:2107038@localhost:5432/mydatabase"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()




# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
