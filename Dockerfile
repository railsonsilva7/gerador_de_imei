FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

WORKDIR /app

# Otimizações para o uv no Docker
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Define a porta padrão
ENV PORT=8080
EXPOSE 8080

# Baixa as dependências e faz cache das mesmas (passo 1)
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# Adiciona o resto do projeto (passo 2)
COPY . /app

# Sincroniza o projeto final
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Garante que o ambiente virtual será utilizado
ENV PATH="/app/.venv/bin:$PATH"

CMD ["python", "run.py"]
