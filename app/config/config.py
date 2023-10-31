"""
Generates environment variable in development mode.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    host: str
    db_port: str
    database: str
    user: str
    password: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"


settings = Settings()  # type: ignore

user = settings.user
password = settings.password
db_name = settings.database
host = settings.host
db_port = settings.db_port
secret_key = settings.secret_key
algorithm = settings.algorithm
access_token_expire_minutes = settings.access_token_expire_minutes

# HOST = os.environ['HOST']
# DB_NAME = os.environ['DATABASE']
# USER = os.environ['USER']
# PASSWORD = os.environ['PASSWORD']
# SECRET_KEY = os.environ['SECRET_KEY']
# ALGORITHM = os.environ['ALGORITHM']
# ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ['ACCESS_TOKEN_EXPIRE_MINUTES'])
