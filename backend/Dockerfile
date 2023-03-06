FROM python:3.11-slim
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# poetryのインストール先の指定
ENV POETRY_HOME=/opt/poetry

# poetryインストール
RUN pip install poetry && \
    poetry config virtualenvs.create false

COPY pyproject.toml* poetry.lock* ./

RUN if [ -f pyproject.toml ]; then poetry install; fi

ENTRYPOINT ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--reload"]