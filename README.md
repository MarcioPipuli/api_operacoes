# API de Operações de Ações 📈

## Descrição
Esta API é um exemplo desenvolvido para treinar o uso de **Python com FastAPI** e será utilizada para demonstrar conceitos de **testes de API utilizando Robot Framework**. A aplicação permite o registro, consulta e manipulação de operações de **compra e venda de ações** em um banco de dados, para consumo posterior por sistemas externos.


## Funcionalidades
- **Envio de operações** de compra e venda para o banco de dados.
- **Consulta e modificação** das operações registradas.
- **Cadastro de usuários** com roles para simulação do uso da aplicação.
- **Autenticação por token** para acesso seguro às rotas.
- **Execução das operações** simulando um sistemas externos simples.


## Tecnologias Utilizadas
- **Python** (Backend)
- **FastAPI** (Framework para criação da API)
- **SQLite** (Banco de dados local)


## Estrutura do Projeto
```bash
/app
│
├── app.py                 # Arquivo principal da aplicação
├── configs/               # Configurações de banco e variáveis do sistema
├── models/                # Definição dos modelos de dados
├── routes/                # Rotas da API
├── operations.db          # Banco de dados SQLite
└── __init__.py            # Inicializador do módulo
```


## Rotas Principais
1. **/users** - Cadastro de usuários e Geração de token de autenticação.
2. **/operations** - Manipulação das operações de compra e venda.
3. **/external_app** - Simulação de um sistemas externos simples para execução das operações.

## Configuração e Uso

### Pré-requisitos
- Python 3.x instalado.
- Instalar dependências:
    ```bash 
    pip install -r requirements.txt
    ```

### Executando a API
1. Inicialize o banco de dados e rode a aplicação
    ```bash 
    uvicorn app.app:app --reload
    ```

2. Acesse a documentação interativa:
    - [Swagger UI](http://127.0.0.1:8000/docs)
    - [ReDoc](http://127.0.0.1:8000/redoc)


### Banco de Dados
A aplicação utiliza SQLite como banco local. O arquivo ``operations.db`` contém as operações registradas e é inicializado automaticamente na primeira execução.