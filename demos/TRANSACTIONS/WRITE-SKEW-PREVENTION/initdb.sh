#!/bin/bash

DB_URL="mongodb+srv://${ATLAS_USER}:${ATLAS_PASS}@${ATLAS_CLUSTER_HOSTNAME}/"
DB_NAME="TRANSACTIONS-WRITESKEW"
ACC_COLL_NAME="accounts"

printf "\nStarted: Initialising DB\n"
mongosh --eval "
    db = db.getSiblingDB('${DB_NAME}');
    accColl = db['${ACC_COLL_NAME}'];
    accColl.drop();    
    accColl.createIndex({account_holder: 1, account_type: 1}, {unique: true});
    print('Re-created database and indexes with empty collections');
" ${DB_URL}

mongoimport --uri ${DB_URL} -d ${DB_NAME} -c ${ACC_COLL_NAME} --type csv --headerline --useArrayIndexFields --columnsHaveTypes "${ACC_COLL_NAME}.csv"
printf "Imported data into DB collections\n"

printf "Finished: Initialising DB\n"
printf "CONNECTION URL:\n"
