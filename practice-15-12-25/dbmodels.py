from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Book(Base):
    __tablename__ = "books" 

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    author = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    publish_year = Column(Integer, nullable=True)  
    category = Column(String(100), nullable=False)

    def __repr__(self):
        return f"<Book(id={self.id}, title={self.title}, author={self.author})>"
