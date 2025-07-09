from pytz import timezone

from typing import Optional
from typing import List

from datetime import timedelta
from datetime import datetime

from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session
from sqlalchemy.future import select

from jose import jwt

from ..models.models import UserModel
from .configs import settings
from .security import verificar_senha

from pydantic import EmailStr

oauth2_schema = OAuth2PasswordBearer(
    tokenUrl=f'{settings.API_V1_STR}/users/login'
)

def autenticar(email: EmailStr,
               senha: str,
               db: Session) -> Optional[UserModel]:
    with db as session:
        query = select(UserModel).filter(UserModel.email == email)
        result = session.execute(query)
        user: UserModel = result.scalars().unique().one_or_none()
        
        if not user:
            return None
        
        if not verificar_senha(senha, user.senha):
            return None

        return user

def _criar_token(tipo_token: str,
                 tempo_vida: timedelta,
                 sub: str) -> str:
    # documentação do payload do JWT -> https://datatracker.ietf.org/doc/html/rfc7519#section-4.1
    payload = {}
    sp = timezone('America/Sao_Paulo')
    expira = datetime.now(tz=sp) + tempo_vida
    
    payload["type"] = tipo_token
    payload["exp"] = expira
    payload["iat"] = datetime.now(tz=sp)
    payload["sub"] = str(sub)
    
    return jwt.encode(payload, 
                      settings.JWT_SECRET, 
                      algorithm=settings.ALGORITHM)

def criar_token_acesso(sub: str) -> str:
    return _criar_token(tipo_token='acess_token',
                        tempo_vida=timedelta(minutes=settings.ACCESS_TOKEN_EXIRE_MINUTES),
                        sub=sub)