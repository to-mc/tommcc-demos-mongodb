// make-data-key.js

const { readMasterKey, CsfleHelper } = require("./helpers");
const { connectionString, dataKey } = require("./config");

async function main() {
  const localMasterKey = readMasterKey();

  const csfleHelper = new CsfleHelper({
    kmsProviders: {
      local: {
        key: localMasterKey,
      },
    },
    connectionString: connectionString,
  });

  const client = await csfleHelper.getRegularClient();

  const dataKey = await csfleHelper.findOrCreateDataKey(client);
  console.log(
    "Base64 data key. Copy and paste this into config.js\t",
    dataKey
  );

  client.close();
}

main().catch(console.dir);
