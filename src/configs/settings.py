#setup configs
from os import getenv as env
from os.path import join
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__name__).absolute().parent
DOT_ENV_FILE = join(BASE_DIR , ".env")

load_dotenv()

#Basic configs
SYSTEM_NAME = "Hair cut"
SYSTEM_VERSION = "0.0.1"
SYSTEM_DESCRIPTION = "A simple system for managing haircut appointments."

DEBUG = env("Debug")
SECRET_KEY = env("SECRET_KEY")
SESSION_EXPIRE_TIME = 600 #seconds

#Databases configs
DATABASE_ENGINE = env("DATABASE_ENGINE")
DATABASE_USER = env("DATABASE_USER")
DATABASE_PASSWORD = env("DATABASE_PASSWORD")
DATABASE_HOST = env("DATABASE_HOST")
DATABASE_PORT = env("DATABASE_PORT")
DATABASE_NAME = env("DATABASE_NAME")
DATABASE_URI = f"{DATABASE_ENGINE}://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

#Redis configs
REDIS_HOST = env("REDIS_HOST")
REDIS_PORT = env("REDIS_PORT")
REDIS_PASSWORD = env("REDIS_PASSWORD")

#Log config
LOG_FILE = join(BASE_DIR , "loggin.log")
LOG_FILE_MODE = "a"
LOG_FORMAT = "[%(levelname)s] %(module)s - %(asctime)s  : %(message)s "
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

#tests
TEST_DATABASE_NAME = "hair_cut_test"
TEST_DATABASE_URI = f"{DATABASE_ENGINE}://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{TEST_DATABASE_NAME}"
