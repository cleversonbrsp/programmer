#!/usr/bin/env python3
"""
Script para modo DRY-RUN - apenas lista recursos com tags "finops.customer: seduc-go" sem fazer alterações.
"""

import oci
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
import sys
from typing import List, Dict, Any

console = Console()

class OCITagScanner:
    def __init__(self, config_path: str = "~/.oci/config"):
        """Inicializa o cliente OCI com configuração."""
        try:
            self.config = oci.config.from_file(config_path)
            self.identity_client = oci.identity.IdentityClient(self.config)
            self.compute_client = oci.core.ComputeClient(self.config)
            self.network_client = oci.core.VirtualNetworkClient(self.config)
            self.blockstorage_client = oci.core.BlockstorageClient(self.config)
            self.database_client = oci.database.DatabaseClient(self.config)
            self.loadbalancer_client = oci.load_balancer.LoadBalancerClient(self.config)
            self.objectstorage_client = oci.object_storage.ObjectStorageClient(self.config)
            console.print(f"[green]✓[/green] Conectado à OCI usando configuração: {config_path}")
        except Exception as e:
            console.print(f"[red]✗[/red] Erro ao conectar à OCI: {e}")
            sys.exit(1)

    def get_compartments(self) -> List[Dict[str, Any]]:
        """Obtém todos os compartimentos acessíveis."""
        try:
            response = self.identity_client.list_compartments(
                compartment_id=self.config['tenancy'],
                access_level="ACCESSIBLE"
            )
            compartments = [{"id": self.config['tenancy'], "name": "Root Compartment"}] + [
                {"id": comp.id, "name": comp.name} for comp in response.data
            ]
            return compartments
        except Exception as e:
            console.print(f"[red]Erro ao listar compartimentos: {e}[/red]")
            return []

    def find_resources_with_tag(self, compartment_id: str, tag_namespace: str = "finops", tag_key: str = "customer", tag_value: str = "seduc-go") -> List[Dict[str, Any]]:
        """Encontra todos os recursos com a tag específica."""
        resources = []
        
        # Instâncias de computação
        try:
            instances = self.compute_client.list_instances(compartment_id=compartment_id).data
            for instance in instances:
                if self._has_target_tag(instance.defined_tags, tag_namespace, tag_key, tag_value):
                    resources.append({
                        "type": "Instance",
                        "id": instance.id,
                        "name": instance.display_name,
                        "lifecycle_state": instance.lifecycle_state,
                        "compartment_id": compartment_id
                    })
        except Exception as e:
            console.print(f"[yellow]Aviso: Erro ao listar instâncias: {e}[/yellow]")

        # Volumes de bloco
        try:
            volumes = self.blockstorage_client.list_volumes(compartment_id=compartment_id).data
            for volume in volumes:
                if self._has_target_tag(volume.defined_tags, tag_namespace, tag_key, tag_value):
                    resources.append({
                        "type": "Volume",
                        "id": volume.id,
                        "name": volume.display_name,
                        "lifecycle_state": volume.lifecycle_state,
                        "compartment_id": compartment_id
                    })
        except Exception as e:
            console.print(f"[yellow]Aviso: Erro ao listar volumes: {e}[/yellow]")

        # VCNs
        try:
            vcns = self.network_client.list_vcns(compartment_id=compartment_id).data
            for vcn in vcns:
                if self._has_target_tag(vcn.defined_tags, tag_namespace, tag_key, tag_value):
                    resources.append({
                        "type": "VCN",
                        "id": vcn.id,
                        "name": vcn.display_name,
                        "lifecycle_state": vcn.lifecycle_state,
                        "compartment_id": compartment_id
                    })
        except Exception as e:
            console.print(f"[yellow]Aviso: Erro ao listar VCNs: {e}[/yellow]")

        # Subnets
        try:
            subnets = self.network_client.list_subnets(compartment_id=compartment_id).data
            for subnet in subnets:
                if self._has_target_tag(subnet.defined_tags, tag_namespace, tag_key, tag_value):
                    resources.append({
                        "type": "Subnet",
                        "id": subnet.id,
                        "name": subnet.display_name,
                        "lifecycle_state": subnet.lifecycle_state,
                        "compartment_id": compartment_id
                    })
        except Exception as e:
            console.print(f"[yellow]Aviso: Erro ao listar subnets: {e}[/yellow]")

        # Load Balancers
        try:
            load_balancers = self.loadbalancer_client.list_load_balancers(compartment_id=compartment_id).data
            for lb in load_balancers:
                if self._has_target_tag(lb.defined_tags, tag_namespace, tag_key, tag_value):
                    resources.append({
                        "type": "Load Balancer",
                        "id": lb.id,
                        "name": lb.display_name,
                        "lifecycle_state": lb.lifecycle_state,
                        "compartment_id": compartment_id
                    })
        except Exception as e:
            console.print(f"[yellow]Aviso: Erro ao listar load balancers: {e}[/yellow]")

        # Databases
        try:
            databases = self.database_client.list_databases(compartment_id=compartment_id).data
            for db in databases:
                if self._has_target_tag(db.defined_tags, tag_namespace, tag_key, tag_value):
                    resources.append({
                        "type": "Database",
                        "id": db.id,
                        "name": db.db_name,
                        "lifecycle_state": db.lifecycle_state,
                        "compartment_id": compartment_id
                    })
        except Exception as e:
            console.print(f"[yellow]Aviso: Erro ao listar databases: {e}[/yellow]")

        return resources

    def _has_target_tag(self, defined_tags: Dict, namespace: str, key: str, value: str) -> bool:
        """Verifica se o recurso tem a tag específica."""
        if not defined_tags:
            return False
        return (namespace in defined_tags and 
                key in defined_tags[namespace] and 
                defined_tags[namespace][key] == value)

    def display_resources_table(self, resources: List[Dict[str, Any]], compartment_name: str):
        """Exibe uma tabela com os recursos encontrados."""
        if not resources:
            console.print(f"[yellow]Nenhum recurso com a tag 'finops.customer: seduc-go' encontrado no compartimento '{compartment_name}'[/yellow]")
            return

        table = Table(title=f"Recursos com tag 'finops.customer: seduc-go' - Compartimento: {compartment_name}")
        table.add_column("Tipo", style="cyan")
        table.add_column("Nome", style="green")
        table.add_column("ID", style="blue")
        table.add_column("Estado", style="yellow")

        for resource in resources:
            table.add_row(
                resource["type"],
                resource["name"],
                resource["id"],
                resource["lifecycle_state"]
            )

        console.print(table)

