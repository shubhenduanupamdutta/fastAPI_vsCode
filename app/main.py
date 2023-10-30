"""
Fast API app for tutorial on freeCodeCamp
by Sanjeev Thyagarajan

"""

# import time
from fastapi import FastAPI
# from psycopg2.extras import RealDictCursor
from .database import engine
# from config import config  # load data from .env
from . import models
from .routers import post, user, auth


# load database tables i.e. models
models.Base.metadata.create_all(bind=engine)


app = FastAPI()
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

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


@app.get("/")
def root():
    """
    Root directory get method

    Returns:
        json: "message"
    """
    return {"message": "Welcome to my API"}
