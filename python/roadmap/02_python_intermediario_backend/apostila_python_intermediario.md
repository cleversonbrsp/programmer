## Apostila – Python Intermediário e Backend

### 1. Objetivos da Fase

Nesta fase, você vai:

- Sair do uso “solto” de scripts para uma visão mais **profissional** de projetos Python.
- Entender **módulos**, **pacotes** e como organizar código em múltiplos arquivos.
- Usar **ambientes virtuais** e gerenciar dependências com `pip` (Poetry será aprofundado na fase 03).
- Conhecer boas práticas de código (PEP 8, estrutura de projeto, testes básicos).
- Criar uma **API REST simples com FastAPI**.
- Construir **CLIs de automação** para tarefas do dia a dia.

Essa fase é crucial para atingir o nível esperado de um **Desenvolvedor Python Pleno**, baseando-se em padrões usados em times de backend e IA.

---

### 2. Módulos e Pacotes

#### 2.1 Módulos

Um **módulo** é um arquivo `.py` que pode ser importado em outro.

Exemplo de estrutura:

```text
meu_projeto/
  ├── main.py
  └── util.py
```

`util.py`:

```python
def soma(a, b):
    return a + b
```

`main.py`:

```python
from util import soma

print(soma(2, 3))
```

#### 2.2 Pacotes

Um **pacote** é uma pasta com um arquivo `__init__.py` (em versões atuais nem sempre é obrigatório, mas ainda é comum).

```text
meu_projeto/
  ├── main.py
  └── calculos/
      ├── __init__.py
      └── basico.py
```

`basico.py`:

```python
def multiplicar(a, b):
    return a * b
```

`main.py`:

```python
from calculos.basico import multiplicar

print(multiplicar(4, 5))
```

Organizar o projeto em pacotes torna mais fácil:

- Reutilizar código.
- Entender responsabilidades de cada arquivo.
- Evoluir para um projeto instalável.

---

### 3. Ambientes Virtuais e `pip`

Ambientes virtuais isolam dependências de cada projeto.

#### 3.1 Criando um ambiente virtual com `venv`

```bash
python -m venv .venv
```

Ativando (Linux/macOS):

```bash
source .venv/bin/activate
```

Verifique:

```bash
which python
python --version
```

#### 3.2 Instalando bibliotecas com `pip`

```bash
pip install fastapi uvicorn
```

Gerando um `requirements.txt`:

```bash
pip freeze > requirements.txt
```

Isso é importante em ambientes corporativos para:

- Reproduzir o ambiente.
- Permitir que outros desenvolvedores instalem as mesmas dependências.

---

### 4. Boas Práticas de Código (PEP 8, Estrutura, Logs)

#### 4.1 PEP 8 – Estilo

Algumas regras importantes:

- 4 espaços por nível de indentação.
- Nomes de funções e variáveis em `snake_case`.
- Linhas até ~79 caracteres (não precisa ser rígido, mas é um guia).

```python
def calcular_total(preco_unitario, quantidade):
    return preco_unitario * quantidade
```

#### 4.2 Estrutura mínima de projeto backend

Exemplo simples:

```text
api_tarefas/
  ├── app/
  │   ├── __init__.py
  │   ├── main.py
  │   ├── models.py
  │   └── routes.py
  ├── tests/
  │   └── test_exemplo.py
  ├── requirements.txt
  └── README.md
```

#### 4.3 Logs

Ao invés de apenas `print`, use o módulo `logging`:

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Aplicação iniciada")
```

Logs são essenciais em ambientes corporativos para:

- Depurar problemas em produção.
- Investigar falhas em integrações com APIs e serviços de IA.

---

### 5. Introdução a APIs REST com FastAPI

FastAPI é uma das principais escolhas para construir APIs em Python.

#### 5.1 Instalação

```bash
pip install fastapi uvicorn
```

#### 5.2 Exemplo mínimo de API

Crie um arquivo `main.py`:

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/status")
def ler_status():
    return {"status": "ok"}
```

Rodando a API:

```bash
uvicorn main:app --reload
```

Você terá:

- Endpoint `GET /status` retornando JSON.
- Documentação automática em `/docs` (Swagger) e `/redoc`.

Esse modelo é a base para:

- Expor **serviços de IA** como APIs.
- Criar camadas de backend que chamam LLMs internamente.

---

### 6. Conceitos de Backend Relacionados à Vaga

Para atuar em projetos de IA/LLM em contexto corporativo, é comum:

- Expor uma **API REST** que recebe:
  - Pergunta do usuário.
  - Contexto adicional.
  - Parâmetros de configuração (por exemplo, temperatura do modelo).
- A API:
  - Chama um serviço de LLM (por exemplo, OpenAI, local, etc.).
  - Integra com outras APIs internas (CRM, ERP, banco de dados).
  - Devolve a resposta já processada para o cliente (front, bot, outro sistema).

Por isso, entender:

- **Rotas, métodos HTTP, status codes, JSON, parâmetros de rota e query**.
- Diferenciar responsabilidades entre:
  - **Camada de API** (controle de requisições).
  - **Camada de negócio** (regras).
  - **Camada de integração com LLM** (chamadas à API do modelo).

é fundamental.

---

### 7. CLIs de Automação

Além de APIs, CLIs são muito usados para:

- Rodar tarefas de manutenção.
- Executar rotinas internas (por exemplo, processar um lote de arquivos de texto para indexar em um RAG).

Modelo simples de CLI:

```python
import argparse


def main():
    parser = argparse.ArgumentParser(description="Exemplo de CLI")
    parser.add_argument("--arquivo", required=True, help="Caminho do arquivo de entrada")
    args = parser.parse_args()

    print("Processando arquivo:", args.arquivo)


if __name__ == "__main__":
    main()
```

Boas práticas:

- Usar `if __name__ == "__main__":` para ponto de entrada.
- Separar lógica de negócio em funções/módulos reutilizáveis.

---

### 8. Testes (Introdução)

Mesmo em nível intermediário, é importante conhecer **testes automatizados**.

#### 8.1 Usando `pytest`

Instale:

```bash
pip install pytest
```

Crie um arquivo `test_exemplo.py`:

```python
from app.main import soma


def test_soma():
    assert soma(2, 3) == 5
```

Rode:

```bash
pytest
```

Ter testes aumenta a confiança quando você:

- Integra novas features de IA.
- Refatora pipelines de LLM ou lógica de RAG.

---

### 9. Conexão com as Próximas Fases

Depois desta fase, você terá:

- Base para desenvolver **APIs** e **CLIs** reutilizáveis.
- Entendimento claro de **organização de projeto**, **imports** e **ambientes**.

Isso será essencial quando:

- Criarmos uma **API de tarefas** com FastAPI (lab 01 desta fase).
- Construirmos CLIs de automação (lab 02).
- Migrarmos para projetos que consumirão **LLMs**, **embeddings** e **RAG**, orquestrados por frameworks como **LangChain**, **LlamaIndex** e **CrewAI**.

O foco, daqui em diante, é deixar seu código pronto para “vida real” em times de IA e backend corporativo.

