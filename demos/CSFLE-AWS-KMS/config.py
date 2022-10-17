import os
import urllib.parse
from helpers import assume_role

provider = "aws"
awsrole = os.environ["ATLAS_AWS_ROLE"]
db_name = "CSFLE-AWS-DEMO"
credentials = assume_role(awsrole)
kms_providers = {
    provider: {
        "accessKeyId": credentials["AccessKeyId"],
        "secretAccessKey": credentials["SecretAccessKey"],
        "sessionToken": credentials["SessionToken"],
    }
}
access_key_id = urllib.parse.quote_plus(credentials["AccessKeyId"])
secret_access_key = urllib.parse.quote_plus(credentials["SecretAccessKey"])
session_token = urllib.parse.quote_plus(credentials["SessionToken"])

kms_key_arn = os.environ["ATLAS_AWS_KMS_KEY"]
kms_key_region = "eu-north-1"
connection_string = (
    f"mongodb+srv://{access_key_id}:{secret_access_key}@{os.environ['ATLAS_CLUSTER_HOSTNAME']}/?"
    f"authMechanism=MONGODB-AWS&authMechanismProperties=AWS_SESSION_TOKEN:{session_token}&authSource=$external"
)
key_vault_namespace = "encryption.__keyVault"
