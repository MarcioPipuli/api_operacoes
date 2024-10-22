from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = '/api/v1'
    DATABASE_URL: str = "sqlite:///./operations.db"
    
    JWT_SECRET: str = 'RQda4Xq3d6-dW_WN0wkwY9wWZbJWGf_sb_2aiNNqJpM'
    """
    import secrets
    token: str = secrets.token_urlsafe(32)
    """
    ALGORITHM: str = 'HS256'
    # 60 minutos * 24 horas * 7 dias => 1 semana
    ACCESS_TOKEN_EXIRE_MINUTES: int = 60 * 24 * 7
    
    class Config:
        case_sensitive: bool = True


settings: Settings = Settings()