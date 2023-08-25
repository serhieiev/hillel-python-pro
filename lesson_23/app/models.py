from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DATABASE_URL = "postgresql://username:password@localhost:5432/mydatabase"

engine = create_engine(DATABASE_URL)

Session = sessionmaker(bind=engine)

Base = declarative_base()


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    author = Column(String)
    date_of_release = Column(Date)
    description = Column(String)
    genre = Column(String)

    def __repr__(self):
        return f"<Book(id={self.id}, name={self.name}, author={self.author}, date_of_release={self.date_of_release}, description={self.description}, genre={self.genre})>"
