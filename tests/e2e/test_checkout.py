import re

import pytest
from playwright.sync_api import Page, expect

# ---------- MASSA DE DADOS REUTILIZÁVEL ----------
# Centralizar dados válidos evita repetição e facilita a manutenção do teste.
NOME_VALIDO = "Bianca Lira"
EMAIL_VALIDO = "bianca@teste.com"
CEP_VALIDO = "12345678"

# ---------- FUNÇÕES AUXILIARES (HELPERS) ----------
# Isolei ações repetitivas de interação com a interface para manter os testes limpos.
def preencher_checkout(page: Page, nome: str = "", email: str = "", cep: str = "") -> None:
    """Preenche o formulário de checkout. Campos não informados ficam vazios."""
    page.get_by_role("textbox", name="Nome completo").fill(nome)
    page.get_by_role("textbox", name="E-mail").fill(email)
    page.get_by_role("textbox", name="CEP").fill(cep)


def confirmar_pedido(page: Page) -> None:
    page.get_by_role("button", name="Confirmar pedido").click()


# ---------- SUÍTE DE TESTES: CAMINHO FELIZ ----------

def test_finalizar_compra(pagina_checkout: Page) -> None:
    preencher_checkout(pagina_checkout, NOME_VALIDO, EMAIL_VALIDO, CEP_VALIDO)
    confirmar_pedido(pagina_checkout)

    expect(pagina_checkout.get_by_text("Pedido confirmado")).to_be_visible()
    expect(pagina_checkout.get_by_role("heading", name=re.compile(r"Pedido VZ-"))
    ).to_be_visible()


# ---------- SUÍTE DE TESTES: VALIDAÇÕES E CENÁRIOS NEGATIVOS ----------

def test_campos_obrigatorios_vazios(pagina_checkout: Page) -> None:

    # Act: Tenta enviar o formulário sem preencher nenhum campo
    confirmar_pedido(pagina_checkout)

    # Assert: Verifica se todas as mensagens de campos obrigatórios aparecem na tela
    expect(pagina_checkout.get_by_text("Informe o nome completo.")).to_be_visible()
    expect(pagina_checkout.get_by_text("Informe o e-mail.")).to_be_visible()
    expect(pagina_checkout.get_by_text("Informe o CEP.")).to_be_visible()

# ---------- SUÍTE DE TESTES: VALIDAÇÕES PARAMETRIZADAS ----------
# O uso do @pytest.mark.parametrize evita duplicação de código, executando 
# múltiplos cenários negativos utilizando a mesma estrutura de teste.
@pytest.mark.parametrize(
    "nome, email, cep, mensagem_esperada",
    [
        pytest.param(
            "Bianca", EMAIL_VALIDO, CEP_VALIDO,
            "Informe nome e sobrenome.", id="sobrenome-vazio",
        ),
        pytest.param(
            "Maria Guia", "teste@teste", "00000000",
            "Informe um e-mail válido.", id="email-invalido",
        ),
        pytest.param(
            "Maria Guia", "teste@teste.com", "0000000",
            "Informe um CEP com 8 dígitos.", id="cep-incompleto",
        ),
    ],
)
def test_validacoes_do_formulario(
    pagina_checkout: Page, nome: str, email: str, cep: str, mensagem_esperada: str
) -> None:
    
    # Act: Preenche com dados inválidos específicos e submete
    preencher_checkout(pagina_checkout, nome, email, cep)
    confirmar_pedido(pagina_checkout)

    # Assert: Valida se a mensagem de erro esperada para cada caso é exibida corretamente
    expect(pagina_checkout.get_by_text(mensagem_esperada)).to_be_visible()
