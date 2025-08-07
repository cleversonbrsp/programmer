#!/usr/bin/env python3
"""
Script para remover tags "finops.customer: seduc-go" de todos os recursos na OCI.
"""

import oci
import click
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
import sys
from typing import List, Dict, Any
import time

console = Console()

class OCITagRemover:
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
                        "defined_tags": instance.defined_tags
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
                        "defined_tags": volume.defined_tags
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
                        "defined_tags": vcn.defined_tags
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
                        "defined_tags": subnet.defined_tags
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
                        "defined_tags": lb.defined_tags
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
                        "defined_tags": db.defined_tags
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

    def remove_tag_from_resource(self, resource: Dict[str, Any], tag_namespace: str = "finops", tag_key: str = "customer") -> bool:
        """Remove a tag específica de um recurso."""
        try:
            resource_type = resource["type"]
            resource_id = resource["id"]
            current_tags = resource["defined_tags"].copy()
            
            # Remove a tag específica
            if tag_namespace in current_tags and tag_key in current_tags[tag_namespace]:
                del current_tags[tag_namespace][tag_key]
                
                # Se o namespace ficou vazio, remove ele também
                if not current_tags[tag_namespace]:
                    del current_tags[tag_namespace]

            # Atualiza o recurso baseado no tipo
            if resource_type == "Instance":
                self.compute_client.update_instance(
                    instance_id=resource_id,
                    update_instance_details=oci.core.models.UpdateInstanceDetails(
                        defined_tags=current_tags
                    )
                )
            elif resource_type == "Volume":
                self.blockstorage_client.update_volume(
                    volume_id=resource_id,
                    update_volume_details=oci.core.models.UpdateVolumeDetails(
                        defined_tags=current_tags
                    )
                )
            elif resource_type == "VCN":
                self.network_client.update_vcn(
                    vcn_id=resource_id,
                    update_vcn_details=oci.core.models.UpdateVcnDetails(
                        defined_tags=current_tags
                    )
                )
            elif resource_type == "Subnet":
                self.network_client.update_subnet(
                    subnet_id=resource_id,
                    update_subnet_details=oci.core.models.UpdateSubnetDetails(
                        defined_tags=current_tags
                    )
                )
            elif resource_type == "Load Balancer":
                self.loadbalancer_client.update_load_balancer(
                    load_balancer_id=resource_id,
                    update_load_balancer_details=oci.core.models.UpdateLoadBalancerDetails(
                        defined_tags=current_tags
                    )
                )
            elif resource_type == "Database":
                self.database_client.update_database(
                    database_id=resource_id,
                    update_database_details=oci.database.models.UpdateDatabaseDetails(
                        defined_tags=current_tags
                    )
                )
            
            return True
        except Exception as e:
            console.print(f"[red]Erro ao remover tag de {resource_type} {resource['name']}: {e}[/red]")
            return False

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
    """Função principal."""
    console.print(Panel.fit(
        "[bold blue]Removedor de Tags OCI[/bold blue]\n"
        "Remove tags 'finops.customer: seduc-go' de todos os recursos",
        border_style="blue"
    ))

    # Inicializa o cliente OCI
    remover = OCITagRemover()
    
    # Obtém todos os compartimentos
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
        task = progress.add_task("Buscando compartimentos...", total=None)
        compartments = remover.get_compartments()
        progress.update(task, description="Compartimentos encontrados")

    if not compartments:
        console.print("[red]Nenhum compartimento encontrado ou erro na conexão.[/red]")
        return

    total_resources = []
    all_resources = []

    # Busca recursos em todos os compartimentos
    for compartment in compartments:
        console.print(f"\n[bold]Analisando compartimento: {compartment['name']}[/bold]")
        
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
            task = progress.add_task(f"Buscando recursos em {compartment['name']}...", total=None)
            resources = remover.find_resources_with_tag(compartment['id'])
            progress.update(task, description=f"Encontrados {len(resources)} recursos")

        if resources:
            remover.display_resources_table(resources, compartment['name'])
            all_resources.extend(resources)
            total_resources.extend(resources)

    if not total_resources:
        console.print("\n[green]✓[/green] Nenhum recurso com a tag 'finops.customer: seduc-go' foi encontrado.")
        return

    # Confirma a remoção
    console.print(f"\n[bold red]ATENÇÃO:[/bold red] Encontrados {len(total_resources)} recursos com a tag 'finops.customer: seduc-go'")
    
    if not click.confirm("Deseja continuar e remover essas tags?"):
        console.print("[yellow]Operação cancelada pelo usuário.[/yellow]")
        return

    # Remove as tags
    console.print("\n[bold]Removendo tags...[/bold]")
    success_count = 0
    error_count = 0

    with Progress() as progress:
        task = progress.add_task("Removendo tags...", total=len(total_resources))
        
        for resource in total_resources:
            if remover.remove_tag_from_resource(resource):
                success_count += 1
                progress.update(task, description=f"✓ {resource['type']} {resource['name']}")
            else:
                error_count += 1
                progress.update(task, description=f"✗ {resource['type']} {resource['name']}")
            
            progress.advance(task)
            time.sleep(0.1)  # Pequena pausa para não sobrecarregar a API

    # Resumo final
    console.print(f"\n[bold]Resumo da operação:[/bold]")
    console.print(f"[green]✓ Sucessos: {success_count}[/green]")
    if error_count > 0:
        console.print(f"[red]✗ Erros: {error_count}[/red]")
    
    console.print(f"\n[green]Operação concluída![/green]")

if __name__ == "__main__":
    main() 