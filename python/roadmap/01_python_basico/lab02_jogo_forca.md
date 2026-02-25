## Lab 02 – Jogo da Forca em Python

### 1. Objetivo

Criar um **jogo da forca** simples no terminal, para praticar:

- Manipulação de **strings**.
- Uso de **listas**.
- Loops com condição de parada.
- Condicionais e controle de fluxo.
- Organização em funções.

Este tipo de exercício ajuda a pensar em **estado do jogo**, algo muito parecido com o que você precisará fazer ao controlar estados de um chatbot ou fluxo de conversas com LLMs.

---

### 2. Descrição do Problema

Você deve implementar um programa `forca.py` que:

- Escolhe uma palavra secreta (pode ser fixa ou escolhida aleatoriamente de uma lista).
- Mostra ao jogador a palavra como uma sequência de traços (`_`), um para cada letra.
- Permite que o jogador chute letras.
- Atualiza o estado do jogo:
  - Substituindo os traços pelas letras corretas.
  - Contabilizando erros.
- Termina o jogo quando:
  - O jogador acerta todas as letras (vitória).
  - O jogador atinge um número máximo de erros (derrota).

---

### 3. Requisitos Mínimos

- Arquivo principal: `forca.py`.
- Palavra secreta fixa (por exemplo `"python"`) ou retirada de uma lista de poucas palavras.
- Mostrar ao usuário:
  - A palavra com traços e/ou letras descobertas.
  - As letras já tentadas.
  - Quantos erros ainda restam.
- Limitar a quantidade de erros (por exemplo, **6 erros**).
- Tratar entrada inválida (vazia, mais de uma letra, caracteres não alfabéticos).

---

### 4. Passos Sugeridos

1. **Definir a palavra secreta**

   - Ex.: `palavra_secreta = "python"`.
   - Criar uma lista para representar o estado atual:

   ```python
   estado_atual = ["_"] * len(palavra_secreta)
   ```

2. **Criar variáveis de controle**

   - Número máximo de erros (por ex. `max_erros = 6`).
   - Lista de letras já tentadas.
   - Contador de erros atuais.

3. **Loop principal do jogo (`while`)**

   - Enquanto o jogador não tiver ganho nem perdido:
     - Mostrar `estado_atual`.
     - Mostrar letras tentadas e erros restantes.
     - Ler uma letra do usuário.

4. **Processar a letra chutada**

   - Se a letra **já foi tentada**, avisar e continuar para próxima iteração.
   - Se a letra **está na palavra**:
     - Atualizar `estado_atual` nas posições corretas.
   - Caso contrário:
     - Incrementar o contador de erros.

5. **Verificar condições de fim de jogo**

   - Vitória: se não houver mais `"_"` em `estado_atual`.
   - Derrota: se `erros >= max_erros`.

6. **Mostrar o resultado final**

   - Em caso de vitória: mensagem de parabéns.
   - Em caso de derrota: mostrar a palavra secreta.

---

### 5. Dicas de Implementação

- Para atualizar o estado quando o jogador acerta uma letra:

```python
for i, letra in enumerate(palavra_secreta):
    if letra == chute:
        estado_atual[i] = chute
```

- Para verificar vitória:

```python
if "_" not in estado_atual:
    # ganhou
```

- Para normalizar a entrada:
  - Converter tudo para **minúsculas** com `.lower()`.
  - Remover espaços com `.strip()`.

---

### 6. Extensões (Desafios Extras)

Se você completar o jogo básico, tente:

- **Desafio 1 – Lista de palavras**
  - Criar uma lista de palavras (`["python", "dados", "modelo", "api"]`).
  - Escolher uma palavra aleatoriamente usando o módulo `random`.

- **Desafio 2 – Desenho da forca**
  - Exibir um “desenho” da forca com base na quantidade de erros (pode ser apenas texto ASCII).

- **Desafio 3 – Separar em funções**
  - Funções como:
    - `exibir_estado(estado_atual, letras_tentadas, erros_restantes)`
    - `processar_chute(chute, palavra_secreta, estado_atual, letras_tentadas)`

- **Desafio 4 – Jogar novamente**
  - Depois do fim do jogo, perguntar se o usuário quer jogar de novo.

---

### 7. Conexão com o Mundo Real e IA/LLM

Esse jogo trabalha conceitos importantes para a carreira em IA:

- **Estado**: o jogo guarda informações de contexto (letras já chutadas, erros, progresso), conceito análogo ao **estado de uma conversa com um chatbot**.
- **Validação de entrada**: garantir que o usuário digitou algo válido é similar a validar inputs de uma API ou requisição de usuário.
- **Controle de fluxo**: usar loops e condicionais de forma clara é fundamental para implementar **pipelines de processamento de texto**, como pré-processamento antes de passar dados para um LLM.

Mais adiante, você poderia:

- Criar uma versão da forca que utiliza um **LLM para sugerir dicas** com base na palavra.
- Transformar o jogo em **API web** com FastAPI.

