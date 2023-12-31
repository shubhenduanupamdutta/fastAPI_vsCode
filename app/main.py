"""
Fast API app for tutorial on freeCodeCamp
by Sanjeev Thyagarajan

"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from .database import engine
# from . import models
from .routers import post, user, auth, vote


# load database tables i.e. models
# models.Base.metadata.create_all(bind=engine)


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    """
    Root directory get method

    Returns:
        json: "message"
    """
    return {
        "message": "Welcome to my API",
        "New on 04th November 2023":
            "Deployed on AWS EC2 using CI/CD using GitHub Actions.",
        "URLs": {
            "Documentation_SwaggerUI": "https://fastapishubhendu.xyz/docs/",
            "Documentation_Redocly": "https://fastapishubhendu.xyz/redoc/"
        }
    }
