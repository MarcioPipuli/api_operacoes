from typing import List
from typing import Optional
from typing import Any

from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import Response
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from models.models import UserModel
from models.entities import UserBase
from models.entities import UserCreate
from models.entities import UserUpdate

from configs.depends import get_db
from configs.depends import get_current_user
from configs.security import gerar_hash_senha
from configs.auth import autenticar
from configs.auth import criar_token_acesso


router = APIRouter()

@router.get('/users/current_user',
            summary='Dados do usuário logado',
            description='Retorna os dados do usuário logado, usando o token JWT para identificar.',
            response_model=UserBase)
def get_current_user(user: UserModel = Depends(get_current_user)):
    return user


@router.post('/users/signup', 
             status_code=status.HTTP_201_CREATED,
             summary='Cadastrar um usuário',
             description='Cadastrar um usuário no banco de dados',
             response_model=UserBase)
def post_user(user: UserCreate,
              db: Session = Depends(get_db)):
    new_user: UserModel = UserModel(email=user.email,
                                        senha=gerar_hash_senha(user.senha),
                                        is_adm=user.is_adm)
    with db as session:        
        try:                
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
            return new_user
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail='Usuário já cadastrado.')


@router.get('/users/all_users',
           summary='Consulta todos os usuários',
           description='Retorna todos os usuários que estão cadastrados.',
           response_model=List[UserBase])
def get_all_users(db: Session = Depends(get_db)):
    with db as session:
        query = select(UserModel)
        result = session.execute(query)
        users: List[UserBase] = result.scalars().unique().all()
        
        return users
    
@router.post('/users/login',
            summary='Autenticação e geração do token JWT',
            description='Autenticar o usuário e gerar um token JWT')
def login(form_data: OAuth2PasswordRequestForm = Depends(),
          db: Session = Depends(get_db)):
    user = autenticar(email=form_data.username,
                      senha=form_data.password,
                      db=db)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Dados de acesso incorretos.')
    
    return JSONResponse(content={"access_token": criar_token_acesso(sub=user.email),"token_type": "bearer"},
                        status_code=status.HTTP_200_OK)