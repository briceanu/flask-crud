from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()


PG_HOST = os.getenv("PG_HOST")
# when you want to make a migration change PG_HOST=postgres to PG_HOST=localhost
PG_PORT = os.getenv("PG_PORT")
PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")
PG_DB = os.getenv("PG_DB")
SQLALCHEMY_ECHO = os.getenv("SQLALCHEMY_ECHO")


DB_URL = f"postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"


# Create engine
engine = create_engine(DB_URL, echo=True, future=True)

# Create session factory
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
# Base class for models
Base = declarative_base()
