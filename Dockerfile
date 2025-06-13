FROM python:3.12-slim-bookworm

WORKDIR /code

# Instala o git e remove os caches pra manter a imagem leve
RUN apt-get update && \
    apt-get install -y git && \
    rm -rf /var/lib/apt/lists/*

ENV TZ=America/Sao_Paulo

COPY . /code

RUN pip install uv && \
    uv sync --frozen

ENV PATH="/code/.venv/bin:$PATH"
ENTRYPOINT ["python3", "-m", "app.main"]