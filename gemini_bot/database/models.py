# models.py для телеграм бота
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Создаем базовый класс для моделей


Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True)
    id_user = Column(Integer, nullable=False, unique=True)
    payload = Column(String(128), nullable=False, unique=True)
    data_buy = Column(Date, nullable=False)
    data_end = Column(Date, nullable=False)


    def __repr__(self):
        return f'<User {self.user_name}>'
