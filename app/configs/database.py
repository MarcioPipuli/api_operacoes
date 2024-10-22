from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .configs import settings

from datetime import datetime


# Criação do engine e da sessão
engine = create_engine(settings.DATABASE_URL, 
                       connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False,
                            autoflush=False,
                            bind=engine)

# Base para as tabelas
Base = declarative_base()

# Criação do banco e das tabelas
def init_db():
    Base.metadata.create_all(bind=engine)
