# 🛒 Verzel Store - Automação de Testes (E2E & API)

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.14%2B-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Playwright-E2E%20%26%20API-green?logo=playwright&logoColor=white" alt="Playwright">
  <img src="https://img.shields.io/badge/Pytest-Framework-orange?logo=pytest&logoColor=white" alt="Pytest">
  <img src="https://img.shields.io/badge/BDD-Gherkin-yellow?logo=cucumber&logoColor=white" alt="BDD">
  <img src="https://img.shields.io/badge/Status-Conclu%C3%ADdo-success" alt="Status">
</p>

Repositório de testes automatizados desenvolvido como parte do processo seletivo de QA para a **Verzel Store**. O projeto abrange testes de ponta a ponta (E2E) com interface gráfica e testes de contrato e integração de API, aplicando boas práticas de mercado, Clean Code, rastreabilidade e relatórios detalhados de cenários e bugs.

---

## 📑 Sumário

- [Tecnologias e ferramentas](#️-tecnologias-e-ferramentas-utilizadas)
- [Estrutura do projeto](#-estrutura-detalhada-do-projeto)
- [O que contém em cada seção](#-o-que-contém-em-cada-seção)
- [Sobre o requirements.txt](#-sobre-o-arquivo-requirementstxt)
- [Como configurar e executar](#-como-configurar-e-executar-o-projeto)
- [Agradecimento](#-agradecimento-aos-recrutadores)

---

## 🛠️ Tecnologias e Ferramentas Utilizadas

- **Python**: linguagem principal utilizada para a estruturação dos scripts de automação.
- **Playwright**: framework moderno para automação web de ponta a ponta (E2E) e requisições HTTP assíncronas para testes de API.
- **Pytest**: framework robusto de execução e gestão de testes, utilizando fixtures e parametrização.
- **BDD / Gherkin**: abordagem de desenvolvimento guiado por comportamento para especificação de cenários de teste.
- **Git / GitHub**: controle de versão e versionamento de código.

---

## 📂 Estrutura Detalhada do Projeto

O projeto está organizado de forma modular, separando claramente a documentação de QA, os relatórios de defeitos, as evidências visuais e o código de automação:

```text
VERZEL-STORE/
│
├── docs/                               # Central de documentação e artefatos de QA
│   ├── bug-reports/                    # Relatórios de bugs detalhados (passos, severidade e evidências)
│   │   ├── BUG-VZS-142-01/
│   │   ├── BUG-VZS-142-02/
│   │   ├── BUG-VZS-142-03/
│   │   └── BUG-VZS-142-04/
│   └── Cenarios-evidencias/            # Artefatos visuais e comportamentais
│       ├── Cenarios-BDD/               # Especificações de cenários em Gherkin
│       │   └── cenarios-de-testes.md   # Mapeamento completo dos testes executados
│       └── evidencias/                 # Capturas de tela e vídeos de execução (Passou/Falhou)
│
├── tests/                              # Código-fonte da automação de testes
│   ├── api/                            # Testes de contrato, integração e segurança de API
│   │   └── test_produtos_api.py        # Validações de status 200, 404, segurança e métodos HTTP
│   ├── e2e/                            # Testes de interface (ponta a ponta)
│   │   ├── conftest.py                 # Configurações globais e fixtures reutilizáveis do Pytest
│   │   └── test_checkout.py            # Fluxo de compra, caminho feliz e validações
│   └── __init__.py                     # Inicializador de pacote Python
│
├── .gitignore                          # Arquivos e pastas ignorados pelo Git (ex: venv/)
├── requirements.txt                    # Dependências e bibliotecas do projeto
└── README.md                           # Documentação principal do repositório
```

---

## 📋 O que contém em cada seção

### 1. 📝 Estrutura de Cenários de Testes (BDD)

Na pasta `docs/Cenarios-evidencias/Cenarios-BDD/` encontram-se os cenários mapeados sob a ótica de **Behavior-Driven Development (BDD)**, com a sintaxe Gherkin (`Dado`, `Quando`, `Então`, `E`), garantindo o alinhamento entre as regras de negócio do e-commerce e a validação técnica.

### 2. 📸 Evidências dos Testes

A pasta `docs/Cenarios-evidencias/evidencias/` armazena as capturas de tela e gravações de vídeo (`.png` e `.mp4`) geradas durante as execuções, servindo como comprovação visual do comportamento da aplicação, tanto nos fluxos aprovados quanto nos cenários que resultaram em falhas.

### 3. 🐛 Bug Reports

Em `docs/bug-reports/` estão documentados os defeitos encontrados durante a homologação do sistema. Cada relatório possui identificador próprio (`BUG-VZS-142-XX`), descrição clara, passos para reprodução, comportamento esperado vs. obtido e vínculo direto com as evidências correspondentes.

### 4. 🌐 Testes E2E Automatizados (`tests/e2e/`)

- **Caminho feliz (Happy Path):** simula a adição da Camiseta Essencial ao carrinho, o preenchimento de dados de entrega válidos e a finalização bem-sucedida, com validação de ID dinâmico (`Pedido VZ-XXXXXX`).
- **Validações negativas e parametrizadas:** utiliza `@pytest.mark.parametrize` para testar as regras críticas do formulário (campos vazios, sobrenome ausente, e-mail inválido e CEP incompleto) de forma limpa e otimizada.

### 5. 🔌 Testes de API Automatizados (`tests/api/`)

- **Contrato e status 200:** valida a recuperação dos produtos existentes no endpoint `/api/produtos/{id}`, garantindo status 200 e que o ID retornado no JSON corresponda ao solicitado.
- **Resiliência e segurança (404 e edge cases):** testa o comportamento da API diante de IDs inexistentes, formatos inválidos e números negativos, além de tentativas simuladas de ataque como SQL Injection (`' OR '1'='1`) e XSS (`<script>`).
- **Métodos não permitidos:** assegura que operações de escrita (`POST`, `PUT`, `PATCH`, `DELETE`) em rotas de leitura sejam bloqueadas adequadamente.

---

## 📦 Sobre o arquivo `requirements.txt`

O `requirements.txt` garante a reprodutibilidade do ambiente de testes. Ele lista as bibliotecas externas exigidas pelo projeto (como `pytest` e `playwright`), permitindo que qualquer avaliador instale tudo com um único comando e evite conflitos de versão.

---

## 🚀 Como configurar e executar o projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/seu-usuario/verzel-store-qa.git
cd verzel-store-qa
```

### 2. Criar e ativar o ambiente virtual (`venv`)

**Windows (PowerShell):**

```powershell
python -m venv venv
.\venv\Scripts\Activate
```

**Linux / macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar as dependências e os navegadores

```bash
pip install -r requirements.txt
playwright install
```

### 4. Executar os testes automatizados

Todos os testes (E2E e API):

```bash
pytest
```

Apenas os testes E2E com o navegador visível (headed):

```bash
pytest tests/e2e --headed
```

Apenas os testes de API:

```bash
pytest tests/api/ -v
```

Um teste específico por nome:

```bash
pytest -k test_finalizar_compra -v
```

Gerar screenshot, vídeo e trace das falhas na pasta de evidências:

```bash
pytest tests/e2e --output=docs/Cenarios-evidencias/evidencias/playwright --screenshot=only-on-failure --video=retain-on-failure --tracing=retain-on-failure
```

---

## 💖 Agradecimento aos recrutadores

Gostaria de expressar minha profunda gratidão à equipe de recrutamento e aos avaliadores técnicos da Verzel pela oportunidade de participar deste processo seletivo. Desenvolver este projeto prático foi uma experiência extremamente enriquecedora, permitindo-me aplicar com rigor meus conhecimentos em automação de testes com Python e Playwright, especificação BDD, análise de cenários negativos e garantia de qualidade de ponta a ponta. Agradeço imensamente pelo desafio proposto e pelo aprendizado adquirido!

---

## 👤 Autor

**Seu Nome**

- GitHub: [@meu-usuario](https://github.com/bianca090)
- LinkedIn: [meu-perfil](https://www.linkedin.com/in/bianca-g-lira/)
