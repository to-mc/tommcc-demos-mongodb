# Data masking

## Seed data (if needed)
1. Connect to db: `mongosh  "mongodb+srv://${ATLAS_USER}:${ATLAS_PASS}@${ATLAS_CLUSTER_HOSTNAME}/"`
2. Add data:

```
use DATA-MASKING;

db.dropDatabase();

db.payments.insertMany([
    {
        'card_name': 'Mrs. Jane A. Doe',
        'card_num': '1234567890123456',
        'card_expiry': ISODate('2023-08-31T23:59:59Z'),
        'card_sec_code': '123',
        'card_provider_name': 'Credit MasterCard Gold',
        'card_type': 'CREDIT',        
        'transaction_id': 'eb1bd77836e8713656d9bf2debba8900',
        'transaction_date': ISODate('2021-01-13T09:32:07Z'),
        'transaction_curncy_code': 'GBP',
        'transaction_amount': NumberDecimal('501.98'),
        'settlement_id': '9ccb27aeb8394c2b3547521bcd52a367',
        'settlement_date': ISODate('2021-01-21T14:03:53Z'),
        'settlement_curncy_code': 'DKK',
        'settlement_amount': NumberDecimal('4255.16'),
        'reported': false,
        'customer_info': {
            'category': 'SENSITIVE',
            'rating': 89,
            'risk': 3,
        }
    },
    {
        'card_name': 'Jim Smith',
        'card_num': '9876543210987654',
        'card_expiry': ISODate('2022-12-31T23:59:59Z'),
        'card_sec_code': '987',
        'card_provider_name': 'Debit Visa Platinum',
        'card_type': 'DEBIT',        
        'transaction_id': '634c416a6fbcf060bb0ba90c4ad94f60',
        'transaction_date': ISODate('2020-11-24T19:25:57Z'),
        'transaction_curncy_code': 'EUR',
        'transaction_amount': NumberDecimal('64.01'),
        'settlement_id': 'd53799f94d7ad72f698c5a4f04c031a6',
        'settlement_date': ISODate('2020-12-04T11:51:48Z'),
        'settlement_curncy_code': 'USD',
        'settlement_amount': NumberDecimal('76.87'),
        'reported': true,
        'customer_info': {
            'category': 'NORMAL',
            'rating': 78,
            'risk': 55,
        }
    },
]);

db.payments.find();
```

## Execute demo

1. Connect to db: `mongosh  "mongodb+srv://${ATLAS_USER}:${ATLAS_PASS}@${ATLAS_CLUSTER_HOSTNAME}/"`
2. Create the masking pipeline:


