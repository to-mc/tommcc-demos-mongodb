import base64
import os
import pathlib
import pymongo
import pymongo.encryption

from config import (
    provider,
    kms_providers,
    connection_string,
    kms_key_arn,
    kms_key_region,
    db_name
)


key_vault_coll = "__keyVault"
key_vault_db = "encryption"
key_vault_namespace = f"{key_vault_db}.{key_vault_coll}"
key_vault_client = pymongo.MongoClient(connection_string)
# Drop the Key Vault Collection in case you created this collection
# in a previous run of this application.
key_vault_client.drop_database(key_vault_db)
# Drop the database storing your encrypted fields as all
# the DEKs encrypting those fields were deleted in the preceding line.
key_vault_client[db_name].drop_collection("patients")
key_vault_client[key_vault_db][key_vault_coll].create_index(
    [("keyAltNames", pymongo.ASCENDING)],
    unique=True,
    partialFilterExpression={"keyAltNames": {"$exists": True}},
)

master_key = {
    "region": kms_key_region,
    "key": kms_key_arn,
}


key_vault_namespace = f"{key_vault_db}.{key_vault_coll}"
client = pymongo.MongoClient(connection_string)
client_encryption = pymongo.encryption.ClientEncryption(
    kms_providers,  # pass in the kms_providers variable from the previous step
    key_vault_namespace,
    client,
    pymongo.encryption.CodecOptions(uuid_representation=pymongo.encryption.STANDARD),
)
data_key_id = client_encryption.create_data_key(provider, master_key, key_alt_names=["tommcc-dek-1"])


app_dir = pathlib.Path(__file__).parent.resolve()
with open(os.path.join(app_dir, "dataKeyId.txt"), "wb") as outfile:
    outfile.write(base64.b64encode(data_key_id))

print("Wrote data key id to dataKeyId.txt")
