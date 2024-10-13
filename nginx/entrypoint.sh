#!/bin/bash

# Executa o script de entrada padrão do Nginx, que configura e inicia o Nginx
/docker-entrypoint.sh

# Habilita o módulo de Filebeat para Nginx, permitindo a coleta de logs do Nginx
filebeat modules enable nginx

# Configura o Filebeat com base na configuração fornecida (filebeat.yml)
filebeat setup

# Executa o Filebeat em primeiro plano
service filebeat start

# Inicia o Nginx no primeiro plano (foreground), necessário para que o container continue em execução
nginx -g 'daemon off;'
