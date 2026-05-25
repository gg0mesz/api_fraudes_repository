from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.engine import URL

url = URL.create(
    drivername="mysql+pymysql",
    username="root",
    password="Lautaro@10",
    host="localhost",
    port=3306,
    database="bancodobrasil"
)

engine = create_engine(url)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()