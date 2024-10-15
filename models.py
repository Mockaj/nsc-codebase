# models.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class File(Base):
    __tablename__ = 'files'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    filename: str = Column(String, nullable=False, unique=True)
    file_content: str = Column(String, nullable=False)

    def __repr__(self) -> str:
        return f"<File(id={self.id}, filename='{self.filename}')>"