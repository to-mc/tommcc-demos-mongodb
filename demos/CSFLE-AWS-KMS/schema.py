from bson import Binary, UUID_SUBTYPE
from helpers import load_data_key_id
import base64

data_key = load_data_key_id()

key_id = Binary(base64.b64decode(data_key), UUID_SUBTYPE)

json_schema = {
    "bsonType": "object",
    "properties": {
        "insurance": {
            "bsonType": "object",
            "properties": {
                "policyNumber": {
                    "encrypt": {
                        "bsonType": "int",
                        "algorithm": "AEAD_AES_256_CBC_HMAC_SHA_512-Deterministic",
                        "keyId": [key_id],
                    }
                }
            },
        },
        "medicalRecords": {
            "encrypt": {
                "bsonType": "array",
                "algorithm": "AEAD_AES_256_CBC_HMAC_SHA_512-Random",
                "keyId": [key_id],
            }
        },
        "bloodType": {
            "encrypt": {
                "bsonType": "string",
                "algorithm": "AEAD_AES_256_CBC_HMAC_SHA_512-Random",
                "keyId": [key_id],
            }
        },
        "ssn": {
            "encrypt": {
                "bsonType": "string",
                "algorithm": "AEAD_AES_256_CBC_HMAC_SHA_512-Deterministic",
                "keyId": [key_id],
            }
        },
    },
}
