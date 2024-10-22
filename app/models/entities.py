from pydantic import BaseModel
from pydantic import validator
from pydantic import conint
from pydantic import confloat
from pydantic import EmailStr

from typing import Optional

from datetime import datetime

from models.enums import OperationType
from models.enums import Tickers


class OperationCreate(BaseModel):
    tipo_operacao: OperationType
    ticker: Tickers
    quantidade: conint(ge=1)
    preco: confloat(ge=0.01)
    
    class Config:
        from_attributes = True  # Permite criação a partir de objetos ORM


class OperationResponse(OperationCreate):
    id: int
    usuario: str 
    data_operacao: datetime
    executado: bool


class OperationUpdate(OperationCreate):
    tipo_operacao: Optional[OperationType] = None
    ticker: Optional[Tickers] = None
    quantidade: Optional[conint(ge=1)] = None
    preco: Optional[confloat(ge=0.01)] = None
    
    class Config:
        from_attributes = True 

    
class UserBase(BaseModel):
    email: EmailStr 
    is_adm: bool = False

    class Config:
        from_attributes = True
    
class UserCreate(UserBase):
    senha: str


class UserUpdate(UserBase):
    email: Optional[EmailStr] = None 
    senha: Optional[str] = None
    is_adm: Optional[bool] = None