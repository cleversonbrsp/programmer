# Removedor de Tags OCI

Automação em Python para remover tags "finops.customer: seduc-go" de todos os recursos na Oracle Cloud Infrastructure (OCI).

## Funcionalidades

- 🔍 **Scanner de recursos**: Encontra todos os recursos com a tag específica
- 🛡️ **Modo Dry-Run**: Visualiza recursos sem fazer alterações
- 🗑️ **Remoção segura**: Remove tags com confirmação do usuário
- 📊 **Interface rica**: Interface colorida com barras de progresso
- 🔧 **Múltiplos tipos**: Suporta instâncias, volumes, VCNs, subnets, load balancers e databases

## Pré-requisitos

1. **Python 3.7+**
2. **SDK da Oracle Cloud Infrastructure**
3. **Configuração OCI**: Arquivo `~/.oci/config` configurado

## Instalação

```bash
cd delete-tags-oci
pip install -r requirements.txt
```

## Uso

### 1. Modo Dry-Run (Recomendado primeiro)

Execute para visualizar quais recursos serão afetados **sem fazer alterações**:

```bash
python dry_run.py
```

### 2. Remoção de Tags

Após confirmar os recursos no dry-run, execute para remover as tags:

```bash
python delete_tags.py
```

O script irá:
1. Listar todos os compartimentos acessíveis
2. Buscar recursos com a tag "finops.customer: seduc-go"
3. Exibir uma tabela com os recursos encontrados
4. Pedir confirmação antes de remover as tags
5. Executar a remoção com barra de progresso
6. Mostrar resumo final

## Tipos de Recursos Suportados

- ✅ Instâncias de Computação
- ✅ Volumes de Bloco
- ✅ VCNs (Virtual Cloud Networks)
- ✅ Subnets
- ✅ Load Balancers
- ✅ Databases

## Configuração OCI

Certifique-se de que o arquivo `~/.oci/config` está configurado corretamente:

```ini
[DEFAULT]
user=ocid1.user.oc1..aaaaaaaaxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
fingerprint=xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx:xx
key_file=~/.oci/oci_api_key.pem
tenancy=ocid1.tenancy.oc1..aaaaaaaaxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
region=us-ashburn-1
```

## Segurança

- ⚠️ **Sempre execute o dry-run primeiro**
- ⚠️ **Confirme os recursos antes da remoção**
- ⚠️ **Verifique as permissões OCI necessárias**
- ⚠️ **Faça backup se necessário**

## Permissões OCI Necessárias

O usuário precisa das seguintes permissões:
- `COMPARTMENT_READ` para listar compartimentos
- `INSTANCE_READ`, `INSTANCE_UPDATE` para instâncias
- `VOLUME_READ`, `VOLUME_UPDATE` para volumes
- `VCN_READ`, `VCN_UPDATE` para VCNs
- `SUBNET_READ`, `SUBNET_UPDATE` para subnets
- `LOAD_BALANCER_READ`, `LOAD_BALANCER_UPDATE` para load balancers
- `DATABASE_READ`, `DATABASE_UPDATE` para databases

## Exemplo de Saída

```
╭─ Removedor de Tags OCI ─╮
│ Remove tags 'finops.customer: seduc-go' de todos os recursos │
╰───────────────────────────────────────────────────────────────╯

✓ Conectado à OCI usando configuração: ~/.oci/config

Analisando compartimento: Root Compartment

┌─ Recursos com tag 'finops.customer: seduc-go' - Compartimento: Root Compartment ─┐
│ Tipo        │ Nome           │ ID                    │ Estado    │
│ Instance    │ web-server-01  │ ocid1.instance.oc1.. │ RUNNING   │
│ Volume      │ data-volume-01 │ ocid1.volume.oc1..   │ AVAILABLE │
└──────────────────────────────────────────────────────────────────────────────────┘

ATENÇÃO: Encontrados 2 recursos com a tag 'finops.customer: seduc-go'
Deseja continuar e remover essas tags? [y/N]: y

Removendo tags...
✓ Instance web-server-01
✓ Volume data-volume-01

Resumo da operação:
✓ Sucessos: 2
✗ Erros: 0

Operação concluída!
```

## Troubleshooting

### Erro de conexão
- Verifique se o arquivo `~/.oci/config` existe e está correto
- Confirme se as credenciais são válidas

### Erro de permissão
- Verifique se o usuário tem as permissões necessárias
- Confirme se o fingerprint da chave está correto

### Recursos não encontrados
- Verifique se a tag está no formato correto: `finops.customer: seduc-go`
- Confirme se os recursos estão em compartimentos acessíveis

## Contribuição

Para adicionar suporte a novos tipos de recursos, edite a função `find_resources_with_tag()` nos scripts. 