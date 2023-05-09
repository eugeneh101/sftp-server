#!/usr/bin/env python3
import aws_cdk as cdk
import boto3

from sftp_server.sftp_server_stack import SftpServerStack


app = cdk.App()
account = boto3.client("sts").get_caller_identity()["Account"]
environment = app.node.try_get_context("environment")
SftpServerStack(
    app,
    "SftpServerStack",
    env=cdk.Environment(account=account, region=environment["AWS_REGION"]),
    environment=environment,
)
app.synth()
