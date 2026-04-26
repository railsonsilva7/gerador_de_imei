# Gerador de IMEI (API)

Bem-vindo ao Gerador de IMEI! Este projeto expõe uma API RESTful (FastAPI) para produzir números baseados na algoritmia de validação matemática de Luhn.

## Requisitos e Instalação

Nossa estrutura utiliza as travas e validações sólidas do `pydantic` como contratos estritos.

### Via [UV](https://github.com/astral-sh/uv) (Recomendado)
Sendo um orquestrador extremamente veloz, o `uv` instalará tudo para você automaticamente lendo o nosso `pyproject.toml`.
```bash
uv sync
```

### Via Pip (Padrão)
Se preferir a via tradicional do ecossistema Python:
```bash
pip install fastapi uvicorn pydantic
```

## Como Executar a Aplicação

Para subir o servidor HTTP local na porta `8000` em formato "Hot Reload" (escutando por edições em tempo real do código):

```bash
uv run uvicorn api:app --reload
```
*(Se estiver utilizando pip, elimine o "uv run" do comando)*

## 📚 Documentação Viva (Swagger) e Testes

A grande mágica do FastAPI é ser "Auto-Documentado". Logo depois que inicializar a aplicação, você tem duas opções para testá-la de ponta a ponta sem criar dor de cabeça:

1. **Acessando a Interface Swagger UI (Browser)**
   Basta visitar: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   Ali terá painéis boníticos onde você insere os inputs (prefix, quantity) e executa o disparo, onde verá o JSON sendo formatado

2. **Via Linha de Comando (cURL)**
   Abras outro terminal e efetue esse curl POST com o esqueleto em JSON:
   ```bash
   curl -X POST "http://127.0.0.1:8000/generate" \
        -H "Content-Type: application/json" \
        -d '{"prefix":"35390744","quantity":10}'
   ```

A resposta devolverá a chave de matriz `imeis`, protegida por status HTTP de acordo com o padrão RFC padrão da Web.

## 🚀 Deploy no Render.com

Este repositório está configurado com **Infraestrutura como Código (IaC)** nativa para o Render.com.

1. **Faça o commit e envie (push)** o repositório todo para o seu GitHub, garantindo que o `render.yaml` e o `requirements.txt` subam juntos.
2. Crie ou logue em sua conta gratuita no [Render.com](https://render.com/).
3. No Dashboard do Render, clique no botão superior direito **"New +" -> "Blueprint"**.
4. Conecte sua conta do GitHub, autorize o acesso e selecione este repositório.
5. Magia Efetivada! ✨ O Render detectará automaticamente o arquivo `render.yaml`, fará o download e build rápido do Python 3.11, instalará o FastAPI com o Uvicorn e botará a sua API no ar com HTTPS em um endereço global - 100% gratuito.
