# CSFLE

## Setup

`openssl rand 96 > master-key.txt`

`node make-data-key.js`

Copy `config.js.example` to `config.js`
Copy key to `config.js`

node `clients.js`





# For AWS

Login to aws and set the shell context
```export AWS_PROFILE=SA
aws sso login```

Generate data key and write its ID to dataKeyId.txt:
`python make_data_key.py`

Optionally enable schema validation (enforce encryption):
`python enforce_encryption_server_schema.py`

## Flask app

Run `flask --app flask_app --debug run`

### Get all users
With encryption: http://127.0.0.1:5000/?encrypt=true
Without encryption: http://127.0.0.1:5000/

Get a user: http://127.0.0.1:5000/ssn/819-16-0723?encrypt=true

Add a random user: `curl -X POST http://127.0.0.1:5000/`
