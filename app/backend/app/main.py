from fastapi import FastAPI  # Importa o framework FastAPI para criar a API
from fastapi.middleware.cors import (
    CORSMiddleware,
)  # Middleware CORS para controle de acesso
from elasticapm.contrib.starlette import (
    make_apm_client,
    ElasticAPM,
)  # Ferramentas do Elastic APM para monitoramento
from app.database import (
    create_tables,
    get_cursor,
)  # Funções de manipulação do banco de dados
from app.config import logger  # Logger para logs da aplicação
from pydantic import BaseModel, Field  # Ferramentas do Pydantic para validação de dados
from app.metrics import (
    ContgemAlunosOnlineMetric,
)  # Métrica personalizada para contagem de alunos online

# Inicializa a aplicação FastAPI
app = FastAPI()

# Cria o cliente APM para monitoramento e rastreamento de erros/performance
apm = make_apm_client(
    {
        "SERVICE_NAME": "backend",  # Nome do serviço monitorado no Elastic APM
        "DEBUG": True,  # Ativa modo de depuração para monitoramento detalhado
        "SERVER_URL": "http://apm:8200",  # URL do servidor APM que coleta os dados
        "ENVIRONMENT": "development",  # Define o ambiente da aplicação (ex: desenvolvimento, produção)
    }
)

# Adiciona o middleware do Elastic APM para capturar dados de performance e erros na aplicação
app.add_middleware(ElasticAPM, client=apm)

# Registra uma métrica personalizada (contagem de alunos online) no cliente APM
apm.metrics.register(ContgemAlunosOnlineMetric)

# Configura o middleware CORS para permitir requisições de qualquer origem (útil para desenvolvimento)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite requisições de qualquer origem
    allow_credentials=True,  # Permite o envio de cookies com as requisições
    allow_methods=["*"],  # Permite todos os métodos HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos os cabeçalhos HTTP
)

# Verifica se o cliente APM foi inicializado e gera um log de depuração
logger.debug("Elastic APM client initialized: %s", apm)


# Define a rota raiz ("/") que retorna uma mensagem de boas-vindas quando acessada
@app.get("/")
def root():
    return {"message": "Essa é uma resposta do container do back-end!!! 🎉🎉🎉"}


# Classe de validação de dados para a requisição de cadastro de aluno
class CadastrarAlunoInputDto(BaseModel):
    nome: str = Field(
        ...,
        min_length=1,
        description="Nome de aluno não pode estar vazio",  # Validação: nome não pode ser vazio
    )


# Rota para cadastrar um novo aluno no banco de dados
@app.post("/cadastrar_aluno")
def cadastrar_aluno(request: CadastrarAlunoInputDto):
    try:
        # Insere um novo aluno na tabela 'tb_alunos' com status 'online' como False
        with get_cursor() as cursor:
            cursor.execute(
                "INSERT INTO tb_alunos (nome, online) VALUES (%s, %s)",
                (request.nome, False),
            )
        return "Aluno cadastrado com sucesso"
    except Exception as e:
        raise Exception(
            f"Erro ao cadastrar aluno: {str(e)}"
        )  # Lança uma exceção em caso de erro


# Rota para simular um erro (divisão por zero)
@app.get("/receber_erro")
def receber_erro():
    try:
        numerator = 10
        denominator = 0  # Causa divisão por zero
        result = numerator / denominator  # Vai gerar uma exceção
        return result
    except Exception as e:
        raise Exception(e)  # Lança a exceção para ser capturada e logada


# Rota para listar todos os alunos cadastrados no banco de dados
@app.get("/listar_alunos")
def listar_alunos():
    try:
        with get_cursor() as cursor:
            cursor.execute("SELECT id, nome, online FROM tb_alunos ORDER BY id ASC")
            alunos = cursor.fetchall()  # Recupera todos os alunos
            # Converte os resultados em uma lista de dicionários
            alunos_dict = [
                {"id": aluno[0], "nome": aluno[1], "online": aluno[2]}
                for aluno in alunos
            ]
        return alunos_dict
    except Exception as e:
        raise Exception(
            f"Erro ao listar alunos: {str(e)}"
        )  # Lança uma exceção em caso de erro


# Rota para acessar o sistema e alterar o status 'online' de um aluno
@app.post("/acessar_sistema/{aluno_id}")
def acessar_sistema(aluno_id: int):
    try:
        with get_cursor() as cursor:
            # Busca o aluno pelo ID fornecido
            cursor.execute(
                "SELECT id, nome, online FROM tb_alunos WHERE id = %s", (aluno_id,)
            )
            aluno = cursor.fetchone()  # Obtém o aluno correspondente ao ID

            if not aluno:
                return {
                    "error": "Aluno não encontrado"
                }  # Retorna erro se o aluno não for encontrado

            # Inverte o status do campo 'online' (True -> False ou False -> True)
            novo_status = not aluno[2]

            # Atualiza o status 'online' no banco de dados
            cursor.execute(
                "UPDATE tb_alunos SET online = %s WHERE id = %s",
                (novo_status, aluno_id),
            )

            # Retorna os dados atualizados do aluno
            return {"id": aluno[0], "nome": aluno[1], "online": novo_status}

    except Exception as e:
        raise Exception(
            f"Erro ao acessar sistema: {str(e)}"
        )  # Lança exceção com mensagem de erro detalhada


# Cria as tabelas no banco de dados ao iniciar a aplicação
create_tables()
