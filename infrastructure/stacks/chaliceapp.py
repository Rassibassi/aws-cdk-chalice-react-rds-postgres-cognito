import json
import os

from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_rds as rds
from aws_cdk import aws_secretsmanager as secretsmanager
from aws_cdk import aws_ssm as ssm
from aws_cdk import core as cdk

# from chalice.cdk import Chalice
# RUNTIME_SOURCE_DIR = os.path.join(
#     os.path.dirname(os.path.dirname(__file__)), os.pardir, "backend"
# )


class ChaliceApp(cdk.Stack):
    def __init__(self, scope, id, **kwargs):
        super().__init__(scope, id, **kwargs)

        self.secret = secretsmanager.Secret(
            self,
            "Secret",
            secret_name="sampleapp-credentials", # DATABASE_SECRET_NAME
            generate_secret_string=secretsmanager.SecretStringGenerator(
                secret_string_template=json.dumps(
                    {
                        "username": "postgres",
                    }
                ),
                exclude_punctuation=True,
                include_space=False,
                generate_string_key="password",
            ),
        )

        self.vpc = ec2.Vpc(
            self,
            "VPC",
            max_azs=2,
            cidr="10.0.0.0/16",
            # configuration will create 3 groups in 2 AZs = 6 subnets.
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    subnet_type=ec2.SubnetType.PUBLIC, name="Public", cidr_mask=24
                ),
                ec2.SubnetConfiguration(
                    subnet_type=ec2.SubnetType.PRIVATE, name="Private", cidr_mask=24
                ),
                ec2.SubnetConfiguration(
                    subnet_type=ec2.SubnetType.ISOLATED, name="DB", cidr_mask=24
                ),
            ],
            # nat_gateway_provider=ec2.NatProvider.gateway(),
            nat_gateways=2,
        )

        self.security_group = ec2.SecurityGroup(
            self,
            "SecurityGroup",
            security_group_name="sampleapp-securitygroup",
            vpc=self.vpc,
        )

        # allow to connect to RDS from within the security group
        self.security_group.connections.allow_from(
            self.security_group, ec2.Port.tcp(5432), "PostgreSQL connection"
        )

        self.database_instance = rds.DatabaseInstance(
            self,
            "RDS",
            database_name="postgresdb",
            engine=rds.DatabaseInstanceEngine.postgres(
                version=rds.PostgresEngineVersion.VER_12_7
            ),
            vpc=self.vpc,
            port=5432,
            allocated_storage=20,
            security_groups=[self.security_group],
            credentials=rds.Credentials.from_secret(self.secret),
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.BURSTABLE3,
                ec2.InstanceSize.MICRO,
            ),
            removal_policy=cdk.RemovalPolicy.DESTROY,
            deletion_protection=False,
        )

        # self.chalice = Chalice(self, "ChaliceApp",
        #     source_dir=RUNTIME_SOURCE_DIR,
        #     stage_config={
        #         "autogen_policy": False,
        #         "iam_policy_file": "policy.json",
        #         "environment_variables": {
        #         }
        #     }
        # )

        cdk.CfnOutput(self, "Secret Name", value=self.secret.secret_name)
        cdk.CfnOutput(self, "Secret Full ARN", value=self.secret.secret_full_arn)
        cdk.CfnOutput(
            self,
            "RDS Endpoint Address",
            value=self.database_instance.db_instance_endpoint_address,
        )
        cdk.CfnOutput(
            self,
            "RDS Endpoint Port",
            value=self.database_instance.db_instance_endpoint_port,
        )
        cdk.CfnOutput(self, "VPC ID", value=self.vpc.vpc_id)
        cdk.CfnOutput(self, "Private Subnet 1", value=self.vpc.private_subnets[0].subnet_id)
        cdk.CfnOutput(self, "Private Subnet 2", value=self.vpc.private_subnets[1].subnet_id)
        cdk.CfnOutput(self, "Security Group ID", value=self.security_group.security_group_id)
