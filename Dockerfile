# Usa versão oficial do Python 3.12 (Debian Slim)
FROM python:3.12-slim

# Variáveis de ambiente de otimização do Python
# Impede a gravação de arquivos .pyc no disco
ENV PYTHONDONTWRITEBYTECODE=1
# Força a saída padrão (stdout/stderr) a ser não-bufferizada
ENV PYTHONUNBUFFERED=1

# Define o diretório de trabalho interno do contêiner
WORKDIR /app

# Instalação de dependências do sistema necessárias para compilação e banco de dados
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Cópia estrita dos requisitos para aproveitar o cache de camadas (Layer Caching) do Docker
COPY requirements.txt /app/

# Atualiza o pip e instala dependências de forma não persistente na memória
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Cópia do restante do código-fonte
COPY . /app/