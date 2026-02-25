## Lab 01 – API de Tarefas com FastAPI

### 1. Objetivo

Criar uma **API REST simples de tarefas** usando FastAPI, para praticar:

- Estrutura básica de API backend.
- Endpoints `GET`, `POST`, `PUT`, `DELETE`.
- Manipulação de dados em memória (lista/dicionário).
- Conceitos diretamente aplicáveis a **APIs que expõem serviços de IA/LLM**.

---

### 2. Descrição do Problema

Você deve implementar uma API que gerencia uma lista de tarefas (to-do list). Cada tarefa deve ter:

- `id` (inteiro)
- `titulo` (string)
- `descricao` (string opcional)
- `concluida` (booleano)

Operações mínimas:

- Listar todas as tarefas.
- Recuperar uma tarefa pelo `id`.
- Criar nova tarefa.
- Atualizar tarefa existente.
- Remover tarefa.

---

### 3. Requisitos Mínimos

- Projeto em uma pasta, por exemplo `api_tarefas/`.
- Arquivo principal: `main.py`.
- Utilizar FastAPI e uvicorn.
- Endpoints:
  - `GET /tarefas`
  - `GET /tarefas/{id}`
  - `POST /tarefas`
  - `PUT /tarefas/{id}`
  - `DELETE /tarefas/{id}`
- Dados podem ser armazenados em uma **lista em memória** (não precisa de banco de dados).
- Utilizar modelos Pydantic para requisições e respostas.

---

### 4. Passos Sugeridos

1. **Criar ambiente virtual e instalar dependências**

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install fastapi uvicorn
   ```

2. **Criar estrutura inicial do projeto**

   ```text
   api_tarefas/
     └── main.py
   ```

3. **Configurar a aplicação FastAPI**

   Em `main.py`:

   - Instanciar `FastAPI()`.
   - Criar uma lista de tarefas em memória.
   - Definir modelos Pydantic para entrada/saída.

4. **Implementar endpoints**

   - `GET /tarefas`: retorna lista completa.
   - `GET /tarefas/{id}`: busca tarefa específica ou retorna erro 404.
   - `POST /tarefas`: cria tarefa nova.
   - `PUT /tarefas/{id}`: atualiza dados de tarefa existente.
   - `DELETE /tarefas/{id}`: remove tarefa.

5. **Testar com a documentação automática**

   - Rodar:

   ```bash
   uvicorn main:app --reload
   ```

   - Acessar o navegador em:
     - `http://localhost:8000/docs`
     - `http://localhost:8000/redoc`

---

### 5. Esqueleto de Código Sugerido

Use apenas como guia; adapte conforme necessário:

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List


class Tarefa(BaseModel):
    id: int
    titulo: str
    descricao: Optional[str] = None
    concluida: bool = False


class TarefaCreate(BaseModel):
    titulo: str
    descricao: Optional[str] = None


app = FastAPI()

tarefas: List[Tarefa] = []


@app.get("/tarefas", response_model=List[Tarefa])
def listar_tarefas():
    return tarefas


@app.post("/tarefas", response_model=Tarefa)
def criar_tarefa(tarefa_in: TarefaCreate):
    novo_id = len(tarefas) + 1
    tarefa = Tarefa(id=novo_id, **tarefa_in.dict())
    tarefas.append(tarefa)
    return tarefa
```

Você deve complementar com os outros endpoints.

---

### 6. Extensões (Desafios Extras)

Se os requisitos mínimos estiverem completos, tente:

- **Desafio 1 – Filtro por status**
  - Adicionar um parâmetro de query em `GET /tarefas` para filtrar:
    - `?concluida=true` ou `?concluida=false`.

- **Desafio 2 – Paginação simples**
  - Parâmetros `limit` e `offset` para controlar quantas tarefas retornar por vez.

- **Desafio 3 – Persistência simples em arquivo**
  - Ao iniciar, carregar tarefas de um arquivo JSON.
  - Ao encerrar ou a cada modificação, salvar tarefas em um arquivo JSON.

- **Desafio 4 – Organização em módulos**
  - Separar modelos, rotas e dados em arquivos diferentes (`models.py`, `routes.py`, etc.).

---

### 7. Conexão com IA/LLM e RAG

Uma API de tarefas simples pode parecer distante de IA, mas está diretamente ligada ao que você fará em projetos de LLM:

- A mesma estrutura de **rotas, requisições e respostas JSON** será usada para:
  - Expor endpoints como `/chat`, `/resumo`, `/rag/consulta`.
  - Receber perguntas, contexto e parâmetros.
  - Chamar internamente um **LLM** (via SDK ou HTTP) e retornar a resposta.

Conceitos que você já pratica aqui:

- Organização de um **serviço backend**.
- Tratamento de erros (`HTTPException`).
- Trabalho com modelos de dados (Pydantic) – algo análogo a esquemas de entrada/saída em pipelines de IA.

Guarde este projeto como base: você poderá reaproveitar a estrutura para criar uma API que conversa com LLMs na fase de LLM/RAG.

