import os

IAM_ROLE_ARN = os.environ["IAM_ROLE_ARN"]
BUCKET_NAME = os.environment["BUCKET_NAME"]

def lambda_handler(event, context) -> dict[str, str]:
    print(event)
    return {
        "Role": IAM_ROLE_ARN,
        "HomeDirectory": f"/{BUCKET_NAME}"
    }