import pytest
import subprocess
import time
import urllib.request

# URL base padrao onde a API ira rodar (local)
BASE_URL = "http://127.0.0.1:8000"

@pytest.fixture(scope="session", autouse=True)
def start_fastapi_server():
    """Sobe o servidor Uvicorn em background antes de rodar os testes."""
    print("\n[+] Iniciando servidor de testes na porta 8000...")
    
    proc = subprocess.Popen(["uvicorn", "api:app", "--port", "8000", "--host", "127.0.0.1"])
    
    # Ping ping via urllib para saber quando o uvicorn esta pronto
    server_ready = False
    for _ in range(15):
        try:
            res = urllib.request.urlopen(BASE_URL + "/docs")
            if res.getcode() == 200:
                server_ready = True
                break
        except Exception:
            time.sleep(0.5)
            
    if not server_ready:
        proc.terminate()
        pytest.fail("[-] O servidor de testes nao respondeu a tempo na porta 8000.")

    yield
    
    print("\n[+] Finalizando servidor de testes...")
    proc.terminate()
    proc.wait()


def test_generate_endpoint_success(playwright):
    """Playwright E2E: Testa se o endpoint devolve um Array de IMEIs legitimos (15 digitos)."""
    # Contexto 'invisivel' do Playwright apenas testando os contratos de API
    api = playwright.request.new_context(base_url=BASE_URL)
    
    # Monta a requisicao POST validando a estrutura de JSON do Pydantic enviando 5 elementos
    response = api.post("/generate", data={"prefix": "35390744", "quantity": 5})
    
    assert response.ok, f"A requisicao falhou: {response.text()}"
    assert response.status == 200
    
    payload = response.json()
    assert "imeis" in payload
    assert isinstance(payload["imeis"], list)
    assert len(payload["imeis"]) == 5
    # Validar se todo elemento da matriz tem 15 digitos
    for imei in payload["imeis"]:
        assert len(imei) == 15
        assert imei.isdigit()

def test_generate_endpoint_invalid_prefix(playwright):
    """Playwright E2E: Impede prefixos incorretos (diferente de 8 digitos numericos)."""
    api = playwright.request.new_context(base_url=BASE_URL)
    
    response = api.post("/generate", data={"prefix": "123", "quantity": 10})
    
    assert not response.ok
    assert response.status == 400
    assert response.json()["detail"] == "Prefix must be exactly 8 numeric digits."
    
def test_generate_endpoint_invalid_quantity(playwright):
    """Playwright E2E: Bloqueia a geração se a quantidade for igual ou inferior a 0."""
    api = playwright.request.new_context(base_url=BASE_URL)
    
    response = api.post("/generate", data={"prefix": "35390744", "quantity": -5})
    
    assert response.status == 400
    assert "Quantity must be a positive integer." in response.json()["detail"]

def test_generate_endpoint_rate_limit_abuse(playwright):
    """Playwright E2E: Verifica se abuso (ataque DoS volumetrico) e barrado com HTTP 429."""
    api = playwright.request.new_context(base_url=BASE_URL)
    
    status_codes = []
    # Tentativa agressiva de chamar o endpoint em loop rapido de 7 vezes (o teto e 5 por segundo)
    for _ in range(7):
        response = api.post("/generate", data={"prefix": "35390744", "quantity": 1})
        status_codes.append(response.status)
        
    # As primeiras chamadas (ate 5) devem passar, logo teremos 200 listados
    assert 200 in status_codes
    
    # A ultima ou penultima obrigatoriamente sera esmagada com Too Many Requests
    assert 429 in status_codes

