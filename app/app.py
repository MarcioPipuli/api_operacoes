from fastapi import FastAPI
from .routes import operations_router
from .routes import user_router
from .routes import external_app_router

from .configs.database import SessionLocal
from .configs.database import init_db
from .configs.configs import settings

# Inicializa o banco de dados
init_db()

app = FastAPI(title='API Operações',
              description="API para envio de operações de compra/venda das ações para um banco de dados que serão consumidas por um sistema terceiro que irá executa-las.",
              version="6.6.6",)
app.include_router(operations_router.router, tags=['Operations'], prefix=settings.API_V1_STR)
app.include_router(user_router.router, tags=['Users'], prefix=settings.API_V1_STR)
app.include_router(external_app_router.router, tags=['Externar Service'], prefix=settings.API_V1_STR)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run("app:app",
                host="127.0.0.1",
                port=8000,
                reload=True)