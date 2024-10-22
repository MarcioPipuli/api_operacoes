from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Path

from sqlalchemy.orm import Session
from sqlalchemy.future import select

from models.entities import OperationResponse
from models.models import OperationModel

from configs.depends import get_db


router = APIRouter()

@router.get('/external_app/execute/{operation_id}',
             status_code=status.HTTP_200_OK,
             summary='Executar uma operação em aberto',
             description='Executar uma operação conforme o ID informado.',
             response_model=OperationResponse)
def get_execute_operation(operation_id: int = Path(..., description='ID da operação que será executada'),
                            db: Session = Depends(get_db)):
    with db as session:
        query = select(OperationModel).filter(OperationModel.id == operation_id)
        result = session.execute(query)
        operation: OperationModel = result.unique().scalar_one_or_none()
        
        if not operation:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f'Operação com ID:{operation_id} não encontrada')
        
        operation.executado = True
        
        session.add(operation)
        session.commit()
        session.refresh(operation)
        
        return operation
        


