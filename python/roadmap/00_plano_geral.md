## Roadmap de Estudos – Desenvolvedor Python (IA / LLM)

Este roadmap foi pensado para levar você de **iniciante em Python** até um nível **Pleno focado em IA e LLMs**, alinhado com a vaga descrita (Python, LLM/RAG, LangChain/LlamaIndex/CrewAI, integrações com APIs e contexto corporativo).

### Objetivo Geral

- **Sair do zero em Python** até:
  - Conseguir **desenvolver e manter aplicações em Python** (CLIs, APIs, automações).
  - Ter base sólida de **Git, Linux, ambiente virtual, boas práticas**.
  - Entender **fundamentos de Machine Learning**.
  - Conseguir **trabalhar com LLMs na prática** (chamadas de API, prompts, embeddings, RAG).
  - Utilizar **LangChain, LlamaIndex e CrewAI** para montar pipelines e agentes.
  - Ter um **projeto final consistente** para portfólio e entrevistas.

### Perfil da Vaga-Alvo

- **Python nível Pleno**: domínio da linguagem, módulos padrão, testes, pacotes, ambientes virtuais.
- **LLMs e RAG**: saber:
  - Chamar modelos via API.
  - Criar **prompts eficazes**.
  - Trabalhar com **embeddings**, **bases de conhecimento** e **arquiteturas RAG**.
- **Ferramentas de orquestração**:
  - LangChain, LlamaIndex, CrewAI ou similares.
- **Integrações corporativas**:
  - Consumo de APIs REST.
  - Integração com serviços externos.
  - Organização de projeto, logs, configuração, segurança básica (tokens, .env).

---

## Estrutura das Fases

### Fase 01 – Python Básico (`01_python_basico/`)

**Objetivo**: Sair do zero e aprender a programar em Python com foco em lógica, estruturas de dados básicas e entrada/saída. Ao final desta fase você deve:

- Entender **tipos básicos**, **condicionais**, **loops**, **funções** e **listas/dicionários**.
- Conseguir escrever pequenos programas de linha de comando.
- Ter contato inicial com **leitura e gravação de arquivos**.

**Arquivos**:
- `apostila_python_basico.md`: teoria + exemplos.
- `lab01_calculadora_cli.md`: criar uma calculadora via terminal.
- `lab02_jogo_forca.md`: implementar um jogo da forca simples.
- `lab03_mini_agenda_arquivos.md`: mini agenda que lê/escreve em arquivos.

### Fase 02 – Python Intermediário e Backend (`02_python_intermediario_backend/`)

**Objetivo**: Evoluir para um uso mais profissional de Python, começando a construir **APIs** e **scripts de automação**. Ao final desta fase você deve:

- Entender **módulos**, **pacotes**, **ambientes virtuais** (aqui prévia, aprofundada na fase 03).
- Usar bibliotecas externas via `pip`.
- Criar uma **API REST simples com FastAPI**.
- Escrever CLIs que automatizam rotinas do dia a dia.

**Arquivos**:
- `apostila_python_intermediario.md`
- `lab01_api_fastapi_tarefas.md`
- `lab02_cli_automatizar_rotinas.md`

### Fase 03 – Git, Linux e Boas Práticas Profissionais (`03_git_linux_boas_praticas/`)

**Objetivo**: Preparar você para um ambiente de trabalho real, com uso de **Git**, **Linux** e **gestão de ambientes/projetos**. Ao final desta fase você deve:

- Entender o **fluxo básico de Git** (clone, branch, commit, push, pull, PR).
- Usar Linux para tarefas comuns de desenvolvimento.
- Criar e gerenciar **ambientes virtuais** com `venv` e **Poetry**.
- Conhecer **boas práticas de organização de projeto** (estrutura de pastas, configuração, .env).

**Arquivos**:
- `apostila_ferramentas_profissionais.md`
- `lab01_fluxo_git_basico.md`
- `lab02_ambiente_virtual_poetry.md`

### Fase 04 – Fundamentos de Machine Learning (`04_ml_fundamentos/`)

**Objetivo**: Dar a base mínima de ML para entender melhor como LLMs se encaixam no ecossistema de IA e como trabalhar com dados. Ao final desta fase você deve:

