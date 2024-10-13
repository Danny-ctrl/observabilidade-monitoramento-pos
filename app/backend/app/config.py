from pydantic import BaseSettings, Field
import logging

# Configura o logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


# Coleta das variáveis de ambiente
class Settings(BaseSettings):
    POSTGRES_USER: str = Field(..., env="POSTGRES_USER")
    POSTGRES_PASSWORD: str = Field(..., env="POSTGRES_PASSWORD")
    POSTGRES_DB: str = Field(..., env="POSTGRES_DB")
    POSTGRES_HOST: str = Field(..., env="POSTGRES_HOST")


# Carrega as configurações do aplicativo
settings = Settings()
