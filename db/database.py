import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
load_dotenv()
engine = os.getenv('DATABASE_ENGINE')
user = os.getenv('USER')
password = os.getenv('PASSWORD')
host = os.getenv('HOST')
dbname = os.getenv('DBNAME')
ENGINE = create_engine(f'{engine}://{user}:{password}@{host}/{dbname}', echo=True)
Session = sessionmaker()
Base = declarative_base()
