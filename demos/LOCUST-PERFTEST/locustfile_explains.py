from urllib import response
import locust


import datetime
from string import ascii_letters
import uuid
from ulid import ULID

from pymongo import MongoClient
import time
import random
import os
import logging
import json


conn_string = (
    f"mongodb+srv://{os.environ.get('ATLAS_USER')}:"
    + f"{os.environ.get('ATLAS_PASS')}@{os.environ.get('ATLAS_CLUSTER_HOSTNAME')}"
)
CLIENT = MongoClient(conn_string)
SLOW_QUERY_THRESHOLD = 100


def random_date(start, end):
    """
    This function will return a random datetime between two datetime
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + datetime.timedelta(seconds=random_second)


class ExistingIds:
    __instance = None

    @staticmethod
    def getInstance():
        if ExistingIds.__instance is None:
            ExistingIds()
        return ExistingIds.__instance

    def __init__(self):
        if ExistingIds.__instance is not None:
            raise Exception("Cannot initialize more than one instance")
        else:
            with open("./data/ids_from_database.json", "r") as fh:
                self.ids = json.load(fh)
            ExistingIds.__instance = self


class NewIds:
    __instance = None

    @staticmethod
    def getInstance():
        if NewIds.__instance is None:
            NewIds()
        return NewIds.__instance

    def create_random_ids(self):
        print("generating random data...")
        data = [
            {
                "projectId": str(uuid.uuid4()),
                "appIds": [
                    {
                        "appId": str(ULID()),
                        "contactIds": [
                            {
                                "contactId": str(ULID()),
                                "conversationIds": [
                                    {"conversationId": str(ULID())}
                                    for _ in range(random.randrange(2, 20))
                                ],
                            }
                            for _ in range(random.randrange(50, 500))
                        ],
                    }
                    for _ in range(random.randrange(2, 10))
                ],
            }
            for _ in range(random.randrange(10, 20))
        ]
        print("finished generating random data...")
        return data

    def __init__(self):
        if NewIds.__instance is not None:
            raise Exception("Cannot initialize more than one instance")
        else:
            self.ids = self.create_random_ids()
            self.event_types = [
                "GENERIC_EVENT",
                "SPECIAL_EVENT",
                "EVENT1",
                "CUSTOM_EVENT",
                "ANOTHER_EVENT",
            ]
            NewIds.__instance = self


class Mongouser(locust.User):
    wait_time = locust.constant_throughput(5)
    client = CLIENT
    db = client["LOCUST-PERFTEST"]
    globaldata = ExistingIds.getInstance()
    newdata = NewIds.getInstance()

    def __init__(self, environment, *args, **kwargs):
        super().__init__(environment, *args, **kwargs)
        self.db.command("ping")

    @locust.task(20)
    @locust.tag("GET")
    def fetch_by_project(self):
        id_doc = random.choice(self.globaldata.ids)["_id"]
        skip = random.randrange(0, 10000, 50)
        response_time, n_returned = self.db_find(
            limit=50, sort=("eventTime", -1), skip=skip, projectId=id_doc["projectId"]
        )

        self.environment.events.request_success.fire(
            request_type="FIND",
            name="Find by projectID",
            response_time=response_time,
            response_length=n_returned,
        )

    @locust.task(40)
    @locust.tag("GET")
    def fetch_by_appId_conversationId(self):
        id_doc = random.choice(self.globaldata.ids)["_id"]
        response_time, n_returned = self.db_find(
            projectId=id_doc["projectId"],
            appId=id_doc["appId"],
            conversationId=id_doc["conversationId"],
            sort=("eventTime", -1),
        )
        self.environment.events.request_success.fire(
            request_type="FIND",
            name="Find by appId&conversationId",
            response_time=response_time,
            response_length=n_returned,
        )

    @locust.task(20)
    @locust.tag("GET")
    def fetch_by_contactId(self):
        id_doc = random.choice(self.globaldata.ids)["_id"]
        response_time, n_returned = self.db_find(
            projectId=id_doc["projectId"],
            contactId=id_doc["contactId"],
            sort=("eventTime", -1),
        )
        self.environment.events.request_success.fire(
            request_type="FIND",
            name="Find by contactId",
            response_time=response_time,
            response_length=n_returned,
        )

    def db_find(self, sort=None, limit=None, skip=None, **kwargs):
        cursor = self.db.events.find(kwargs)
        if sort:
            cursor.sort(*sort)
        if limit:
            cursor.limit(limit)
        if skip:
            cursor.skip(skip)
        explain = cursor.explain()
        return (
            explain["executionStats"]["executionTimeMillis"],
            explain["executionStats"]["nReturned"],
        )

    @locust.task(0)
    @locust.tag("PUT")
    def insert_new_record(self):
        item = random.choice(self.newdata.ids)
        app_id = random.choice(item["appIds"])
        contact_id = random.choice(app_id["contactIds"])
        conversation_id = random.choice(contact_id["conversationIds"])
        start_time = time.time()
        data = self.db.events.insert_one(
            {
                "_id": str(ULID()),
                "eventType": random.choice(self.newdata.event_types),
                "eventTime": random_date(
                    datetime.datetime.fromisoformat("2022-01-01"), datetime.datetime.now()
                ),
                "projectId": item["projectId"],
                "appId": app_id["appId"],
                "conversationId": conversation_id["conversationId"],
                "processingMode": "CONVERSATION",
                "contactId": contact_id["contactId"],
                "metadata": ("".join(random.choice(ascii_letters) for i in range(1000))),
                "_class": "com.companyname.eventstore.adapter.mongo.documents.Event",
            }
        )
        total_time = int((time.time() - start_time) * 1000)
        logging.debug(data)
        if data:
            self.environment.events.request_success.fire(
                request_type="INSERT",
                name="Insert new record",
                response_time=total_time,
                response_length=len(str(data)),
            )
        else:
            self.environment.events.request_failure.fire(
                request_type="INSERT",
                name="Insert new record",
                response_time=total_time,
                response_length=0,
                exception="No data",
            )
