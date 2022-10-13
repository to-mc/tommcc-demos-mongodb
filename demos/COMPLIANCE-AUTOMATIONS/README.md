# Compliance checker

Installs a scheduled trigger with an app services function that checks if auditing is enabled, and monitoring tools are disabled. If they are out of compliance, the settings get updated.


## Steps

### Install and log in to the realm cli

```
npm install -g mongodb-realm-cli
realm-cli login --api-key=${TM_ATLAS_PUBLIC_KEY} --private-api-key=${TM_ATLAS_PRIVATE_KEY}
```


### Create an API key (at organization level) and add the credentials as secrets

```
realm-cli secrets create --name="AtlasPublicKey"  --value="${TM_ATLAS_PUBLIC_KEY}"
realm-cli secrets create --name="AtlasPrivateKey"  --value="${TM_ATLAS_PRIVATE_KEY}"
realm-cli secrets create --name="AtlasProjectId"  --value="${TM_ATLAS_PROJECT_ID}"
```

### Deploy the application

```
realm-cli push
```


### Optional: manually run the function
```
realm-cli function run
```