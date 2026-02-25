## Lab 01 – Calculadora de Linha de Comando em Python

### 1. Objetivo

Criar uma **calculadora simples** que roda no terminal, usando:

- Entrada de dados com `input`.
- Conversão de tipos (`int`, `float`).
- Condicionais (`if/elif/else`).
- Laços (`while`) para repetir até o usuário decidir sair.
- Tratamento básico de erros.

Este exercício simula pequenos utilitários de linha de comando muito usados em times de tecnologia para automatizar tarefas simples.

---

### 2. Descrição do Problema

Você deve implementar um programa `calculadora.py` que:

- Mostra um **menu de operações**: soma, subtração, multiplicação, divisão.
- Pede dois números para o usuário.
- Executa a operação escolhida.
- Exibe o resultado.
- Permite repetir a operação até o usuário escolher sair.

Exemplo de fluxo:

```
=== Calculadora CLI ===
1) Somar
2) Subtrair
3) Multiplicar
4) Dividir
0) Sair
Escolha uma opção: 1

Digite o primeiro número: 10
Digite o segundo número: 5
Resultado: 15
```

---

### 3. Requisitos Mínimos

- Arquivo principal: `calculadora.py`.
- Usar um **loop** principal para o menu (por exemplo, `while True:`).
- Implementar as 4 operações básicas:
  - Soma
  - Subtração
  - Multiplicação
  - Divisão (com cuidado para não dividir por zero).
- Tratar pelo menos:
  - Erro de **entrada inválida** (quando o usuário digita texto onde deveria ser número).
  - **Divisão por zero**.
- Permitir que o usuário **saia** escolhendo a opção 0.

---

### 4. Passos Sugeridos

1. **Criar o esqueleto do programa**

   - Imprimir o título da calculadora.
   - Criar um loop infinito (`while True`) para o menu.

2. **Implementar o menu**

   - Exibir as opções.
   - Ler a escolha do usuário.
   - Usar `if/elif/else` para decidir o que fazer em cada opção.

3. **Ler os operandos**

   - Para as opções 1 a 4:
     - Pedir dois números com `input`.
     - Converter para `float` ou `int`.

4. **Realizar a operação**

   - Calcular o resultado de acordo com a opção.
   - Exibir o resultado em um `print`.

5. **Adicionar tratamento de erros**

   - Usar `try/except` ao converter a entrada para número.
   - Verificar se o divisor é zero na divisão.

6. **Opção de saída**

   - Se a opção for `0`, exibir mensagem de despedida e sair do loop com `break`.

---

### 5. Exemplo de Estrutura de Código (Esqueleto)

Não copie e cole tudo sem entender. Use apenas como guia de organização:

```python
def mostrar_menu():
    print("=== Calculadora CLI ===")
    print("1) Somar")
    print("2) Subtrair")
    print("3) Multiplicar")
    print("4) Dividir")
    print("0) Sair")


while True:
    mostrar_menu()
    opcao = input("Escolha uma opção: ")

    if opcao == "0":
        print("Saindo...")
        break

    # aqui você trata as demais opções
```

---

### 6. Extensões (Desafios Extras)

Se você completar os requisitos mínimos, tente ir além:

- **Desafio 1 – Repetir operação automaticamente**
  - Depois de mostrar o resultado, perguntar se o usuário quer usar o **resultado como primeiro número** da próxima operação.

- **Desafio 2 – Histórico de operações**
  - Guardar em uma lista todas as operações realizadas (ex.: `"10 + 5 = 15"`).
  - Adicionar uma opção no menu para listar o histórico.

- **Desafio 3 – Funções separadas**
  - Criar funções como `somar(a, b)`, `subtrair(a, b)` etc.
  - Criar uma função `ler_numero(mensagem)` que trata erros de conversão.

- **Desafio 4 – Interface mais amigável**
  - Limpar a tela (em sistemas Unix, `os.system("clear")`) entre operações.
  - Melhorar mensagens de erro.

---

### 7. Conexão com o Mundo Real

Pode parecer apenas um exercício simples de matemática, mas:

- Você está praticando **entrada/saída**, **tratamento de erros**, **loops**, **funções**.
- Esses conceitos são usados em:
  - Scripts internos de **automação de tarefas**.
  - Ferramentas de **linha de comando** que disparam jobs de IA/ML.
  - Programas auxiliares para times de dados (por exemplo, utilitários para testar APIs ou manipular arquivos).

Guarde esse arquivo no seu repositório de estudos. Mais tarde, você pode revisitar a calculadora para:

- Transformá-la em um **CLI mais profissional** com bibliotecas como `typer` ou `click`.
- Usá-la como base para entender como se organiza um projeto Python real.

