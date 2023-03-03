from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, Float

PG_DSN = 'postgresql+asyncpg://postgres:postgres@127.0.0.1:5431/stwars'

engine = create_async_engine(PG_DSN)
Session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base(bind=engine)

class People(Base):
    __tablename__ = 'people'

    id = Column(Integer, primary_key=True)
    birth_year = Column(String)
    ye_color = Column(String)
    films = Column(Text)
    gender = Column(String)
    hair_color = Column(String)
    height = Column(Integer)
    homeworld = Column(Text)
    mass = Column(Float)
    name = Column(String, unique=True, nullable=False)
    skin_color = Column(String)
    starships = Column(Text)
    vehicles = Column(Text)










