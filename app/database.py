from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import dotenv
dotenv.load_dotenv()

# configuring env variables
USER = os.environ["USER"]
PASSWORD = os.environ["PASSWORD"]
HOST = os.environ["HOST"]
DB_NAME = os.environ["DATABASE"]
# format of database URL
# "postgresql://<username>:<password>@<ip_address>/<db_name>"
SQLALCHEMY_DATABASE_URL = f"postgresql://{USER}:{PASSWORD}@{HOST}/{DB_NAME}"

# Creating the engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# to talk to database we also have to create a session
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

# Declaring a base class
Base = declarative_base()


# Create Dependency
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()