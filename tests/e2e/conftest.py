import re

import pytest
from playwright.sync_api import Page


# ---------- CONFIGURAÇÕES DE AMBIENTE E SESSÃO ----------
# O pytest utiliza fixtures para gerenciar o setup e teardown dos testes de forma modular.
@pytest.fixture(scope="session")
def base_url() -> str:
    return "https://verzel-store.qa-test-verzel-store.workers.dev"


@pytest.fixture
def pagina_checkout(page: Page) -> Page:
    """Abre a loja, adiciona a Camiseta Essencial ao carrinho e chega no checkout."""
    page.goto("/")
    page.get_by_role("article", name="Camiseta Essencial").get_by_role("button").click()
    page.get_by_role("link", name=re.compile(r"Carrinho")).click()
    page.get_by_role("link", name="Finalizar compra").click()
    return page
