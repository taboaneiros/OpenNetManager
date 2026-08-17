# Usa a imagem oficial Python 3.13
FROM docker.io/python:3.13-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Instala dependências de sistema necessárias para psycopg2 (PostgreSQL)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copia os arquivos de dependências e as instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código do projeto
COPY . .

# Coleta os arquivos estáticos (necessário para produção)
RUN python manage.py collectstatic --noinput

# Cria um usuário não-root para maior segurança
RUN useradd --create-home appuser
USER appuser

# Expõe a porta padrão do Django
EXPOSE 8000

# Define um entrypoint para garantir migrações antes de iniciar
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Adiciona um HEALTHCHECK para monitorar a saúde do container
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD ["curl", "-f", "http://localhost:8000"]

ENTRYPOINT ["/entrypoint.sh"]
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
