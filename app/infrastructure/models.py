from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    url = Column(String, unique=True, index=True)
    total_pages = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

    pages = relationship("BookPage", back_populates="book", cascade="all, delete-orphan")

class BookPage(Base):
    __tablename__ = "book_pages"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    page_number = Column(Integer)
    image_url = Column(Text)
    image_path = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    book = relationship("Book", back_populates="pages")

class ProcessMarkdown(Base):
    __tablename__ = "process_markdown"

    id = Column(Integer, primary_key=True, index=True)
    image_name = Column(String, index=True, unique=True)
    result_markdown = Column(Text)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
