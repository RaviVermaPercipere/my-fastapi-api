from dotenv import load_dotenv
import os

load_dotenv()

MY_AWS_ACCESS_KEY = os.getenv("MY_AWS_ACCESS_KEY")
MY_AWS_SECRET_KEY = os.getenv("MY_AWS_SECRET_KEY")
MY_AWS_REGION = os.getenv("MY_AWS_REGION")

BUCKET_NAME = os.getenv("BUCKET_NAME")
S3_FOLDER = os.getenv("S3_FOLDER")

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME")