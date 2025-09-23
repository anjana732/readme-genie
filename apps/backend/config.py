from dotenv import load_dotenv
import os
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
SCHEMA = os.getenv("SCHEMA")
USER_TABLE = os.getenv("USER_TABLE")
OTP_TABLE = os.getenv("OTP_TABLE")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
RETRY_TIMES = 3
INVALID_LOG_ID = -99