```
// PART 1 OF PIPELINE
var simpleMasksPt1Stage = {
    // 1. FULL TEXT REPLACEMENT WITH RANDOM VALUES, eg: '133' -> '472'
    'card_sec_code': {'$concat': [
                        {'$toString': {'$floor': {'$multiply': [{'$rand': {}}, 10]}}},
                        {'$toString': {'$floor': {'$multiply': [{'$rand': {}}, 10]}}},
                        {'$toString': {'$floor': {'$multiply': [{'$rand': {}}, 10]}}},
                     ]},
                     
    // 2. PARTIAL TEXT OBFUSCATION RETAINING LAST NUMBER OF CHARS, eg: '1234567890123456' -> 'XXXXXXXXXXXX3456'
    'card_num': {'$concat': [
                    'XXXXXXXXXXXX',
                    {'$substrCP': ['$card_num', 12, 4]},
                ]},
    
    // 3a. PARTIAL TEXT OBFUSCATION RETAINING LAST WORD, eg: 'Mrs. Jane A. Doe' -> 'Mx. Xxx Doe'  (needs post-processing in a subsequent pipeline stage)
    'card_name': {'$regexFind': {'input': '$card_name', 'regex': /(\S+)$/}},
        
    // 4. PARTIAL DATE OBFUSCATION BY ADDING OR SUBTRACTING A RANDOM TIME AMOUNT UP TO ONE HOUR MAX
    'transaction_date': {'$add': [
                            '$transaction_date',
                            {'$floor': {'$multiply': [{'$subtract': [{'$rand': {}}, 0.5]}, 2*60*60*1000]}},
                        ]},
    
    // 5. FULL DATE REPLACEMENT BY TAKING AN ARBITRARY DATETIME OF 01-Jan-2021 AND ADDING A RANDOM AMOUNT UP TO ONE YEAR MAX
    'settlement_date': {'$add': [
                            {'$dateFromString': {'dateString': '2021-01-01T00:00:00.000Z'}},
                            {'$floor': {'$multiply': [{'$rand': {}}, 365*24*60*60*1000]}},
                       ]},

    // 6. FULL DATE REPLACEMENT BY TAKING THE CURRENT DATETIME AND ADDING A RANDOM AMOUNT UP TO ONE YEAR MAX
    'card_expiry': {'$add': [
                        '$$NOW',
                        {'$floor': {'$multiply': [{'$rand': {}}, 365*24*60*60*1000]}},
                   ]},
    
    // 7. PARTIAL NUMBER OBFUSCATION BY ADDING OR SUBTRACTING A RANDOM PERCENT OF ITS VALUE, UP TO 10% MAX
    'transaction_amount': {'$add': [
                            '$transaction_amount',
                            {'$trunc': {'$multiply': [{'$subtract': [{'$rand': {}}, NumberDecimal('0.5')]}, NumberDecimal('0.2'), '$transaction_amount']}},
                        ]},

    // 8. BOOLEAN RANDOM REPLACEMENT, ie. a 50:50 chance of being true vs false
    'reported': {'$cond': {
                    'if':   {'$gte': [{'$rand': {}}, 0.5]}, 'then': true,
                    'else': false
                }},               

    // 9. FULL FIELD OBFUSCATION USING AN MD5 HASH OF ITS VALUE (note, not 'cryptographically safe')
    'transaction_id': {'$function': {'lang': 'js', 'args': ['$transaction_id'], 'body':                   
                            function(id) {
                                return hex_md5(id);
                            }
                      }},
};


// PART 2 OF PIPELINE
var simpleMasksPt2Stage = {
    // 3b. PARTIAL TEXT OBFUSCATION RETAINING LAST WORD (post processing from previous regex operation to pick out 'match')
    'card_name': {'$concat': ['Mx. Xxx ', {'$ifNull': ['$card_name.match', 'Anonymous']}]},
};


// PART 3 OF PIPELINE
var redactFieldsStage = {
    // 10. EXCLUDE SUB-DOCUMENT DATA BASED ON A FIELD'S VALUE, eg. if customer_info.category = SENSITIVE
    '$cond': {
        'if'  : {'$eq': ['$category', 'SENSITIVE']},
        'then': '$$PRUNE',
        'else': '$$DESCEND'
    }
};


// BRING FULL PIPELINE TOGETHER
var pipeline = [
    {'$set': simpleMasksPt1Stage},
    {'$set': simpleMasksPt2Stage},
    {'$redact': redactFieldsStage},
];
```
## Query the data
### Option 1: Query directly with pipeline (Trusted app)

`db.payments.aggregate(pipeline)`


### Option 2: Create masked read-only view
`db.createView('payments_redacted_view', 'payments', pipeline)`

`db.payments_redacted_view.find()`


### Option 3: Create masked copy of data

```
new_pipeline = [].concat(pipeline);  // COPY THE ORIGINAL PIPELINE
new_pipeline.push(
    {'$merge': {'into': { 'db': 'DATA-MASKING', 'coll': 'payments_redacted'}, 'on': '_id',  'whenMatched': 'fail', 'whenNotMatched': 'insert'}}
);
db.payments.aggregate(new_pipeline);
db.payments_redacted.find();
```


### Option 4: Overwrite original data with masked data

```
replace_pipeline = [].concat(pipeline);  // COPY THE ORIGINAL PIPELINE
replace_pipeline.push(
    {'$merge': {'into': { 'db': 'DATA-MASKING', 'coll': 'payments'}, 'on': '_id',  'whenMatched': 'replace', 'whenNotMatched': 'fail'}}
);
db.payments.aggregate(replace_pipeline);
db.payments.find();
```