from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey

from datetime import datetime

from configs.database import Base
from configs.configs import settings


class OperationModel(Base):
    __tablename__ = "operations"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    usuario = Column(String, ForeignKey('users.email'), nullable=False)
    tipo_operacao = Column(String, nullable=False)
    ticker = Column(String, nullable=False)
    quantidade = Column(Integer, nullable=False)
    preco = Column(Float, nullable=False)
    data_operacao = Column(DateTime, default=datetime.utcnow)
    executado = Column(Boolean, default=False)

class UserModel(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, index=True, nullable=False, unique=True)
    senha = Column(String, nullable=False)
    is_adm = Column(Boolean, default=False)
    