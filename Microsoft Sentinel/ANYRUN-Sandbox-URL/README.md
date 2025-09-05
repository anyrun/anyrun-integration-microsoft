<p align="center">
    <a href="#readme">
        <img alt="ANY.RUN logo" src="https://raw.githubusercontent.com/anyrun/anyrun-sdk/b3dfde1d3aa018d0a1c3b5d0fa8aaa652e80d883/static/logo.svg">
    </a>
</p>

______________________________________________________________________

# Microsoft Sentinel Connector for automated URL analysis via ANY.RUN Malware Sandbox

## Overview

This playbook extracts URL from incidents and submit it for analysis in the ANY.RUN Sandbox to enrich the incident with a verdict using a single Azure Logic App.

## Requirements:
- ANY.RUN API-Key
- Microsoft Sentinel
- Azure Logic App (Flex Consumption plan) 

## Deployment

### Import Azure Logic App template

- Click below to deploy Azure Logic App with **Flex Consumption plan**

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Frollehfoh%2FANY.RUN%2Fmain%2Fconnectors%2FMicrosoft%2FMicrosoft%2520Sentinel%2FANYRUN-Sandbox-URL%2FANYRUN-Sandbox-URL.json)

- Enter the parameters required for deploying the Logic App and click **Review + create**.

![logic_app_deployment](images/004.png)

- Description of the required parameters:

| Parameter Name                  | Description                                                                 |
|---------------------------------|-----------------------------------------------------------------------------|
| LogicAppName                    | Workflow name.                                                              |
| AzureTenantId                   | Tenant ID for authentication in connections.                                |
| AzureClientId                   | Client ID for authentication (ID of the App Registration created before).   |
| azureClientSecret               | Client Secret for authentication.                                           |
| keyVaultName                    | Key Vault name.                                                             |
| keyVaultUri                     | Key Vault URI (copy Vault URI from your Key Vault overview).                |

## Logic App configuration (Optional)

### ANY.RUN Sandbox analysis parameters

ANY.RUN is an interactive online malware analysis service for dynamic and static research of most types of threats using any environments. We offer a connector for Microsoft Sentinel, which you can independently adapt to your infrastructure and needs in just a few clicks. You can easily change the parameters used for analyzing the required URL.

> **Note:** You can learn more about the capabilities of ANY.RUN Sandbox by reviewing our **[API documentation](https://any.run/api-documentation/)**.

The main setup and customization of the Logic App is available through the graphical editor (**Development tools** > **Logic app designer**) or the code editor (**Development tools** > **Logic app code view**).

- The URL analysis parameters in ANY.RUN Sandbox are defined in the **HTTP-RunNewURLAnalysis** action.

![analysis_action](images/001.png)

- Analysis options are specified in the HTTP request body.

![analysis_parameters](images/002.png)

- Description of the default parameters:

| Parameter Name              | Description                                                                 |
|-----------------------------|-----------------------------------------------------------------------------|
| obj_type                    | Specifies the type of the new task (the value "url" is required for this workflow). |
| opt_timeout                 | Defines the timeout option for the analysis.                                |
| obj_ext_browser             | Indicates the browser name to use.                                          |
| env_os                      | Specifies the operating system.                                             |
| env_bitness                 | Defines the bitness of the operating system.                                |
| env_version                 | Sets the version of the operating system.                                   |
| opt_automated_interactivity | Controls the automated interactivity (ML) option (changing this is not recommended). |
| auto_confirm_uac            | Enables automatic confirmation of Windows UAC requests (changing this is not recommended). |

> **Note:** You can add more parameters for analysis. To see the full list of available parameters and their values, visit our **[API documentation](https://any.run/api-documentation/)**.

### Simultaneous Analysis of Objects in ANY.RUN Sandbox

ANY.RUN Sandbox allows users to perform multiple analyses simultaneously (availability and capability depend on your pricing plan). By default, if a Microsoft Sentinel incident contains multiple URLs, each analysis will run sequentially (a new URL analysis won't start until the previous one finishes, to avoid errors).

- To increase the speed of incident enrichment, you can analyze objects simultaneously. To do this, open the **For each - URL** loop > **Settings** and increase the **Degree of parallelism** value. It is recommended to set a value that does not exceed the number of possible parallel analyses in ANY.RUN Sandbox for your pricing plan.

![parallel_analysis](images/003.png)

> **Note**: To upgrade your pricing plan capabilities, [contact us](https://app.any.run/contact-us).
