## Apostila – Python Básico

### 1. Objetivos da Fase

Nesta fase, você vai:

- Entender o que é Python e como instalar/executar seus primeiros scripts.
- Dominar **tipos básicos**: números, strings, booleanos.
- Usar **variáveis**, **entrada de dados**, **condicionais** (`if/else`) e **loops** (`for`, `while`).
- Trabalhar com **listas**, **tuplas**, **dicionários**.
- Criar **funções** simples e organizar melhor seu código.
- Ler e escrever **arquivos de texto**.

Ao final, você estará pronto para:

- Resolver problemas simples de lógica.
- Criar programas de linha de comando (CLIs) como:
  - Uma **calculadora**.
  - Um **jogo da forca**.
  - Uma **mini agenda** gravando dados em arquivos.

---

### 2. Ambiente de Desenvolvimento

**Passos mínimos:**

- Instale o Python 3 (idealmente 3.10+).
- Confirme no terminal:

```bash
python --version
```

ou

```bash
python3 --version
```

- Crie uma pasta para estudos, por exemplo `python-estudos`.

Para executar um script:

```bash
python hello.py
```

---

### 3. Primeiro Programa em Python

Crie um arquivo `hello.py`:

```python
print("Olá, mundo!")
```

Conceitos:

- `print(...)` envia texto para a saída padrão (terminal).
- Aspas simples ou duplas definem uma **string**.

---

### 4. Tipos Básicos e Operadores

Principais tipos:

- **int**: números inteiros (`1`, `42`, `-7`).
- **float**: números com casa decimal (`3.14`, `0.5`).
- **str**: textos (`"Python"`, `"Olá"`).
- **bool**: booleanos (`True`, `False`).

Exemplo:

```python
idade = 30          # int
altura = 1.75       # float
nome = "Ana"        # str
ativo = True        # bool
```

Operadores aritméticos:

- `+` (soma), `-` (subtração), `*` (multiplicação), `/` (divisão float),
- `//` (divisão inteira), `%` (resto), `**` (potência).

```python
resultado = (2 + 3) * 4
print(resultado)  # 20
```

Operadores de comparação:

- `==`, `!=`, `<`, `>`, `<=`, `>=` retornam `True` ou `False`.

---

### 5. Variáveis e Entrada de Dados

Variáveis guardam valores na memória:

```python
nome = "João"
idade = 25
print("Nome:", nome)
print("Idade:", idade)
```

Entrada via teclado com `input()`:

```python
nome = input("Digite seu nome: ")
print("Olá,", nome)
```

`input` sempre retorna uma **string**. Para números:

```python
idade = int(input("Digite sua idade: "))
altura = float(input("Digite sua altura: "))
```

---

### 6. Condicionais (`if`, `elif`, `else`)

Permitem decisões no código:

```python
idade = int(input("Idade: "))

if idade < 18:
    print("Menor de idade.")
elif idade < 60:
    print("Adulto.")
else:
    print("Idoso.")
```

Regras importantes:

- Blocos são definidos por **indentação** (4 espaços por convenção).
- `elif` e `else` são opcionais.

---

### 7. Laços de Repetição (`for`, `while`)

**Loop `for` com `range`:**

```python
for i in range(5):
    print("i =", i)
```

- `range(5)` gera 0, 1, 2, 3, 4.

**Loop `while`:**

```python
contador = 0

while contador < 3:
    print("Contador:", contador)
    contador += 1
```

Use `while` quando não souber exatamente quantas repetições serão necessárias.

---

### 8. Estruturas de Dados Básicas

#### 8.1 Listas

Listas são coleções mutáveis:

```python
frutas = ["maçã", "banana", "laranja"]
frutas.append("uva")
print(frutas[0])      # "maçã"
print(len(frutas))    # tamanho da lista
```

Percorrendo listas:

```python
for fruta in frutas:
    print(fruta)
```

#### 8.2 Tuplas

Parecidas com listas, mas **imutáveis**:

```python
coordenada = (10, 20)
x, y = coordenada
```

#### 8.3 Dicionários

Chave → valor:

```python
usuario = {
    "nome": "Maria",
    "idade": 28,
}

print(usuario["nome"])
usuario["cidade"] = "São Paulo"
```

Iterando:

```python
for chave, valor in usuario.items():
    print(chave, "=", valor)
```

---

### 9. Funções

Funções ajudam a **reutilizar código**:

```python
def saudacao(nome):
    print(f"Olá, {nome}!")

saudacao("Ana")
```

Função com retorno:

```python
def soma(a, b):
    return a + b

resultado = soma(2, 3)
print(resultado)
```

Boas práticas:

- Funções devem ter **nome claro**.
- Uma função deve ter **responsabilidade única** ou bem limitada.

---

### 10. Tratamento de Erros (Introdução)

Uso básico de `try/except`:

```python
try:
    numero = int(input("Digite um número: "))
    print("Dobro:", numero * 2)
except ValueError:
    print("Você não digitou um número válido.")
```

Essa noção básica já ajuda em CLIs como a calculadora.

---

### 11. Manipulação de Arquivos

Ler e escrever arquivos é essencial para muitos sistemas reais. Exemplo:

```python
with open("dados.txt", "w", encoding="utf-8") as f:
    f.write("Linha 1\n")
    f.write("Linha 2\n")
```

Lendo:

```python
with open("dados.txt", "r", encoding="utf-8") as f:
    conteudo = f.read()
    print(conteudo)
```

Leitura linha a linha:

```python
with open("dados.txt", "r", encoding="utf-8") as f:
    for linha in f:
        print(linha.strip())
```

Esses conceitos serão usados no **lab da mini agenda**.

---

### 12. Boas Práticas desde o Início

- Use nomes de variáveis claros: `total_pedidos`, `preco_unitario`.
- Quebre problemas grandes em funções menores.
- Use comentários apenas quando o **código não for óbvio**.
- Teste com diferentes entradas (incluindo casos extremos).

---

### 13. Conexão com a Carreira em IA/LLM

Mesmo parecendo simples, tudo que você está aprendendo aqui é base para:

- Criar **scripts de ETL** (extrair, transformar e carregar dados) que alimentarão modelos.
- Implementar **CLIs de utilidade interna** em times de dados e IA.
- Entender a lógica por trás de **pipelines de IA** (if/else, loops, funções, manipulação de listas e dicionários).
- Facilitar a migração posterior para:
  - Chamadas de API de LLMs.
  - Manipulação de respostas de modelos (que normalmente chegam em JSON/dicionários).

Antes de seguir, tente completar todos os labs desta fase. Isso garantirá uma base sólida para as próximas etapas.

