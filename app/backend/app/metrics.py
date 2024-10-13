from elasticapm.metrics.base_metrics import (
    MetricSet,
)  # Importa o conjunto de métricas base do Elastic APM
from app.database import get_cursor  # Função para obter o cursor do banco de dados
from app.config import logger  # Logger para gerar logs da aplicação

# Classe que representa métricas de negócio relacionadas ao número de usuários online


class ContgemAlunosOnlineMetric(
    MetricSet
):  # Herda de MetricSet para criar um conjunto de métricas personalizado
    def before_collect(self):
        """
        Método que é chamado antes de coletar as métricas. Aqui, coletamos a métrica
        de contagem de usuários que estão online no sistema.
        """
        try:
            # Abre uma conexão com o banco de dados e obtém o cursor
            with get_cursor() as cursor:
                # Executa uma query para contar o número de usuários que estão online
                cursor.execute("SELECT COUNT(*) FROM tb_alunos WHERE online = TRUE")
                online_users = cursor.fetchone()[0]  # Obtém o resultado da contagem

                # Atualiza a métrica do Elastic APM com o número de usuários online
                self.gauge("online_users").val = online_users

        except Exception as e:
            # Em caso de erro, gera um log com a mensagem de erro
            logger.error(f"Error collecting user count metric: {e}")
