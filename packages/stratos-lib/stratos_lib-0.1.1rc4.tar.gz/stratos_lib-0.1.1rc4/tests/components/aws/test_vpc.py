import pulumi

from stratos_lib import configs as confs
from stratos_lib.components.aws.vpc import VpcComponent

from ...fixtures import PulumiMocks

pulumi.runtime.set_mocks(PulumiMocks(), preview=False)


@pulumi.runtime.test
def test_vpc():
    config = confs.VpcConfig(
        name="TestVpc",
        env="test",
        account="fake",
        region="us-east-1",
        tags={"test": "test"},
    )

    def check_subnets(subnets):
        assert len(subnets) == len(config.subnets)

    vpc = VpcComponent(config=config)

    return pulumi.Output.all(*vpc.subnets).apply(check_subnets)
