## Lab 03 – Mini Agenda com Arquivos em Python

### 1. Objetivo

Criar uma **mini agenda de contatos** que salva e lê dados de um arquivo de texto, para praticar:

- Leitura e escrita de arquivos (`open`, `read`, `write`).
- Estruturas de dados (`listas`, `dicionários`).
- Loops e condicionais.
- Organização em funções.

Este lab é uma ponte direta para aplicações reais de backend e scripts de suporte em IA, onde você frequentemente vai ler e gravar dados em arquivos antes de enviá-los para modelos.

---

### 2. Descrição do Problema

Você deve criar um programa `agenda.py` que:

- Mantém uma lista de contatos, com pelo menos:
  - Nome
  - Telefone
  - (Opcional) E-mail
- Salva os contatos em um arquivo de texto, por exemplo `contatos.txt`.
- Carrega os contatos do arquivo quando o programa inicia.
- Permite:
  - Listar contatos.
  - Adicionar contato.
  - Buscar contato pelo nome.
  - Sair do programa, salvando as alterações.

Formato simples sugerido do arquivo (um contato por linha):

```text
nome;telefone;email
Ana;1111-1111;ana@example.com
João;2222-2222;joao@example.com
```

---

### 3. Requisitos Mínimos

- Arquivo principal: `agenda.py`.
- Nome fixo para o arquivo de dados (ex.: `contatos.txt` na mesma pasta).
- Funções mínimas:
  - Carregar contatos do arquivo ao iniciar.
  - Salvar contatos no arquivo ao sair.
- Menu com opções como:
  - `1) Listar contatos`
  - `2) Adicionar contato`
  - `3) Buscar contato por nome`
  - `0) Sair`
- Usar **lista de dicionários** em memória, por exemplo:

```python
contatos = [
    {"nome": "Ana", "telefone": "1111-1111", "email": "ana@example.com"},
]
```

---

### 4. Passos Sugeridos

1. **Definir o nome do arquivo**

   ```python
   ARQUIVO_CONTATOS = "contatos.txt"
   ```

2. **Implementar a função de carregar contatos**

   - Se o arquivo não existir, retornar lista vazia.
   - Se existir:
     - Ler linha por linha.
     - Quebrar cada linha por `";"` com `.split(";")`.
     - Montar dicionários e adicionar à lista.

3. **Implementar a função de salvar contatos**

   - Abrir o arquivo em modo `"w"` (sobrescrever).
   - Para cada contato na lista, escrever uma linha no formato `nome;telefone;email`.

4. **Criar menu principal**

   - Loop `while True`.
   - Mostrar opções.
   - Ler escolha do usuário.
   - Chamar funções adequadas para cada opção.

5. **Implementar operação de adicionar contato**

   - Ler nome, telefone e (opcional) e-mail via `input`.
   - Adicionar na lista de contatos em memória.

6. **Implementar busca por nome**

   - Pedir um termo de busca.
   - Percorrer a lista e mostrar os contatos cujo nome contiver o termo.

7. **Ao sair, salvar os contatos**

   - Quando o usuário escolher a opção 0:
     - Chamar a função de salvar contatos.
     - Exibir mensagem e encerrar.

---

### 5. Dicas de Implementação

- Para verificar se o arquivo existe, você pode usar `os.path.exists`:

```python
import os

if os.path.exists(ARQUIVO_CONTATOS):
    # carregar contatos
```

- Para evitar problemas com quebras de linha:

```python
linha = linha.strip()
```

- Para busca simples por nome (case insensitive):

```python
termo = input("Buscar por nome: ").strip().lower()

for contato in contatos:
    if termo in contato["nome"].lower():
        print(contato)
```

---

### 6. Extensões (Desafios Extras)

Se você concluir os requisitos mínimos, tente:

- **Desafio 1 – Remover e editar contatos**
  - Adicionar opção para remover contato pelo nome.
  - Adicionar opção para editar telefone/e-mail de um contato.

- **Desafio 2 – Validação de dados**
  - Impedir cadastro de contatos sem nome.
  - Verificar se o telefone não está vazio.

- **Desafio 3 – Formatação de saída**
  - Exibir contatos em formato tabular, por exemplo:

  ```text
  Nome       | Telefone   | E-mail
  Ana        | 1111-1111  | ana@example.com
  João       | 2222-2222  | joao@example.com
  ```

- **Desafio 4 – Arquivo CSV “de verdade”**
  - Usar o módulo `csv` da biblioteca padrão para ler/gravar o arquivo com mais segurança.

---

### 7. Conexão com o Mundo Real e IA/LLM

Este exercício é uma mini versão de tarefas muito comuns em ambientes de IA:

- Ler e gravar dados em arquivos de texto ou CSV antes de enviar para modelos.
- Organizar informações em **estruturas de dados** claras (listas de dicionários).
- Implementar operações básicas de **CRUD** (Create, Read, Update, Delete).

Quando você estiver trabalhando com LLMs e RAG, fará coisas semelhantes:

- Carregar documentos.
- Transformar/normalizar dados.
- Salvar resultados de consultas ou processamentos.

Por isso, domine bem este lab. Ele será útil como base conceitual para as próximas fases (APIs, ML e RAG).

