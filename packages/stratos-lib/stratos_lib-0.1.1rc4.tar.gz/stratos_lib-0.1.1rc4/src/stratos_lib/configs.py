import os
from enum import Enum, unique

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

SETTINGS_CONFIG = SettingsConfigDict(
    case_sensitive=False,
    env_file=os.environ.get("ENVFILE", ".env"),
    env_file_encoding="utf-8",
    env_nested_delimiter="__",
)


@unique
class SubnetType(Enum):
    PUBLIC = "PUBLIC"
    PRIVATE = "PRIVATE"
    ISOLATED = "ISOLATED"


@unique
class ContainerImageSource(Enum):
    ECR = "ECR"
    REGISTRY = "REGISTRY"


class IngressConfig(BaseSettings):
    security_group_id: str
    port: int


class SecretConfig(BaseSettings):
    name: str
    region: str


class DomainConfig(BaseSettings):
    domain: str
    subdomain: str | None = None
    private_zone: bool = False
    create_zone: bool = True

    @property
    def name(self):
        if not self.subdomain:
            return self.domain

        return f"{self.subdomain}.{self.domain}"


# class Ec2Config(BaseSettings):
#     size: ec2.InstanceSize
#     type_: ec2.InstanceClass


class ScalingConfig(BaseSettings):
    max_task_count: int = 2
    target_cpu_util_pct: float | int = 65


class VolumeConfig(BaseSettings):
    path: str
    filesys_id: str | None = None


class ContainerConfig(BaseSettings):
    port: int
    image: str
    tag: str = "latest"
    source: ContainerImageSource = ContainerImageSource.REGISTRY
    volumes: list[VolumeConfig] = Field(default_factory=list)
    command: str | None = None


class SubnetConfig(BaseSettings):
    name: str
    type: SubnetType
    cidr_mask: int = 24

    @classmethod
    def vpc_defaults(cls) -> list["SubnetConfig"]:
        return [
            cls(
                name="ingress",
                type=SubnetType.PUBLIC,
            ),
            cls(
                name="compute",
                type=SubnetType.PRIVATE,
            ),
            cls(
                name="isolated",
                type=SubnetType.ISOLATED,
            ),
        ]


class ResourceConfig(BaseSettings):
    name: str
    env: str
    account: str
    region: str
    tags: dict[str, str] = Field(default_factory=dict)

    model_config = SETTINGS_CONFIG

    @property
    def construct_id(self) -> str:
        return f"{self.env.capitalize()}{self.name}"


class VpcConfig(ResourceConfig):
    max_azs: int = 1
    subnets: list[SubnetConfig] = Field(
        default_factory=SubnetConfig.vpc_defaults
    )


# class RdsConfig(StackConfig):
#     vpc_id: str
#     db_port: int = 5432
#     allocated_storage: int = 32
#     database_name: str = "main"
#     instance_type: comps.Ec2Config = Field(
#         default=comps.Ec2Config(
#             size=ec2.InstanceSize.MICRO, type_=ec2.InstanceClass.T4G
#         )
#     )
#     # TODO support non-postgres
#     engine_version: rds.PostgresEngineVersion = (
# rds.PostgresEngineVersion.VER_15_3)
#     removal_policy: RemovalPolicy = Field(default=RemovalPolicy.SNAPSHOT)
#     deletion_protection: bool = Field(default=False)
# subnet_type: ec2.SubnetType = Field(
#         default=ec2.SubnetType.PRIVATE_ISOLATED)


# class BastionConfig(StackConfig):
#     vpc_id: str
#     key_pair_name: str
#     ssh_port: int = 22
#     bootstrap_script: str | None = None
#     ip_allowlist: list[str] = Field(default_factory=list)
# ingress_confs: list[
#         comps.IngressConfig
#     ] = Field(default_factory=list)


# class FargateConfig(StackConfig):
#     vpc_id: str
#     container: comps.ContainerConfig
#     public_access: bool = False
#     scaling: comps.ScalingConfig = comps.ScalingConfig()
#     ip_allowlist: list[str] = Field(default_factory=list)
#     ingress_confs: list[comps.IngressConfig] = Field(
# default_factory=list)
#     domains: list[comps.DomainConfig] = Field(default_factory=list)

#     external_http_port: int = 80
#     external_https_port: int = 443

#     @property
#     def use_efs(self) -> bool:
#         return len(self.container.volumes) > 0

#     @property
#     def supports_https(self) -> bool:
#         return any(self.domains)

#     @property
#     def external_ports(self) -> Iterable[int]:
#         if self.supports_https:
#             return (self.external_http_port, self.external_https_port)
#         return (self.external_http_port,)
