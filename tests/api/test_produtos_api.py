from urllib.parse import quote

import pytest
from playwright.sync_api import APIRequestContext, APIResponse, Playwright

# Configuração dos endpoints da aplicação alvo
BASE_URL = "https://verzel-store.qa-test-verzel-store.workers.dev"
ENDPOINT = "/api/produtos"

# Lista de IDs conhecidos na base de dados da loja
IDS_PRODUTOS = ["P001", "P002", "P003", "P004", "P005", "P006", "P007", "P008"]


@pytest.fixture(scope="module")
def api(playwright: Playwright):
    """Contexto de API compartilhado pelos testes deste arquivo."""
    contexto = playwright.request.new_context(base_url=BASE_URL)
    yield contexto
    contexto.dispose()


def buscar_produto(api: APIRequestContext, produto_id: str) -> APIResponse:
    """Função auxiliar para efetuar o pedido GET, garantindo a codificação correta do ID."""
    return api.get(f"{ENDPOINT}/{quote(produto_id, safe='')}")


# ---------- Caminho feliz ----------

@pytest.mark.parametrize("produto_id", IDS_PRODUTOS)
def test_buscar_produto_existente_retorna_200(api: APIRequestContext, produto_id: str) -> None:
    response = buscar_produto(api, produto_id)

    assert response.status == 200, f"Esperado 200 para {produto_id}, veio {response.status}"
    assert response.json()["id"] == produto_id


# ---------- Caminho negativo ----------

@pytest.mark.parametrize(
    "produto_id",
    [
        pytest.param("P999", id="inexistente"),
        pytest.param("P000", id="zero"),
        pytest.param("abc", id="formato-invalido"),
        pytest.param("-1", id="negativo"),
        pytest.param("' OR '1'='1", id="sql-injection"),
        pytest.param("<script>alert(1)</script>", id="xss"),
    ],
)
def test_buscar_produto_inexistente_retorna_404(api: APIRequestContext, produto_id: str) -> None:
    response = buscar_produto(api, produto_id)

    assert response.status == 404, f"Esperado 404 para '{produto_id}', veio {response.status}"


@pytest.mark.parametrize("metodo", ["post", "put", "patch", "delete"])
def test_metodo_nao_permitido_nao_retorna_sucesso(api: APIRequestContext, metodo: str) -> None:
    response = getattr(api, metodo)(f"{ENDPOINT}/P001")

    assert response.status in (401, 403, 404, 405), (
        f"{metodo.upper()} não deveria funcionar, veio {response.status}"
    )
