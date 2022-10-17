from config import connection_string
from pymongo import MongoClient
from schema import json_schema


client = MongoClient(connection_string)

schema = {"$jsonSchema": json_schema}

client["CSFLE-AWS-DEMO"].create_collection("patients", validator=schema)