def main():
    """Função principal - modo DRY-RUN."""
    console.print(Panel.fit(
        "[bold yellow]Scanner de Tags OCI - MODO DRY-RUN[/bold yellow]\n"
        "Lista recursos com tags 'finops.customer: seduc-go' sem fazer alterações",
        border_style="yellow"
    ))

    # Inicializa o scanner OCI
    scanner = OCITagScanner()
    
    # Obtém todos os compartimentos
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
        task = progress.add_task("Buscando compartimentos...", total=None)
        compartments = scanner.get_compartments()
        progress.update(task, description="Compartimentos encontrados")

    if not compartments:
        console.print("[red]Nenhum compartimento encontrado ou erro na conexão.[/red]")
        return

    total_resources = []
    compartment_resources = {}

    # Busca recursos em todos os compartimentos
    for compartment in compartments:
        console.print(f"\n[bold]Analisando compartimento: {compartment['name']}[/bold]")
        
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
            task = progress.add_task(f"Buscando recursos em {compartment['name']}...", total=None)
            resources = scanner.find_resources_with_tag(compartment['id'])
            progress.update(task, description=f"Encontrados {len(resources)} recursos")

        if resources:
            scanner.display_resources_table(resources, compartment['name'])
            total_resources.extend(resources)
            compartment_resources[compartment['name']] = resources

    # Resumo final
    console.print(f"\n[bold]Resumo da análise (DRY-RUN):[/bold]")
    console.print(f"[blue]Total de compartimentos analisados: {len(compartments)}[/blue]")
    console.print(f"[red]Total de recursos com tag 'finops.customer: seduc-go': {len(total_resources)}[/red]")
    
    if total_resources:
        console.print(f"\n[bold]Distribuição por compartimento:[/bold]")
        for comp_name, resources in compartment_resources.items():
            if resources:
                console.print(f"  • {comp_name}: {len(resources)} recursos")
        
        console.print(f"\n[yellow]Para remover essas tags, execute: python delete_tags.py[/yellow]")
    else:
        console.print(f"\n[green]✓[/green] Nenhum recurso com a tag 'finops.customer: seduc-go' foi encontrado.")

if __name__ == "__main__":
    main() 