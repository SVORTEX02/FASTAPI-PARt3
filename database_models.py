from sqlalchemy import Column, Integer, String, ARRAY
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class DestinationDB(Base):
    __tablename__ = "destinations"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    comments = Column(ARRAY(String), nullable=False)  
