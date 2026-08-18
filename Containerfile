# Imagem base compatível com ARMv7
FROM python:3.11-slim

# Diretório de trabalho
WORKDIR /app

# Variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instalar dependências do sistema necessárias para compilar libs criptográficas
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Criar diretório para estáticos
RUN mkdir -p /app/static

# Entrypoint: aplica migrações, coleta estáticos e inicia o servidor
ENTRYPOINT ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn --bind 0.0.0.0:8000 meuprojeto.wsgi:application"]
