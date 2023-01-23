var peopleSchema = {
  bsonType: "object",
  properties: {
    firstName: { bsonType: "string" }, // not required, but if listed type will be enforced
    lastName: { bsonType: "string" }, // not required, but if listed type will be enforced
    ssn: {
      encrypt: {
        bsonType: "string",
        algorithm: "AEAD_AES_256_CBC_HMAC_SHA_512-Deterministic",
        keyId: [key1],
      },
    },
    address: {
      bsonType: "object",
      properties: {
        street: { bsonType: "string" },
        city: { bsonType: "string" },
        state: { bsonType: "string" },
        zip: { bsonType: "string" },
      },
    },
    contact: {
      bsonType: "object",
      properties: {
        email: {
          encrypt: {
            bsonType: "string",
            algorithm: "AEAD_AES_256_CBC_HMAC_SHA_512-Deterministic",
            keyId: [key2],
          },
        },
        mobile: {
          encrypt: {
            bsonType: "string",
            algorithm: "AEAD_AES_256_CBC_HMAC_SHA_512-Deterministic",
            keyId: [key2],
          },
        },
      },
    },
  },
};
