from aws_cdk import (
    Duration,
    RemovalPolicy,
    Stack,
    aws_iam as iam,
    aws_lambda as _lambda,
    aws_s3 as s3,
    aws_transfer as transfer,
)
from constructs import Construct


class SftpServerStack(Stack):
    def __init__(
        self, scope: Construct, construct_id: str, environment: dict, **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.sftp_role = iam.Role(
            self,
            "SftpRole",
            assumed_by=iam.CompositePrincipal(
                iam.ServicePrincipal("transfer.amazonaws.com"),
                iam.ServicePrincipal("lambda.amazonaws.com"),
            ),
        )
        self.sftp_role.add_to_policy(
            statement=iam.PolicyStatement(
                actions=[
                    "logs:CreateLogGroup",
                    "logs:CreateLogStream",
                    "logs:PutLogEvents",
                ],
                resources=["*"],
            ),
        )
        self.sftp_role.add_to_policy(
            statement=iam.PolicyStatement(
                actions=[
                    "s3:ListBucket",
                    "s3:GetBucketLocation",
                    # more permissions
                    "s3:PutObject",
                    "s3:List*",
                    "s3:GetObject",
                    "s3:DeleteObject",
                    "s3:DeleteObjectVersion",
                    "s3:GetObjectVersion",
                    "s3:GetObjectACL",
                    "s3:PutObjectACL",
                ],
                resources=["*"],
            ),
        )
        self.sftp_role.add_to_policy(
            statement=iam.PolicyStatement(
                actions=["lambda:InvokeFunction"],
                resources=["*"],
            ),
        )

        self.s3_bucket_for_sftp = s3.Bucket(
            self,
            "S3BucketForSnsMessages",
            bucket_name=environment["S3_BUCKET_NAME"],
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )

        self.authentication_lambda = _lambda.Function(
            self,
            "AuthenticationLambda",
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset(
                "lambda_code/authentication_lambda",
                exclude=[".venv/*"],
            ),
            handler="handler.lambda_handler",
            timeout=Duration.seconds(3),  # should be instantaneous
            memory_size=128,
            environment={"S3_BUCKET_NAME": environment["S3_BUCKET_NAME"]},
            role=self.sftp_role,
        )

        # connect AWS resources
        self.authentication_lambda.add_environment(
            key="IAM_ROLE_ARN", value=self.sftp_role.role_arn
        )
        transfer.CfnServer(
            self,
            "SftpServer",
            logging_role=self.sftp_role.role_arn,
            domain="S3",
            endpoint_type="PUBLIC",
            identity_provider_type="AWS_LAMBDA",
            identity_provider_details={
                "function": self.authentication_lambda.function_arn
            },
        )
