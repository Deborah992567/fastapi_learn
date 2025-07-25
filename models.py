from sqlalchemy import ForeignKey , Column , Boolean , Integer , String
from database import Base



class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    author = Column(String)
    is_available = Column(Boolean, default=True)
    year_published = Column(Integer)