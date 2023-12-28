from typing import Generic, TypeVar

import pulumi
import pulumi_azure_native as azure

from stratos_lib import configs as confs

TConfig = TypeVar("TConfig", bound=confs.VpcConfig)


def name(*suffixes: str) -> str:
    return "_".join(suffixes)


class VpcComponent(pulumi.ComponentResource, Generic[TConfig]):
    def __init__(
        self,
        config: TConfig,
        opts: pulumi.ResourceOptions | None = None,
    ):
        super().__init__("custom:azure:VpcComponent", config.name, None, opts)

        # Create a Resource Group
        self.resource_group = azure.resources.ResourceGroup(
            name(config.name, "resgroup")
        )

        # Create a new VPC
        self.vpc = azure.network.VirtualNetwork(
            name(config.name, "vpc"),
            resource_group_name=self.resource_group.name,
            address_space=azure.network.AddressSpaceArgs(
                address_prefixes=["10.0.0.0/16"],
            ),
            location=self.resource_group.location,
            tags=config.tags,
        )

        # Private Subnet with Internet access (via NAT Gateway for egress)
        self.nat_gateway = azure.network.NatGateway(
            name(config.name, "nat-gateway"),
            resource_group_name=self.resource_group.name,
            location=self.resource_group.location,
            sku=azure.network.NatGatewaySkuArgs(name="Standard"),
            public_ip_addresses=[
                azure.network.SubResourceArgs(
                    id=azure.network.PublicIPAddress(
                        name(config.name, "nat-gateway-ip"),
                        resource_group_name=self.resource_group.name,
                        location=self.resource_group.location,
                        sku=azure.network.PublicIPAddressSkuArgs(
                            name="Standard"
                        ),
                    ).id
                )
            ],
        )

        self.subnets = []
        for idx, subnet_config in enumerate(config.subnets):
            subnet_name = name(subnet_config.name, "subnet")

            nat_kwargs = {}
            if subnet_config.type == confs.SubnetType.ISOLATED:
                nat_kwargs["service_endpoints"] = []
            else:
                nat_kwargs["nat_gateway"] = azure.network.SubResourceArgs(
                    id=self.nat_gateway.id
                )

            # Create a public subnet
            subnet = azure.network.Subnet(
                subnet_name,
                resource_group_name=self.resource_group.name,
                virtual_network_name=self.vpc.name,
                address_prefix=f"10.0.{idx + 1}.0/24",
                tags=config.tags,
            )
            self.subnets.append(subnet)

            pulumi.export(f"{subnet_name}_id", subnet.id)

        pulumi.export("vpc_id", self.vpc.id)
        pulumi.export("resource_group_id", self.resource_group.id)
