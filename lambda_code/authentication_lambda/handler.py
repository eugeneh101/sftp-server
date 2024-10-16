import json
import os

IAM_ROLE_ARN = os.environ["IAM_ROLE_ARN"]
S3_BUCKET_NAME = os.environ["S3_BUCKET_NAME"]


def lambda_handler(event, context) -> dict[str, str]:
    print(event)
    if event.get("username") == "demo" and event.get("password") == "demo":
        return {
            "Role": IAM_ROLE_ARN,
            "HomeDirectoryType": "LOGICAL",
            "HomeDirectoryDetails": json.dumps(
                [{"Entry": "/", "Target": f"/{S3_BUCKET_NAME}"}]
            ),
        }
    else:
        return {
            "statusCode": 401,
            "body": "Unauthorized access",
        }
