.PHONY: build up down logs restart clean audit-deps scan-secrets sast security-check test lint pre-commit-check

# Variável principal
PYTHON = uv run python

# --- Automações de Segurança ---

audit-deps:
	@echo "🔍 Inspecionando vulnerabilidades nas dependências..."
	uv run pip-audit

scan-secrets:
	@echo "🕵️ Buscando chaves e senhas vazadas no código via Docker..."
	docker run --rm -v $${PWD}:/code zricethezav/gitleaks:latest detect --source="/code" -v

sast:
	@echo "🛡️ Executando análise estática de segurança com Bandit..."
	uv run bandit -r . -c pyproject.toml

# Alvo principal de segurança que agrupa todos os testes
security-check: audit-deps scan-secrets sast
	@echo "✅ Todas as auditorias de segurança passaram perfeitamente, meu caro!"

test:
	@echo "🧪 Executando testes..."
	uv run pytest tests/

lint:
	@echo "🧹 Executando linting..."
	uv run ruff check .

# Regra completa para rodar antes de enviar o código (Push)
pre-commit-check: security-check test lint
	@echo "🚀 Código blindado, testado e formatado. Pronto para commit!"

# --- Docker ---

build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f

restart: down up

clean:
	docker compose down -v --rmi all --remove-orphans

# --- Cloudflare ---

cf-build:
	@echo "📦 Extraindo dependências (requirements.txt) via uv para a Cloudflare..."
	uv export --format requirements-txt --no-dev --no-hashes > requirements.txt

cf-dev: cf-build
	@echo "🔥 Iniciando ambiente de desenvolvimento Cloudflare local..."
	npx wrangler dev

cf-deploy: pre-commit-check cf-build
	@echo "🚀 Fazendo deploy seguro para a Cloudflare Workers..."
	npx wrangler deploy