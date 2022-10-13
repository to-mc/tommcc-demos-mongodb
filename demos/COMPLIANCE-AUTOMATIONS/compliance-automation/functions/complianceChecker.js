exports = async function () {
  
  const baseUrl = `https://${context.values.get("TM_ATLAS_PUBLIC_KEY")}:${context.values.get("TM_ATLAS_PRIVATE_KEY")}@cloud.mongodb.com/api/atlas/v1.0/`;
  const projectSettingsUrl = `${baseUrl}groups/${context.values.get("TM_ATLAS_PROJECT_ID")}/settings`;
  const auditLogUrl = `${baseUrl}groups/${context.values.get("TM_ATLAS_PROJECT_ID")}/auditLog`;

  const options = {
    digestAuth: true,
    encodeBodyAsJSON: true,
    headers: {
      "Content-type": ["application/json"],
    },
  };

  const retrieveSettings = async function () {
    const settingsResult = await context.http.get({url: projectSettingsUrl, ...options});
    const auditResult = await context.http.get({url: auditLogUrl, ...options});
    const result = {
      ...EJSON.parse(settingsResult.body.text()),
      audit: EJSON.parse(auditResult.body.text()),
    };
    return result;
  };

  const setProjectSettings = async function () {
    // Desired settings
    const data = {
      isDataExplorerEnabled: false,
      isPerformanceAdvisorEnabled: false,
      isRealtimePerformancePanelEnabled: false,
      isSchemaAdvisorEnabled: false,
    };

    await context.http.patch({url: projectSettingsUrl, 
      ...options,
      body: data,
    });
  };

  const setAuditLog = async function () {
    // EXAMPLE AUDIT FILTER
    const auditFilter = {
      atype: "authenticate",
      param: { user: "auditReadOnly", db: "admin", mechanism: "SCRAM-SHA-1" },
    };

    const data = {
      auditAuthorizationSuccess: false,
      enabled: true,
      auditFilter: EJSON.stringify(auditFilter),
    };

    await context.http.patch({url: auditLogUrl, 
      ...options,
      body: data
    });
  };

  const checkSettings = async function (projectSettings) {
    // Check project settings
    const values = [
      projectSettings.isDataExplorerEnabled,
      projectSettings.isPerformanceAdvisorEnabled,
      projectSettings.isRealtimePerformancePanelEnabled,
      projectSettings.isSchemaAdvisorEnabled,
    ];

    // If any of the values are true
    if (values.some((element) => element === true)) {
      console.log("project settings incorrect");
      await setProjectSettings();
      console.log("project settings corrected");
    } else {
      console.log("project settings are correct");
    }

    // Check audit settings
    if (!projectSettings.audit.enabled) {
      console.log("auditing is disabled");
      await setAuditLog();
      console.log("auditing has been enabled");
    } else {
      console.log("auditing is enabled");
    }
  };

  retrieveSettings().then((data) => {
    checkSettings(data);
  });
  
};
