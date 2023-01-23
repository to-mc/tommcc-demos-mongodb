module.exports = {
  mdb_url: `mongodb+srv://${process.env.ATLAS_USER}:${process.env.ATLAS_PASS}@${process.env.ATLAS_CLUSTER_HOSTNAME}/test`,
  //Concurrency: how many parallel threads should be doing inserts
  //increase this number to increase the workload on mongodb
  //recommended to be set equal to the number of cores on the machine running this program
  concurrency: 10,

  //how many records should be returned by find commands
  limit: 10,

  //operation frequency (milliseconds)
  writeFrequency: 2,
  readFrequency: 5,
};
