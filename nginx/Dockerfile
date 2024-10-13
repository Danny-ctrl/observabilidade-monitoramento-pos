# Usa a imagem base do Nginx mais recente disponível
FROM nginx:latest

# Remove logs antigos para evitar acumulação de dados desnecessários
RUN rm -f /var/log/nginx/access.log && rm -f /var/log/nginx/error.log

# Copia a configuração personalizada do Nginx para o diretório de configuração do container
COPY default.conf /etc/nginx/conf.d/default.conf

# Baixa e instala o Filebeat
RUN curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-7.17.0-amd64.deb && \
    dpkg -i filebeat-7.17.0-amd64.deb

# Copia a configuração personalizada do Filebeat para o diretório de configuração do container
COPY filebeat.yml /etc/filebeat/filebeat.yml

# Ajusta as permissões do arquivo de configuração do Filebeat para que apenas o proprietário possa modificar
RUN chmod go-w /etc/filebeat/filebeat.yml

# Copia o script de entrada para o container
COPY entrypoint.sh /entrypoint.sh

# Torna o script de entrada executável
RUN chmod +x entrypoint.sh

# Define o script de entrada como o comando a ser executado quando o container iniciar
ENTRYPOINT [ "/entrypoint.sh" ]
