<p align="center">
    <a href="#readme">
        <img alt="ANY.RUN logo" src="https://raw.githubusercontent.com/anyrun/anyrun-sdk/b3dfde1d3aa018d0a1c3b5d0fa8aaa652e80d883/static/logo.svg">
    </a>
</p>

______________________________________________________________________

# Microsoft Sentinel Connector for automated File analysis via ANY.RUN Malware Sandbox

## Overview

This playbook allows you to send files from incidents for analysis in the ANY.RUN Sandbox. 
It uploads the file from the endpoint to Azure Blob Storage and then forwards it to the ANY.RUN Sandbox using an Azure Logic App.

Templates are provided for endpoints running the following operating systems:
- Windows
- UNIX (Ubuntu, Debian)

## Requirements:
- ANY.RUN API-Key
- Microsoft Sentinel
- Azure Logic App (Flex Consumption plan)
- Azure Blob Storage
- Microsoft Defender for Endpoint (**Optional**)

## Solution overview

The connector consists of two Azure Logic Apps: 
- Parent workflow (varies depending on the host operating system):
  - [ANYRUN-Sandbox-File-Windows](https://github.com/rollehfoh/ANY.RUN/blob/main/connectors/Microsoft/Microsoft%20Sentinel/ANYRUN-Sandbox-File/Logic%20Apps/ANYRUN-Sandbox-File-Windows.json)
  - [ANYRUN-Sandbox-File-Ubuntu](https://github.com/rollehfoh/ANY.RUN/blob/main/connectors/Microsoft/Microsoft%20Sentinel/ANYRUN-Sandbox-File/Logic%20Apps/ANYRUN-Sandbox-File-Ubuntu.json)
  - [ANYRUN-Sandbox-File-Debian](https://github.com/rollehfoh/ANY.RUN/blob/main/connectors/Microsoft/Microsoft%20Sentinel/ANYRUN-Sandbox-File/Logic%20Apps/ANYRUN-Sandbox-File-Debian.json)
- Child workflow (uniform for all operating systems):
  - [ANYRUN-Submit-File-to-Blob](https://github.com/rollehfoh/ANY.RUN/blob/main/connectors/Microsoft/Microsoft%20Sentinel/ANYRUN-Sandbox-File/Logic%20Apps/ANYRUN-Submit-File-to-Blob.json)

## Logic Apps description

### Parent Workflow
This Logic App serves as the main orchestration workflow for the connector. It is triggered by a Microsoft Sentinel incident webhook and processes file entities associated with the incident. The workflow submits files for analysis in ANY.RUN Sandbox obtained from Azure Blob Storage. 

### Child Workflow

This Logic App is a child workflow invoked by the parent to handle file upload from hosts to Azure Blob Storage using Microsoft Defender for Endpoint. It is triggered by an HTTP request from the parent and parses input data. For each file, it initiates MDE live response to execute a script on the host for upload file to Azure Blob Storage.

 > **Note:** The child playbook in this connector is designed to extract files from the endpoint and upload them to Azure Blob Storage using Microsoft Defender for Endpoint (MDE). If you use a different solution instead of MDE, you can replace this playbook with one adapted for your infrastructure.
>
> If you are still using MDE to protect your devices, we recommend using the template of our connector **[Microsoft Sentinel & Microsoft Defender for Endpoint](https://github.com/rollehfoh/ANY.RUN/tree/main/connectors/Microsoft/Microsoft%20Sentinel/ANYRUN-Sandbox-Defender)**.

## Deployment

### Import Azure Logic App template

#### Child Logic App

First, you need to deploy the child Logic App, as its parameters are required for configuring the parent one.

- Click below to deploy Child Azure Logic App with **Flex Consumption plan**
 
[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Frollehfoh%2FANY.RUN%2Fmain%2Fconnectors%2FMicrosoft%2FMicrosoft%2520Sentinel%2FANYRUN-Sandbox-File%2FLogic%2520Apps%2FANYRUN-Submit-File-to-Blob.json)

- Enter the parameters required for deploying the Logic App and click **Review + create**.

![child_logic_app_deployment](images/004.png)

- Description of the required parameters:

| Parameter Name                  | Description                                                                 |
|---------------------------------|-----------------------------------------------------------------------------|
| LogicAppName                    | Workflow name.                                                              |
| AzureTenantId                   | Tenant ID for authentication in connections.                                |
| AzureClientId                   | Client ID for authentication (ID of the App Registration created before).   |
| azureClientSecret               | Client Secret for authentication.                                           |
| logAnalyticsWorkspaceName       | Log Analytics Workspace Name.                                               |

#### Parent Logic App 

> **Note:** You can deploy all the proposed parent Logic Apps or select specific ones depending on the operating system installed on your endpoints. The parent Logic Apps operate independently of each other.

- Click below to deploy Parent Azure Logic App with **Flex Consumption plan**
  - ANYRUN-Sandbox-File-Windows
[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Frollehfoh%2FANY.RUN%2Fmain%2Fconnectors%2FMicrosoft%2FMicrosoft%2520Sentinel%2FANYRUN-Sandbox-File%2FLogic%2520Apps%2FANYRUN-Sandbox-File-Windows.json)
  - ANYRUN-Sandbox-File-Ubuntu
[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Frollehfoh%2FANY.RUN%2Fmain%2Fconnectors%2FMicrosoft%2FMicrosoft%2520Sentinel%2FANYRUN-Sandbox-File%2FLogic%2520Apps%2FANYRUN-Sandbox-File-Ubuntu.json)
  - ANYRUN-Sandbox-File-Debian
[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Frollehfoh%2FANY.RUN%2Fmain%2Fconnectors%2FMicrosoft%2FMicrosoft%2520Sentinel%2FANYRUN-Sandbox-File%2FLogic%2520Apps%2FANYRUN-Sandbox-File-Debian.json)

- Enter the parameters required for deploying the Logic App and click **Review + create**.

![parent_logic_app_deployment](images/005.png)

- Description of the required parameters:

| Parameter Name              | Description                                                                 |
|-----------------------------|-----------------------------------------------------------------------------|
| logicAppName                | Workflow name.                                                              |
| azureTenantId               | Azure Tenant ID for authentication in connections.                          |
| azureClientId               | Client ID for authentication (ID of the App Registration created before).   |
| azureClientSecret           | Client Secret for authentication.                                           |
| keyVaultName                | Key Vault name.                                                             |
| keyVaultUri                 | Key Vault URI (copy Vault URI from your Key Vault overview).                |
| azureBlobStorageAccountName | Azure Blob Storage Account Name.                                            |
| azureBlobStorageContainerName | Azure Blob Storage Container Name.                                        |
| childWorkflowName           | Name of the child Logic App.                                                |

## Storage Account Configuration

To generate an SAS token for Azure Blob Storage, you need to assign the appropriate role directly to the Logic App.

- Open your Storage Account.

- Navigate to **Access Control (IAM)** and click Add.

![storage_child_logic_app](images/006.png)

- Specify the child Logic App `ANYRUN-Submit-File-to-Blob`.

- Select the following role:

| Name                       | Description                                                                 |
|----------------------------|-----------------------------------------------------------------------------|
| Storage Account Contributor | Lets you manage storage accounts, including accessing storage account keys which provide full access to storage account data. |

## Logic App configuration (Optional)

### ANY.RUN Sandbox analysis parameters

ANY.RUN is an interactive online malware analysis service for dynamic and static research of most types of threats using any environments. We offer a connector for Microsoft Sentinel, which you can independently adapt to your infrastructure and needs in just a few clicks. You can easily change the parameters used for analyzing the required File.

> **Note:** You can learn more about the capabilities of ANY.RUN Sandbox by reviewing our **[API documentation](https://any.run/api-documentation/)**.

The main setup and customization of the Logic App is available through the graphical editor (**Development tools** > **Logic app designer**) or the code editor (**Development tools** > **Logic app code view**).

- The File analysis parameters in ANY.RUN Sandbox are defined in the **HTTP - Submit File to ANY.RUN Sandbox Windows** action.

![analysis_action](images/001.png)

- Analysis options are specified in the HTTP request body.

 > **Note:** HTTP request body consists of multipart/form-data

![analysis_parameters](images/002.png)

- Description of the default parameters:

| Parameter Name              | Description                                                                 |
|-----------------------------|-----------------------------------------------------------------------------|
| opt_timeout                 | Defines the timeout option for the analysis.                                |
| env_os                      | Specifies the operating system.                                             |
| env_bitness                 | Defines the bitness of the operating system.                                |
| env_version                 | Sets the version of the operating system.                                   |
| env_type                    | Specify the environment preset type.                                        |
| opt_automated_interactivity | Controls the automated interactivity (ML) option (changing this is not recommended). |
| auto_confirm_uac            | Enables automatic confirmation of Windows UAC requests (changing this is not recommended). |
| run_as_root                 | Allow the file to run with superuser privileges on Linux.                   |
| obj_ext_extension           | Specify whether to change the file extension to a valid one.                |

### Simultaneous Analysis of Objects in ANY.RUN Sandbox

ANY.RUN Sandbox allows users to perform multiple analyses simultaneously (availability and capability depend on your pricing plan). By default, if a Microsoft Sentinel incident contains multiple Files, each analysis will run sequentially (a new File analysis won't start until the previous one finishes, to avoid errors).

- To increase the speed of incident enrichment, you can analyze objects simultaneously. To do this, open the **For each - detonate files to ANY.RUN Sandbox** loop > **Settings** and increase the **Degree of parallelism** value. It is recommended to set a value that does not exceed the number of possible parallel analyses in ANY.RUN Sandbox for your pricing plan.

![parallel_analysis](images/003.png)

> **Note**: To upgrade your pricing plan capabilities, [contact us](https://app.any.run/contact-us).
