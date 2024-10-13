import psycopg2  # biblioteca para conectar e executar queries no PostgreSQL
from contextlib import (
    contextmanager,
)  # utilizado para gerenciar o contexto do cursor e da conexão
from app.config import (
    settings,
)  # importa as configurações da aplicação (provavelmente usando Pydantic ou algo semelhante)

# Configuração da string de conexão com o banco de dados PostgreSQL
STRING_CONEXAO = f"dbname='{settings.POSTGRES_DB}' user='{settings.POSTGRES_USER}' host='{settings.POSTGRES_HOST}' password='{settings.POSTGRES_PASSWORD}'"


# Gerenciamento de contexto para conexão e cursor do banco de dados
@contextmanager
def get_cursor():
    # Cria uma nova conexão com o banco de dados utilizando a string de conexão
    conn = psycopg2.connect(STRING_CONEXAO)
    try:
        # Cria um cursor para executar comandos SQL
        cursor = conn.cursor()
        yield cursor  # Retorna o cursor para ser utilizado no contexto da função
        conn.commit()  # Comita as mudanças no banco de dados após a execução bem-sucedida
    except Exception as e:
        conn.rollback()  # Em caso de erro, faz o rollback das operações
        raise e  # Relança a exceção para tratamento posterior
    finally:
        # Fecha o cursor e a conexão após o uso, garantindo que os recursos sejam liberados
        if cursor:
            cursor.close()
        conn.close()


# Função para criar as tabelas necessárias no banco de dados
def create_tables():
    # Query SQL para criar a tabela 'tb_alunos' caso ela não exista
    create_table_query = """
    CREATE TABLE IF NOT EXISTS tb_alunos (
        id SERIAL PRIMARY KEY,
        nome VARCHAR(100) NOT NULL,
        online BOOLEAN NOT NULL
    );
    """
    # Utiliza o contexto 'get_cursor' para obter um cursor e executar a query
    with get_cursor() as cursor:
        cursor.execute(create_table_query)  # Executa o comando SQL para criar a tabela
