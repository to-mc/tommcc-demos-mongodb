import os
import pathlib
import boto3


def assume_role(aws_role_arn):
    sts_client = boto3.client("sts")
    assumed_role_object = sts_client.assume_role(
        RoleArn=aws_role_arn,
        RoleSessionName="AssumeRoleSession1",
    )

    return assumed_role_object["Credentials"]


def load_data_key_id():
    app_dir = pathlib.Path(__file__).parent.resolve()
    with open(os.path.join(app_dir, "dataKeyId.txt"), "rb") as fh:
        return fh.read()