- Entender conceitos como **dataset**, **treino/teste**, **overfitting**, **métrica**.
+- Utilizar **scikit-learn** para modelos simples.
- Treinar e avaliar uma **regressão linear**.
- Criar um **classificador simples**, como filtro de spam.

**Arquivos**:
- `apostila_ml_fundamentos.md`
- `lab01_regressao_linear_sklearn.md`
- `lab02_classificador_spam.md`

### Fase 05 – LLMs e Arquiteturas RAG (`05_llm_e_rag/`)

**Objetivo**: Entrar no mundo de **LLMs na prática**, entendendo chamadas de API, prompts, embeddings e a arquitetura RAG. Ao final desta fase você deve:

- Conseguir chamar um modelo LLM via API (OpenAI, Gemini, ou outro).
- Entender o que é **token**, **contexto**, **prompt**, **temperature**.
- Compreender e implementar um fluxo básico de **RAG**:
  - Ingestão de documentos.
  - Criação de embeddings.
  - Busca semântica.
  - Montagem do contexto no prompt.

**Arquivos**:
- `apostila_llm_rag.md`
- `lab01_chatbot_basico_api_llm.md`
- `lab02_rag_com_langchain.md`
- `lab03_rag_com_llamaindex.md`

### Fase 06 – Orquestração e Multiagentes (`06_orquestracao_e_multi_agentes/`)

**Objetivo**: Desenvolver fluência em **LangChain**, **LlamaIndex** e **CrewAI**, criando pipelines de IA e agentes especializados. Ao final desta fase você deve:

- Saber criar **chains** com LangChain (prompt → LLM → parsing → ferramenta).
- Montar índices e rotas de consulta com **LlamaIndex**.
- Criar **agentes e times de agentes** com CrewAI (por exemplo, agente pesquisador).

**Arquivos**:
- `apostila_langchain_llamaindex_crewai.md`
- `lab01_pipeline_langchain.md`
- `lab02_crewai_agente_pesquisador.md`

### Fase 07 – Projeto Final e Entrevista (`07_projeto_final/`)

**Objetivo**: Consolidar tudo em um **projeto completo**, próximo ao tipo de solução que você encontraria na vaga, e se preparar para processos seletivos.

Ao final desta fase você deve:

- Ter um **projeto de IA/LLM com RAG** rodando (preferencialmente com API ou interface simples).
- Integrar o projeto com **alguma API externa** (busca, CRM fictício, ferramenta de produtividade etc.).
- Ter um **repositório organizado no GitHub**, com README e instruções de uso.
- Ter um **checklist de entrevista** para revisar antes de falar com recrutadores e gestores.

**Arquivos**:
- `guia_projeto_final.md`
- `checklist_entrevista_vaga.md`

---

## Como Estudar este Roadmap

- **Ordem recomendada**: seguir as fases na ordem (01 → 07), mas você pode acelerar as fases iniciais se já tiver noções de lógica.
- **Ritmo sugerido** (trabalhando ou estudando em paralelo):
  - 8–12 semanas para sair de iniciante a Python intermediário/backend.
  - 4–6 semanas para ML + LLMs/RAG.
  - 2–4 semanas para orquestração + projeto final.
- **Estilo de estudo**:
  - Leia a **apostila** da fase.
  - Faça todos os **labs** no mínimo nível de requisitos.
  - Pegue ao menos uma **extensão/desafio extra** por fase.

---

## Conexão Direta com a Vaga

- **Desenvolver e manter aplicações em Python**  
  - Fases 01, 02 e 03 preparam você para isso (CLIs, APIs, ferramentas, boas práticas).

- **Integrar e ajustar modelos LLM (RAG, fine-tuning, embeddings)**  
  - Fases 04, 05 e 06 focam nesse ponto (fundamentos de ML, LLMs, RAG, LangChain, LlamaIndex, CrewAI).

- **Estruturar e otimizar prompts e bases de conhecimento**  
  - Fase 05 (LLM/RAG) e 06 (orquestração) cobrem prompting, embeddings e estratégias de chunking/consulta.

- **Integrar IA com sistemas legados e APIs corporativas**  
  - Fase 02 (API com FastAPI, automações) + Fase 05/06 (integração de LLMs com APIs).

- **Ambiente corporativo**  
  - Fase 03 (Git, Linux, Poetry, boas práticas) + Fase 07 (projeto final e checklist de entrevista).

