## Lab 02 – CLI para Automatizar Rotinas em Python

### 1. Objetivo

Criar uma **ferramenta de linha de comando (CLI)** em Python para automatizar uma rotina simples, por exemplo:

- Organizar arquivos em pastas.
- Fazer backup de um diretório.
- Processar arquivos de texto (ex.: contar linhas, palavras, etc.).

Você vai praticar:

- Uso do módulo `argparse` ou semelhante.
- Leitura de arquivos e diretórios.
- Organização de código em funções.
- Boas práticas para CLIs que podem ser usados em projetos de dados e IA.

---

### 2. Descrição do Problema (Sugestão)

Escolha **uma** das ideias abaixo (ou defina a sua) para implementar em um arquivo `cli_rotina.py`:

- **Organizador de arquivos**:
  - Dado um diretório, mover arquivos para subpastas por extensão (`.txt`, `.csv`, `.jpg`, etc.).

- **Backup simples**:
  - Copiar todos os arquivos de um diretório para outro, opcionalmente comprimindo em `.zip`.

- **Processador de textos**:
  - Dado um arquivo ou diretório, contar:
    - Número de arquivos.
    - Número total de linhas.
    - Palavras mais frequentes.

O foco não é a funcionalidade exata, mas sim a estrutura da CLI.

---

### 3. Requisitos Mínimos

- Arquivo principal: `cli_rotina.py`.
- Utilizar `argparse` para:
  - Definir pelo menos **um argumento obrigatório** (por exemplo, `--entrada` ou `--origem`).
  - Opcionalmente, um argumento opcional (por exemplo, `--destino` ou `--extensao`).
- Tratar erros básicos, como:
  - Diretório inexistente.
  - Arquivo inexistente.
- Exibir mensagens claras no terminal sobre o que está sendo feito.

---

### 4. Passos Sugeridos

1. **Criar esqueleto da CLI com `argparse`**

   ```python
   import argparse


   def main():
       parser = argparse.ArgumentParser(description="CLI para automatizar rotinas")
       parser.add_argument("--origem", required=True, help="Diretório ou arquivo de origem")
       args = parser.parse_args()

       print("Origem recebida:", args.origem)


   if __name__ == "__main__":
       main()
   ```

2. **Definir claramente a rotina automatizada**

   - Exemplo: organizar arquivos em pastas por extensão.
   - Desenhar o fluxo em texto antes de codar.

3. **Implementar funções auxiliares**

   - Por exemplo:
     - `listar_arquivos(diretorio)`
     - `mover_arquivo(origem, destino)`
     - `criar_pasta_se_nao_existir(caminho)`

4. **Implementar a lógica principal**

   - Com base nos argumentos recebidos, chamar as funções auxiliares.

5. **Testar pelo terminal**

   - Exemplo:

   ```bash
   python cli_rotina.py --origem ./entrada
   ```

---

### 5. Sugestão de Estrutura para “Organizador de Arquivos”

Se você escolher essa opção:

- Entrada: diretório de origem (`--origem`).
- Saída: subpastas dentro de `--origem` por extensão de arquivo.

Exemplo:

```text
entrada/
  ├── foto1.jpg
  ├── foto2.png
  ├── texto1.txt
  └── planilha1.csv
```

Resultado:

```text
entrada/
  ├── imagens/
  │   ├── foto1.jpg
  │   └── foto2.png
  ├── textos/
  │   └── texto1.txt
  └── planilhas/
      └── planilha1.csv
```

---

### 6. Extensões (Desafios Extras)

- **Desafio 1 – Múltiplos subcomandos**
  - Usar `argparse` com subparsers para algo como:

  ```bash
  python cli_rotina.py organizar --origem ./entrada
  python cli_rotina.py backup --origem ./entrada --destino ./backup
  ```

- **Desafio 2 – Logs em arquivo**
  - Usar o módulo `logging` para registrar as operações realizadas em um arquivo de log.

- **Desafio 3 – Configuração por arquivo `.ini` ou `.yaml`**
  - Permitir que a CLI leia um arquivo de configuração com parâmetros padrão.

- **Desafio 4 – Transformar em pacote instalável**
  - Estruturar como um pacote Python com `setup.cfg`/`pyproject.toml` e um entrypoint de console.

---

### 7. Conexão com Projetos de IA/LLM

CLIs desse tipo são extremamente úteis em projetos de IA:

- Automatizar:
  - Coleta e organização de documentos que serão indexados em um sistema de RAG.
  - Pré-processamento de textos antes de criar embeddings.
  - Geração de relatórios ou estatísticas sobre dados de entrada de modelos.

Com esse lab, você dá um passo em direção a construir **ferramentas internas** que facilitam o dia a dia de um time de IA, algo muito valorizado em perfis plenos.

