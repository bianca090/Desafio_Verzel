# 🐛 [BUG] API permite criação de pedidos com e-mails sintaticamente inválidos

## 📌 Informações Gerais

* **ID do Bug:** `BUG-VZS-142-04`
* **Card Relacionado:** `VZS-142` (Validação de Regras de Negócio e Integridade de Pedidos)
* **Critério de Aceite Afetado:** N/A (Regra Geral de Validação de Dados / Sanitização de API)
* **Tipo de Teste:** Teste Funcional de API / Candidato a Regressão
* **Severidade:** Alta (Permite persistência de dados de contato inválidos)
* **Prioridade:** Média (Afeta a integridade dos dados cadastrais e pode impactar comunicações futuras)
* **Ambiente:** QA / API (`POST /api/pedidos`)
* **Relatora:** Bianca Gomes de Lira
* **Data:** 08/10/2026

---

## 🎯 Resumo / Descrição

A API `POST /api/pedidos` não realiza validação sintática adequada do campo `cliente.email` antes de criar o pedido.

Ao enviar formatos de e-mail inválidos, como endereços contendo **pontos consecutivos no domínio** (`usuario@dominio..com`) ou **ponto após o TLD** (`usuario@dominio.com.`), a API aceita a requisição e retorna `201 Created`, permitindo a criação do pedido com um endereço de e-mail inválido.

Esse comportamento permite que dados inconsistentes sejam persistidos na aplicação sem que o cliente seja informado sobre o erro de preenchimento.

---

## 🔄 Passos para Reprodução

1. Abra uma ferramenta de testes de API, como Postman ou Insomnia.
2. Configure uma requisição `POST` para o endpoint `/api/pedidos`.
3. Defina o header:

   * `Content-Type: application/json`

4. Envie o seguinte payload:

```json
{
  "cliente": {
    "nome": "Maria Silva",
    "email": "usuario@dominio..com",
    "cep": "12340678"
  },
  "itens": [
    {
      "produtoId": "P005",
      "quantidade": 1
    }
  ],
  "cupom": "BEMVINDO10"
}
```

5. Dispare a requisição.
6. Analise o status HTTP e o conteúdo da resposta.
7. Verifique se o pedido foi criado mesmo com o endereço de e-mail inválido.

---

## ❌ Comportamento Atual (Incorreto)

* **Status HTTP:** `201 Created` ❌
* A API aceita o endereço `usuario@dominio..com`.
* O pedido é criado normalmente.
* O e-mail sintaticamente inválido é persistido junto aos dados do pedido.
* Nenhuma mensagem de validação é apresentada ao consumidor da API.

O mesmo comportamento ocorre com o formato:

```text
usuario@dominio.com.
```

---

## ✅ Comportamento Esperado

A API deve realizar a validação sintática do campo `cliente.email` antes de processar e persistir o pedido.

Ao receber um endereço inválido, como `usuario@dominio..com` ou `usuario@dominio.com.`, a API deve:

* Rejeitar a requisição.
* Retornar `400 Bad Request` ou outro código definido pelo contrato da API para erro de validação.
* Informar que o campo `cliente.email` possui formato inválido.
* Impedir a criação/persistência do pedido.

Exemplo de resposta esperada:

```json
{
  "erro": {
    "codigo": "EMAIL_INVALIDO",
    "mensagem": "O e-mail informado possui formato inválido.",
    "campo": "cliente.email"
  }
}
```

---

## 📸 Evidências

### Evidência 01 — Ponto após o TLD

`erro-email3.png`

* **Entrada:** `usuario@dominio.com.`
* **Resultado:** `201 Created` ❌
* **Problema:** Pedido criado mesmo com formato de e-mail inválido.

### Evidência 02 — Pontos consecutivos no domínio

`erro-email-invalido.png`

* **Entrada:** `usuario@dominio..com`
* **Resultado:** `201 Created` ❌
* **Problema:** Pedido criado mesmo com pontos consecutivos no domínio.

---