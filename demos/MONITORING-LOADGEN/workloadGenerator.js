const config = require("./config");
const mongodb = require("mongodb");
const cluster = require("cluster");
var faker = require("faker");

//Generate data for mongodb
var client = new mongodb.MongoClient(config.mdb_url);

if (cluster.isPrimary) {
  console.log(config.mdb_url);

  console.log(`Master ${process.pid} is running`);

  // Fork workers.
  for (let i = 0; i < config.concurrency; i++) {
    cluster.fork();
  }

  cluster.on("exit", (worker, code, signal) => {
    console.log(`worker ${worker.process.pid} died`);
  });
} else {
  // Workers can all write to mongodb at once
  client.connect().then(function () {
    console.log("Connected successfully to server");
    var dbName = "monitoringExample";
    const db = client.db(dbName);
    var collection = db.collection("sample");

    //simulate writes
    simReads(collection);

    //simulate reads
    simWrites(collection);
  });
}

function genData() {
  var newDoc = {
    name: {
      first: faker.name.firstName(),
      last: faker.name.lastName(),
    },
    date: faker.date.recent(),
    transaction: {
      account: faker.finance.account(),
      transactionType: faker.finance.transactionType(),
      currency: faker.finance.currencyCode(),
      amount: faker.finance.amount(),
    },
  };

  return newDoc;
}

function getRandomInt(min, max) {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min)) + min;
}

async function simWrites(collection) {
  setInterval(function () {
    try {
      collection.insertOne(genData(), function (err, result) {
        if (err != null) {
          console.log(err);
        }
      });
    } catch (err) {
      console.log(err);
    }
  }, config.writeFrequency);
}

async function simReads(collection) {
  setInterval(function () {
    var skipNum = getRandomInt(0, 5000);
    var limit = skipNum + config.limit;
    try {
      collection.find({}, { limit: limit, skip: skipNum }).toArray();
    } catch (err) {
      console.log(err);
    }
  }, config.readFrequency);
}
