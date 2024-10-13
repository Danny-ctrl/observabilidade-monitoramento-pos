# base da imagem Docker a ser utilizada
FROM node:18-alpine

# adicionar a camada que será o diretório padrão a ser utilizado
WORKDIR /src

# copiar o arquivo de instalação dos pacotes necessários para diretório padrão do container
COPY package.json ./

# realizar a instalação dos pacotes necessários
RUN npm install

# copiar todos os arquivos da máquina para o diretório do container
COPY . .
