import os

IAM_ROLE_ARN = os.environ["IAM_ROLE_ARN"]
S3_BUCKET_NAME = os.environ["S3_BUCKET_NAME"]


def lambda_handler(event, context) -> dict[str, str]:
    print(event)
    return {
        "Role": IAM_ROLE_ARN,
        "HomeDirectory": f"/{S3_BUCKET_NAME}",
    }
