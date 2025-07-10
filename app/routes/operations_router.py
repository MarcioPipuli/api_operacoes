from typing import List

from fastapi import APIRouter
from fastapi import status
from fastapi import Path
from fastapi import Depends
from fastapi import Response
from fastapi import HTTPException

from ..models.entities import OperationCreate
from ..models.entities import OperationResponse
from ..models.entities import OperationUpdate

from sqlalchemy.orm import Session
from sqlalchemy.future import select

from ..models.models import OperationModel
from ..models.models import UserModel

from ..configs.depends import get_db
from ..configs.depends import get_current_user


router = APIRouter()

@router.post('/operations/send',
             status_code=status.HTTP_201_CREATED,
             summary='Enviar operação',
             description='Enviar uma operação de compra/venda para o banco de dados.',
             response_model=OperationResponse)
def post_operations(operation:  OperationCreate,
                    user: UserModel = Depends(get_current_user),
                    db: Session = Depends(get_db)):
        new_operation: OperationModel = OperationModel(**operation.dict(), usuario=user.email)
        with db as session:
                session.add(new_operation)
                session.commit()
                session.refresh(new_operation)
                
                return new_operation


@router.get('/operations/me',
            summary='Consultar operações do usuário',
            description='Retorna todas as operações registradas por um usuário específico, usando o token JWT para identificar o usuário.',
            response_model=List[OperationResponse]
        )
def get_operations_me(db: Session = Depends(get_db),
                      user: UserModel = Depends(get_current_user)):
        with db as session:
                query = select(OperationModel).filter(OperationModel.usuario == user.email)
                result = session.execute(query)
                operations: List[OperationModel] = result.scalars().all()
            
                return operations
        

@router.get('/operations/unprocessed', 
            summary='Consulta operações não processadas',
            description='Retorna todas as operações que ainda não foram processadas pelo sistema, independentemente do usuário.',
            response_model=List[OperationResponse])
def get_operations_unprocessed(db: Session = Depends(get_db),
                               user: UserModel = Depends(get_current_user)):        
        with db as session:                
                query = select(OperationModel).filter(OperationModel.executado == False)
                result = session.execute(query)
                operations: List[OperationModel] = result.scalars().all()
                
                if user.is_adm == True:
                        return operations
                else:
                        raise HTTPException(
                                status_code=status.HTTP_403_FORBIDDEN,
                                detail='Você não tem permissão para realizar essa ação'
                                )
                

# @router.get('/operations/unprocessed/file', 
#         summary='(SE DER TEMPO E EU SOUBER FAZER!!!) Gerar arquivo de operações não processadas',
#         description='Gera um arquivo (ex: CSV ou JSON) com as operações que ainda não foram consumidas pelo outro sistema.'
#         )
# async def get_operations_unprocessed():
#     return {'details': 'ta funfando o GET UNPROCESSED de operações'}


@router.get('/operations/operation/{operation_id}', 
            status_code=status.HTTP_200_OK,
            summary='Consulta uma operação pelo ID',
            description='Retorna os dados da operação conforme o ID informado.',
            response_model=OperationResponse)
def get_operation_by_id(operation_id: int = Path(..., description='ID da operação que será consultada'),
                        user: UserModel = Depends(get_current_user),
                        db: Session = Depends(get_db)):
        with db as session:
                query = select(OperationModel).filter(OperationModel.id == operation_id)
                result = session.execute(query)
                operation: OperationModel = result.unique().scalar_one_or_none()
                
                if not operation:
                        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                            detail=f'Operação com ID:{operation_id} não encontrada')
                
                if operation.usuario == user.email or user.is_adm == True:
                        return operation
                else:
                        raise HTTPException(
                                status_code=status.HTTP_403_FORBIDDEN,
                                detail='Você não tem permissão para realizar essa ação'
                                )


@router.delete('/operations/operation/{operation_id}',
               status_code=status.HTTP_204_NO_CONTENT,
               summary='Excluir operação',
               description='Exclui uma operação específica')
def delete_operation(operation_id: int = Path(description='ID da operação que será excluída'),
                     user: UserModel = Depends(get_current_user),
                     db: Session = Depends(get_db)):
        with db as session:
                query = select(OperationModel).filter(OperationModel.id == operation_id)
                result = session.execute(query)
                operation_del: OperationModel = result.unique().scalar_one_or_none()
                
                if not operation_del:
                        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                            detail=f'Operação com ID:{operation_id} não encontrada')
                
                if operation_del.usuario == user.email or user.is_adm == True:
                        if operation_del.executado == False:
                                session.delete(operation_del)
                                session.commit()
                                
                                return Response(status_code=status.HTTP_204_NO_CONTENT)

                        else:
                                raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                                detail=f'Operação com ID:{operation_id} já foi consumida e não pode ser excluída')
                else:
                        raise HTTPException(
                                status_code=status.HTTP_403_FORBIDDEN,
                                detail='Você não tem permissão para realizar essa ação'
                                )


@router.patch('/operations/operation/{operation_id}',
              status_code=status.HTTP_202_ACCEPTED,
              summary='Atualizar operação',
              description='Atualiza os dados de uma operação específica',
              response_model=OperationResponse)
def patch_operation(operation_id: int = Path(..., description='ID da operação que será atualizada'),
                    update_operation:  OperationUpdate = ...,
                    user: UserModel = Depends(get_current_user),
                    db: Session = Depends(get_db)):
        with db as session:
                query = select(OperationModel).filter(OperationModel.id == operation_id)
                result = session.execute(query)
                operation_up: OperationModel = result.unique().scalar_one_or_none()
                
                if not operation_up:
                        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                            detail=f'Operação com ID:{operation_id} não encontrada')
                
                if operation_up.usuario == user.email or user.is_adm == True:
                        if operation_up.executado == False:
                                update_data = update_operation.dict(exclude_unset=True)
                                for key, value in update_data.items():
                                        setattr(operation_up, key, value)
                                
                                session.commit()
                                session.refresh(operation_up)
                                
                                return operation_up

                        else:
                                raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                                detail=f'Operação com ID:{operation_id} já foi consumida e não pode ser excluída')
                else:
                        raise HTTPException(
                                status_code=status.HTTP_403_FORBIDDEN,
                                detail='Você não tem permissão para realizar essa ação'
                                )