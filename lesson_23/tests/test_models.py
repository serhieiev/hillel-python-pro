import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Book
from datetime import date

DATABASE_URL = "postgresql://username:password@localhost:5432/test_mydatabase"


@pytest.fixture
def session():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)

def test_create_and_read_book(session):
    # Create a book
    book = Book(name="Test Book", author="Test Author", date_of_release=date(2023, 8, 21), description="Test Description", genre="Test Genre")
    session.add(book)
    session.commit()

    # Read the book
    db_book = session.query(Book).filter_by(name="Test Book").first()
    assert db_book is not None
    assert db_book.name == "Test Book"
    assert db_book.author == "Test Author"
    assert db_book.date_of_release == date(2023, 8, 21)
    assert db_book.description == "Test Description"
    assert db_book.genre == "Test Genre"

if __name__ == "__main__":
    pytest.main()
