from os import getenv

from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker

DB_USER = getenv("DB_USER")
DB_PASSWORD = getenv("DB_PASSWORD")
DB_HOST = getenv("DB_HOST")
DB_NAME = getenv("DB_NAME")

url = URL.create("mysql+pymysql", DB_USER, DB_PASSWORD, DB_HOST, database=DB_NAME)
engine = create_engine(url, pool_size=10, max_overflow=20)
session_maker = sessionmaker(autocommit=False, autoflush=False, bind=engine)
