# MBA USP Esalq - Observabilidade e Monitoramento

### Subindo o Ambiente do Elastic Stack ELK

1. **Crie um diretório para armazenar os dados do Elasticsearch:**

    ```bash
    mkdir elasticsearch_data
    ```

2. **Crie uma rede Docker chamada `observabilidade` para permitir a comunicação entre os containers:**

    ```bash
    docker network create observabilidade
    ```

3. **Inicie os containers definidos no arquivo `docker-compose.yml` na raiz do projeto, em modo desacoplado (`-d`) e reconstruindo as imagens se necessário (`--build`):**

    ```bash
    docker compose up -d --build
    ```

4. **Navegue para o diretório `app`, onde o arquivo `docker-compose.yml` da aplicação está localizado:**

    ```bash
    cd app
    ```

5. **Inicie os containers definidos no arquivo `docker-compose.yml` no diretório `app`, em modo desacoplado (`-d`) e reconstruindo as imagens se necessário (`--build`):**

    ```bash
    docker compose up -d --build
    ```

### Explicação Geral

- **`mkdir elasticsearch_data`**: Cria um diretório local para armazenar dados persistentes do Elasticsearch.
- **`docker network create observabilidade`**: Cria uma rede Docker personalizada chamada `observabilidade` para comunicação entre containers.
- **`docker compose up -d --build`**: Inicia os containers definidos no arquivo `docker-compose.yml` na raiz do projeto. O parâmetro `-d` executa os containers em segundo plano e `--build` força a reconstrução das imagens.
- **`cd app`**: Muda o diretório de trabalho para `app`, onde há um arquivo `docker-compose.yml` específico para a aplicação.
- **`docker compose up -d --build`**: Inicia os containers definidos no arquivo `docker-compose.yml` no diretório `app`, também em modo desacoplado e reconstruindo as imagens se necessário.

### Possíveis erros

1. Caso ocorra o seguinte erro na criação dos container: 

    ```bash
    bootstrap check failure [1] of [1]: max virtual memory areas vm.max_map_count [65530] is too low, increase to at least [262144]
    ```
    Execute o comando:
    ```bash
    sysctl -w vm.max_map_count=262144
    ```

2. Caso os logs do filebeat não estejam sendo coletados no nginx:

    Acesse o container do nginx executando:
    ```bash
    docker exec -it nginx bash
    ```
    Verifique se o filebeat está rodando:
    ```bash
    service filebeat status
    ```
    Caso ele não esteja rodando e apresentando uma mensagem de erro, execute o seguinte comando:
    ```bash
    service filebeat start
    ```