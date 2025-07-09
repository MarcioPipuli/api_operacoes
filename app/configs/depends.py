from typing import Generator, Optional

from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError

from sqlalchemy.orm import Session
from sqlalchemy.future import select

from pydantic import BaseModel

from .database import SessionLocal
from .auth import oauth2_schema
from .configs import settings
from ..models.models import UserModel


class TokenData(BaseModel):
    username: Optional[str] = None


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(db: Session = Depends(get_db),
                     token: str = Depends(oauth2_schema)) -> UserModel:
    credential_exception: HTTPException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Não foi possível autenticar a credencial',
        headers={"WWW-Authenticate": "Bearer"}
        ) 
    
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False}
        )
        
        username: str = payload.get("sub")
        if username is None:
            raise credential_exception
        
        token_data: TokenData = TokenData(username=username)
    except JWTError:
        raise credential_exception
    
    with db as session:
        query = select(UserModel).filter(UserModel.email == token_data.username)
        result = session.execute(query)
        user: UserModel = result.scalars().unique().one_or_none()
        
        if user is None:
            raise credential_exception
        
        return user