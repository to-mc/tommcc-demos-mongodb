#!/usr/bin/env python3
import hashlib
import os
import sys

from pymongo import MongoClient


####
# READ_DATA is main routine. Reads from a changestream all changes
# that write_data is adding. Each string of data is added to hashlib
# and std output is updated with the moving MD5 hash
####
def read_data(proof12):
    # setup a md5 checksum
    h = hashlib.md5()

    seq = 1
    cursor = proof12.watch()
    print("Successfully connected, watching for changes...")
    try:
        for doc in cursor:
            try:
                # hashlib.update works cummullative.
                # Repeated calls are equivalent to a single call with
                # the concatenation of all the arguments
                h.update(doc["fullDocument"]["random"].encode())
                print("Seq: ", seq, " md5:", h.hexdigest())
                sys.stdout.flush()
                seq += 1
            except Exception as ex:
                print(ex)
                print("Cannot read: No cluster instance available for reading?")
    except KeyboardInterrupt:
        keyboard_shutdown()


####
# Swallow the verbiage that is spat out when using 'Ctrl-C' to kill the script
# and instead just print a simple single line message
####
def keyboard_shutdown():
    print("Interrupted\n")
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)


####
# Check all prerequesites - mainly read.py must be started
# before write.py
####
def prereqs():
    connstring = (
        f"mongodb+srv://{os.environ.get('ATLAS_USER')}:"
        + f"{os.environ.get('ATLAS_PASS')}@{os.environ.get('ATLAS_CLUSTER_HOSTNAME')}"
    )
    client = MongoClient(connstring, retryWrites=True)
    db = client["ROLLING-UPDATES"]

    # Drop data collection to make sure it is empty
    db.data.drop()

    # Now make sure it exist and empty
    proof12 = db.create_collection("data")

    return proof12


if __name__ == "__main__":
    col = prereqs()
    read_data(col)
