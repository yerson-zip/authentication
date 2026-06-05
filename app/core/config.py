import os
from dotenv import load_dotenv


load_dotenv()

url_database = os.getenv("DATABASE")
secret_key = os.getenv("SECRET_KEY")
time_jwt = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
algorithm = os.getenv("ALGORITHM")

