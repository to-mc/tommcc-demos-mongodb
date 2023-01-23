./bin/mongosync --cluster0 mongodb://localhost --cluster1 mongodb+srv://${ATLAS_USER}:${ATLAS_PASS}@${ATLAS_CLUSTER_HOSTNAME}/





curl localhost:27182/api/v1/start -XPOST \
--data '
   {
      "source": "cluster0",
      "destination": "cluster1"
   } '