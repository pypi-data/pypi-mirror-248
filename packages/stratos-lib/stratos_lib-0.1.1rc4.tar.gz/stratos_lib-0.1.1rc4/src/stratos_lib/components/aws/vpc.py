from typing import Generic, TypeVar

import pulumi
import pulumi_aws as aws

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
        super().__init__("custom:aws:VpcComponent", config.name, None, opts)

        # Create a new VPC
        self.vpc = aws.ec2.Vpc(
            name(config.name, "vpc"),
            cidr_block="10.0.0.0/16",
            enable_dns_hostnames=True,
            enable_dns_support=True,
            tags=config.tags,
        )

        # Create an Internet Gateway for the VPC
        self.nat_gateway = aws.ec2.InternetGateway(
            "vpc_igw",
            vpc_id=self.vpc.id,
            tags=config.tags,
        )

        # Create an egress only internet gateway for the private subnet
        self.egress_only_igw = aws.ec2.EgressOnlyInternetGateway(
            "egress_only_igw",
            vpc_id=self.vpc.id,
            tags=config.tags,
        )

        # Create a route table for public subnet
        # with default route to Internet Gateway
        self.public_route_table = aws.ec2.RouteTable(
            "public_route_table",
            vpc_id=self.vpc.id,
            routes=[
                aws.ec2.RouteTableRouteArgs(
                    cidr_block="0.0.0.0/0",
                    gateway_id=self.nat_gateway.id,
                )
            ],
            tags=config.tags,
        )

        # Create a route table for private subnet
        # with default route to egress only gateway
        self.private_route_table = aws.ec2.RouteTable(
            "private_route_table",
            vpc_id=self.vpc.id,
            routes=[
                aws.ec2.RouteTableRouteArgs(
                    ipv6_cidr_block="::/0",
                    egress_only_gateway_id=self.egress_only_igw.id,
                )
            ],
            tags=config.tags,
        )

        self.subnets = []
        for idx, subnet_config in enumerate(config.subnets):
            for az in range(config.max_azs):
                zone = chr(ord("a") + az)
                subnet_name = name(subnet_config.name, "subnet", zone)
                # Create a public subnet
                subnet = aws.ec2.Subnet(
                    subnet_name,
                    vpc_id=self.vpc.id,
                    cidr_block=f"10.0.{idx + 1}.0/24",
                    availability_zone=f"{config.region}{zone}",
                    tags=config.tags,
                )
                self.subnets.append(subnet)

                pulumi.export(f"{subnet_name}_id", subnet.id)

                # For isolated subnets, we skip route table configuration
                if subnet_config.type == confs.SubnetType.ISOLATED:
                    continue

                if subnet_config.type == confs.SubnetType.PUBLIC:
                    route_table_id = self.public_route_table.id
                else:
                    route_table_id = self.private_route_table.id

                aws.ec2.RouteTableAssociation(
                    name(subnet_name, "rt", "assoc"),
                    subnet_id=subnet.id,
                    route_table_id=route_table_id,
                )

        # Export the VPC and Subnets IDs
        pulumi.export("vpc_id", self.vpc.id)
