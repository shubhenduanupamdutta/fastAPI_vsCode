from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import config

# format of database URL
# "postgresql://<username>:<password>@<ip_address>/<db_name>"
SQLALCHEMY_DATABASE_URL = f"postgresql://{config.USER}\
    :{config.PASSWORD}@{config.HOST}/{config.DB_NAME}"

# Creating the engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# to talk to database we also have to create a session
local_session = sessionmaker(autoflush=False, autocommit=False, bind=engine)

# Declaring a base class
Base = declarative_base()
