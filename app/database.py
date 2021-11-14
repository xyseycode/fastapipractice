from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_user = "postgres"
db_password = "pink5ive"
db_host = "localhost"
db_name = "fastapi"

SQLALCHEMY_DATABASE_URL = "postgresql://%s:%s@%s/%s".format(
    db_user, db_password, db_host, db_name
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
