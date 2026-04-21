from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

db_url = "postgresql://postgres:18922002@localhost:5432/demo_fastapi"

engine = create_engine(db_url)

session = sessionmaker(autoflush=False, autocommit=False, bind=engine)
