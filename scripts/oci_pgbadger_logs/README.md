# PGBadger Logs Analyzer - Oracle Cloud Infrastructure

## 📋 Descrição

Este script automatiza a análise de logs PostgreSQL armazenados no Oracle Cloud Infrastructure (OCI) Object Storage. Ele busca, baixa e processa logs de banco de dados PostgreSQL em um intervalo de tempo específico, gerando relatórios HTML detalhados usando o PGBadger.

### 🎯 Funcionalidades

- **Busca Inteligente**: Localiza logs PostgreSQL no OCI Object Storage baseado em intervalo de tempo
- **Download Automatizado**: Baixa e descompacta arquivos `.gz` automaticamente
- **Análise Unificada**: Processa múltiplos logs e gera um relatório consolidado
- **Suporte Multi-Ambiente**: Configuração para múltiplos ambientes de banco de dados
- **Integração CI/CD**: Pipeline GitHub Actions para execução automatizada

## 🛠️ Requisitos

### Dependências Python
```bash
pip install oci
```

### Dependências do Sistema
```bash
sudo apt update
sudo apt install -y pgbadger
```

### Configuração OCI
O script utiliza as seguintes variáveis de ambiente para autenticação OCI:
- `OCI_CLI_USER` - ID do usuário OCI
- `OCI_CLI_TENANCY` - ID do tenancy OCI
- `OCI_CLI_FINGERPRINT` - Fingerprint da chave API
- `OCI_CLI_KEY_CONTENT` - Conteúdo da chave privada
- `OCI_CLI_REGION` - Região OCI

### Configuração do Script
As seguintes variáveis de ambiente são necessárias para execução:
- `PG_ENV` - Chave do ambiente (0, 1, 2, ou 3)
- `PG_START` - Data/hora de início (formato: YYYY-MM-DD HH:MM UTC)
- `PG_END` - Data/hora de fim (formato: YYYY-MM-DD HH:MM UTC)

## 🚀 Como Usar

### Execução Local

1. **Configure as variáveis de ambiente:**
```bash
export PG_ENV=1
export PG_START="2025-06-18 04:00"
export PG_END="2025-06-18 05:00"
```

2. **Execute o script:**
```bash
python3 pgbadger_logs.py
```

### Execução via GitHub Actions

O projeto inclui um pipeline automatizado (`pipeline.yml`) que pode ser executado via GitHub Actions:

1. Configure os secrets do repositório com as credenciais OCI
2. Acesse a aba "Actions" no GitHub
3. Execute o workflow "Logs PostgreSQL com PGBadger"
4. Configure os parâmetros de entrada:
   - **Environment**: Escolha o ambiente (0-3)
   - **Start Datetime**: Data/hora de início (UTC)
   - **End Datetime**: Data/hora de fim (UTC)

## 📁 Estrutura de Arquivos

```
scripts/oci_pgbadger_logs/
├── pgbadger_logs.py    # Script principal
├── pipeline.yml        # Pipeline GitHub Actions
├── README.md          # Este arquivo
```

## ⚙️ Configuração de Ambientes

O script suporta múltiplos ambientes configurados no dicionário `ENVIRONMENTS`:

```python
ENVIRONMENTS = {
    "0": {
        "name": "nome-do-ambiente-0",
        "bucket": "nome-do-bucket-0",
        "namespace": "nome-do-namespace",
        "folder": "nome-do-folder(normalmente o OCID do DB System)",
        "subfolder": "nome-do-subfolder(normalmente um UUID sistemico)"
    },
    # ... outros ambientes
}
```

## 📊 Saída

O script gera relatórios HTML do PGBadger contendo:
- Estatísticas de performance do banco
- Análise de queries lentas
- Métricas de conexões e sessões
- Relatórios de erros e warnings
- Gráficos e visualizações

Os relatórios são salvos em:
- **Local**: `/tmp/pgbadger`
- **GitHub Actions**: Artefatos do workflow

## 🔧 Personalização

### Modificar Configurações de Ambiente
Edite o dicionário `ENVIRONMENTS` no início do arquivo `pgbadger_logs.py` para adicionar ou modificar ambientes.

### Alterar Diretório de Saída
Modifique a variável `output_dir` na função `main()` para alterar onde os relatórios são salvos.

### Ajustar Parâmetros do PGBadger
Modifique a lista `pgbadger_cmd` na função `main()` para adicionar parâmetros específicos do PGBadger.

## 🐛 Troubleshooting

### Problemas Comuns

1. **Erro de autenticação OCI**
   - Verifique se todas as variáveis de ambiente OCI estão configuradas
   - Confirme se o arquivo de configuração OCI está correto

2. **PGBadger não encontrado**
   - Execute: `sudo apt install -y pgbadger`
   - Verifique se o PGBadger está no PATH

3. **Nenhum log encontrado**
   - Confirme se o intervalo de tempo está correto
   - Verifique se os logs existem no bucket especificado

### Logs de Debug
O script exibe informações detalhadas durante a execução:
- Número de objetos encontrados por página
- Tempo de execução das operações
- Caminhos dos arquivos processados

## 📝 Licença

Este projeto é parte do repositório pessoal de scripts de programação.

## 🤝 Contribuição

Para contribuir com melhorias:
1. Faça um fork do repositório
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Abra um Pull Request

---

**Desenvolvido para análise automatizada de logs PostgreSQL na Oracle Cloud Infrastructure**