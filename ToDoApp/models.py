from sqlalchemy import Column, Integer, Boolean, VARCHAR, ForeignKey

from .database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(VARCHAR(255), unique=True)
    username = Column(VARCHAR(255), unique=True)
    first_name = Column(VARCHAR(255))
    last_name = Column(VARCHAR(255))
    hashed_password = Column(VARCHAR(255))
    is_active = Column(Boolean, default=True)
    role = Column(VARCHAR(255))
    phone_number = Column(VARCHAR(255))

class Todos(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(VARCHAR(255))
    description = Column(VARCHAR(255))
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))