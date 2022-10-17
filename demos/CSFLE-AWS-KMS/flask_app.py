from crypt import methods
import random
from config import kms_providers, connection_string, key_vault_namespace, db_name
from pymongo.encryption import AutoEncryptionOpts
from pymongo import MongoClient, errors
from schema import json_schema
from flask import Flask, request
from bson.json_util import dumps
import faker

fake = faker.Faker()
app = Flask(__name__)


patient_schema = {"CSFLE-AWS-DEMO.patients": json_schema}
fle_opts = AutoEncryptionOpts(
    kms_providers, key_vault_namespace, schema_map=patient_schema
)
secureClient = MongoClient(connection_string, auto_encryption_opts=fle_opts)
regularClient = MongoClient(connection_string)


def get_client(args):
    print(args)
    return secureClient if args.get("encrypt", default="") else regularClient


@app.route("/", methods=["GET"])
def find_all():
    client = get_client(request.args)

    doc = client[db_name].patients.find()
    return dumps(list(doc))


@app.route("/ssn/<string:ssn>", methods=["GET"])
def get_by_ssn(ssn):
    client = get_client(request.args)

    doc = client[db_name].patients.find_one({"ssn": ssn})
    return dumps(doc)


@app.route("/", methods=["POST"])
def add_random_user():
    client = get_client(request.args)
    doc = {
        "name": fake.name(),
        "ssn": fake.ssn(),
        "bloodType": random.choice(["A-", "A+", "B-", "B+", "AB-", "AB+", "O-", "O+"]),
        "medicalRecords": [
            {
                "weight": fake.random_int(min=50, max=200),
                "bloodPressure": f"{fake.random_int(min=50, max=130)}/{fake.random_int(min=40, max=85)}",
            }
        ],
        "insurance": {
            "policyNumber": fake.random_number(6),
            "provider": fake.company(),
        },
    }
    try:
        client[db_name].patients.insert_one(doc)
    except errors.WriteError as ex:
        return dumps(ex.details)
    return dumps(doc)
