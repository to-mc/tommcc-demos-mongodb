import os

mongo_uri = (
    f"mongodb+srv://{os.environ.get('ATLAS_USER')}:"
    + f"{os.environ.get('ATLAS_PASS')}@{os.environ.get('ATLAS_CLUSTER_HOSTNAME')}"
)

