# Guia Educativo: Lógica de Programação

## Índice

1. [Introdução à Lógica de Programação](#introducao)
2. [Variáveis](#variaveis)
3. [Operadores](#operadores)
   - 3.1 Operadores Aritméticos
   - 3.2 Operadores Relacionais
   - 3.3 Operadores Lógicos
   - 3.4 Operadores de Atribuição
4. [Estruturas de Controle](#estruturas-de-controle)
   - 4.1 Condicional (if/else)
   - 4.2 Laços de Repetição (for, while)
5. [Funções](#funcoes)
   - 5.1 Definição de Funções
   - 5.2 Argumentos e Retorno
6. [Estruturas de Dados](#estruturas-de-dados)
   - 6.1 Listas
   - 6.2 Dicionários
   - 6.3 Tuplas
   - 6.4 Conjuntos
7. [Exercícios Práticos](#exercicios)
8. [Conclusão](#conclusao)

## 1. Introdução à Lógica de Programação

A lógica de programação é o fundamento essencial para o desenvolvimento de softwares. Trata-se de organizar passos lógicos para resolver problemas computacionais. Compreender conceitos básicos, como variáveis, operadores, e estruturas de controle, é o primeiro passo para programar em qualquer linguagem.

## 2. Variáveis

Uma variável é um espaço na memória para armazenar valores temporariamente. Em Python, você não precisa declarar o tipo da variável, pois ele é definido automaticamente com base no valor atribuído.

Exemplo:

```python
nome = "João"  # String
total = 42       # Inteiro
preco = 19.99    # Float
ativo = True     # Booleano
```

## 3. Operadores

### 3.1 Operadores Aritméticos

Realizam operações matemáticas.

```python
soma = 10 + 5
subtracao = 10 - 5
multiplicacao = 10 * 5
divisao = 10 / 5
resto = 10 % 3
exponenciacao = 2 ** 3
```

### 3.2 Operadores Relacionais

Comparam valores, retornando `True` ou `False`.

```python
x = 10
y = 20

print(x > y)  # False
print(x == y) # False
print(x != y) # True
```

### 3.3 Operadores Lógicos

Combinam expressões lógicas.

```python
x = 5
y = 10

print(x > 3 and y < 20)  # True
print(x < 3 or y > 15)   # False
print(not(x > 3))        # False
```

### 3.4 Operadores de Atribuição

Utilizados para definir ou modificar valores de variáveis.

```python
x = 10
x += 5  # x = x + 5
x *= 2  # x = x * 2
```

## 4. Estruturas de Controle

### 4.1 Condicional (if/else)

Controla o fluxo com base em condições.

```python
idade = 18
if idade >= 18:
    print("Você é maior de idade.")
else:
    print("Você é menor de idade.")
```

### 4.2 Laços de Repetição

#### Laço `for`

Itera sobre uma sequência.

```python
for i in range(5):
    print(f"Iteração {i}")
```

#### Laço `while`

Executa enquanto a condição for verdadeira.

```python
x = 0
while x < 5:
    print(f"Valor atual: {x}")
    x += 1
```

## 5. Funções

### 5.1 Definição de Funções

Funções são blocos de código reutilizáveis.

```python
def saudacao():
    print("Olá, mundo!")

saudacao()
```

### 5.2 Argumentos e Retorno

```python
def soma(a, b):
    return a + b

resultado = soma(10, 5)
print(resultado)  # 15
```

## 6. Estruturas de Dados

### 6.1 Listas

Uma coleção ordenada e mutável.

```python
numeros = [1, 2, 3, 4]
numeros.append(5)
print(numeros)
```

### 6.2 Dicionários

Armazenam pares de chave e valor.

```python
dados = {"nome": "Ana", "idade": 25}
print(dados["nome"])
```

### 6.3 Tuplas

Semelhantes às listas, mas imutáveis.

```python
cores = ("vermelho", "azul")
print(cores[0])
```

### 6.4 Conjuntos

Coleções não ordenadas e sem duplicatas.

```python
numeros = {1, 2, 2, 3}
print(numeros)  # {1, 2, 3}
```

## 7. Exercícios Práticos

### Exercícios Básicos

1. Crie uma variável chamada `nome` e atribua a ela o seu nome. Em seguida, exiba a mensagem: "Olá, <nome>!".
2. Escreva um programa que calcule o quadrado de um número fornecido pelo usuário.
3. Crie um programa que receba duas notas de um aluno e calcule a média.

### Exercícios Intermediários

4. Escreva um programa que exiba todos os números pares de 1 a 20.
5. Faça um programa que leia um número do usuário e exiba a tabuada desse número (de 1 a 10).
6. Escreva um programa que leia uma lista de números e exiba apenas os números maiores que 10.

### Exercício Avançado (Explicado)

7. FizzBuzz: Exiba os números de 1 a 100, substituindo múltiplos de 3 por "Fizz", múltiplos de 5 por "Buzz" e múltiplos de ambos por "FizzBuzz".

**Dica**: Use um laço `for` e condicionais para resolver.

Exemplo de lógica:

```python
for i in range(1, 101):
    if i % 3 == 0 and i % 5 == 0:
        print("FizzBuzz")
    elif i % 3 == 0:
        print("Fizz")
    elif i % 5 == 0:
        print("Buzz")
    else:
        print(i)
```

## 8. Conclusão

A lógica de programação é o alicerce para se tornar um programador habilidoso. Dominar variáveis, operadores, estruturas de controle e funções é essencial. Pratique com os exemplos e exercícios para solidificar seu aprendizado!

