"""
Generates environment variable in development mode.
"""

import os
from dotenv import load_dotenv


load_dotenv()

HOST = os.environ['HOST']
DB_NAME = os.environ['DATABASE']
USER = os.environ['USER']
PASSWORD = os.environ['PASSWORD']
