"use strict";

const express = require('express');
const routes = require('./routes.js');
const MongoClient = require('mongodb').MongoClient;

const uri = `mongodb+srv://${process.env.ATLAS_USER}:${process.env.ATLAS_PASS}@${process.env.ATLAS_CLUSTER_HOSTNAME}/GEOSPATIAL`
const client = new MongoClient(uri)

let app = express();

let allowCrossDomain = (req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Methods', 'GET');
  res.header('Access-Control-Allow-Headers', 'Content-Type');
  next();
};

app.use(allowCrossDomain);

const db = client.db("GEOSPATIAL");


app.get('/stations', routes.getStations.bind(null, db));
app.get('/stations/statistics', routes.getStationSummary.bind(null, db));
app.get('/stations/statistics/:id', routes.getStationStatistics.bind(null, db));
app.get('/stations/:id', routes.getStation.bind(null, db));
app.get('/bikes', routes.getBike.bind(null, db));

app.listen(8081, () => console.log("Server listening..."));


