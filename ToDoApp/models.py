from database import Base
from sqlalchemy import Column, Integer, String, Boolean, VARCHAR


class Todos(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(VARCHAR(255))
    description = Column(VARCHAR(255))
    priority = Column(Integer)
    complete = Column(Boolean, default=False)