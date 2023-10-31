from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config.config import USER, PASSWORD, HOST, DB_NAME

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


# For reference:
# import psycopg2
# import time
# from psycopg2.extras import RealDictCursor
# from .config import config
# while True:
#     try:
#         conn = psycopg2.connect(host=config.HOST,
#                                 dbname=config.DB_NAME,
#                                 user=config.USER,
#                                 password=config.PASSWORD,
#                                 cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Connection to database was successful.")
#         break
#     except Exception as e:
#         print("Connection to database failed")
#         print(f"Error: {e}")
#         time.sleep(5)
