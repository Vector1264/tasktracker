from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy import DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    boards = relationship("Board", back_populates="owner",
                          cascade="all, delete-orphan")
    
class Board(Base):
    __tablename__="boards"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User", back_populates="boards")
    columns = relationship("Column", back_populates="board",
                           cascade="all, delete-orphan")
    
class Column(Base):
    __tablename__ = "columns"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    position = Column(Integer, default=0)
    board_id = Column(Integer, ForeignKey("boards.id"))

    boards = relationship("Board", back_populates="columns")
    cards = relationship("Card", back_populates="column",
                         cascade="all, delete-orphan")
    
class Card(Base):
    __tablename__ = "cards"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, default="")
    position = Column(Integer, default=0)
    column_id = Column(Integer, ForeignKey("column.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    column = relationship("Column", back_populates="cards")