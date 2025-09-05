<p align="center">
    <a href="#readme">
        <img alt="ANY.RUN logo" src="https://raw.githubusercontent.com/anyrun/anyrun-sdk/b3dfde1d3aa018d0a1c3b5d0fa8aaa652e80d883/static/logo.svg">
    </a>
</p>

______________________________________________________________________

# Microsoft Sentinel Connectors for ANY.RUN Malware Sandbox

## Overview

This repository contains the necessary resources for integrating Microsoft Sentinel with the ANY.RUN Sandbox. The connectors enrich Microsoft Sentinel incidents by analyzing URLs or files associated with them in the ANY.RUN Sandbox.

As a result, your Microsoft Sentinel incidents will include a verdict, threat score, malware tags and a link to the detailed analysis in the ANY.RUN UI, allowing you to explore the object's behavior in a real infrastructure environment. Additionally, your Threat Intelligence portal in Sentinel will be enriched with Indicators of Compromise (IoCs) extracted during the sandbox analysis.

## Connector capabilities
- Incident enrichment:
  - Analysis Verdict and Threat score
  - Malware Tags
  - Table with IoC's detected during the analysis
  - Analysis Report Link
- Uploading IoC's detected during the analysis to Sentinel Threat Intelligence portal

## Analyze URLs from Microsoft Sentinel Incidents via ANY.RUN Sandbox

This playbook extracts URL from incidents and submit it for analysis in the ANY.RUN Sandbox to enrich the incident with a verdict using a single Azure Logic App.

[Open connector page](https://github.com/rollehfoh/ANY.RUN/tree/main/connectors/Microsoft/Microsoft%20Sentinel/ANYRUN-Sandbox-URL)

## Analyze Files from Microsoft Sentinel Incidents via ANY.RUN Sandbox

This playbook allows you to send files from incidents for analysis in the ANY.RUN Sandbox. It uploads the file from the endpoint to Azure Blob Storage and then forwards it to the ANY.RUN Sandbox using an Azure Logic App.

Templates are provided for endpoints running the following operating systems:
- Windows
- UNIX (Ubuntu, Debian)

[Open connector page](https://github.com/rollehfoh/ANY.RUN/tree/main/connectors/Microsoft/Microsoft%20Sentinel/ANYRUN-Sandbox-File)

## Analyze All Entities from Microsoft Sentinel Incidents via ANY.RUN Sandbox and Microsoft Defender for Endpoint

This template makes the incident enrichment process in Microsoft Sentinel even more automated if you are also using Microsoft Defender for Endpoint (MDE). In this case, the entire automation mechanism can be combined into a single Azure Logic App, leveraging MDE's capabilities to extract files from endpoints via API.

[Open connector page](https://github.com/rollehfoh/ANY.RUN/tree/main/connectors/Microsoft/Microsoft%20Sentinel/ANYRUN-Sandbox-Defender)

## Prerequisites

### Key Vault

- You need the Hunter pricing plan in ANY.RUN and your API key. We recommend storing your API key in Azure Key Vault. To do this, select your existing Key Vault or create a new one. Then, navigate to the **Objects** > **Secrets** section and create a new secret named `ANYRUN-APIKey`.

  > **Note:** It is recommended to keep this name unchanged, as otherwise, you will need to update it later in the deployed Logic App.

![key_vault](images/001.png)

### App Registration

- You need to create a new application for your connector. To do this, go to **Microsoft Entra ID**.

![entra_id](images/002.png)

- Click **Add** > **App registration**.

![app_registration](images/003.png)

- Name your new application and click **Register**.

![register_app](images/004.png)

### API Permissions for new App

#### Key Vault API Permissions

- For the created application, add the following permissions for API connections in the **Manage** > **API permissions** > **Add a permission** tab:

![add_permission](images/007.png)

- In the **Microsoft APIs** tab, add **Azure Key Vault**.

![add_vault_permission](images/005.png)

- Add the following permissions for it:

| Category | Permission Name   | Description                                                                 |
|----------|-------------------|-----------------------------------------------------------------------------|
| N/A      | user_impersonation | Allow the application full access to the Azure Key Vault service on behalf of the signed-in user |

#### Microsoft Defender ATP API Permissions

  > **Note:** This article is only required for workflows where you use Microsoft Defender for Endpoint (MDE) to extract files from the endpoint.

- Add an API connection for **WindowsDefenderATP**. Select the corresponding API in the **APIs my organization uses** tab.

![select_defender_permission](images/008.png)

- Then, select **Application permissions**.

![add_defender_permission](images/009.png)

- Select the following permissions:

| Category | Permission Name    | Description                                                                 |
|----------|--------------------|-----------------------------------------------------------------------------|
| Machine  | Machine.LiveResponse | Needed to gather evidences from machines                                  |
| Machine  | Machine.Read.All   | Needed to retrieve information about machines                               |
| Library  | Library.Manage     | Needed to upload custom ps1 script for retrieving AV related evidences      |

### Required Roles for the New App

Since the connectors use various resources available in Azure, the created application `ANYRUN-App` needs to be assigned the appropriate roles.

#### Key Vault

- Navigate to the required Key Vault where you previously added the ANY.RUN API-Key.

![kv_role_overview](images/018.png)

- Open **Access control (IAM)** > **Add** > **Add role assignment**.

![kv_role_add](images/019.png)

- In the search window, type and select the role **Key Vault Secrets User**, then click **Next**.

![kv_role_search](images/020.png)

- Description of the required role:

| Name                   | Description                                                                 |
|------------------------|-----------------------------------------------------------------------------|
| Key Vault Secrets User | Read secret contents. Only works for key vaults that use the 'Azure role-based access control' permission model. |

- Then, assign this role to the created application **ANYRUN-App**.

![kv_role_select](images/021.png)

#### Sentinel

- Open your Sentinel workspace and navigate to **Settings** > **Workspace settings**.

![sentinel_settings](images/022.png)

- Open **Access control (IAM)** > **Add** > **Add role assignment**.

![sentinel_role_add](images/023.png)

- In the search window, type and select the roles **Microsoft Sentinel Contributor** and **Log Analytics Contributor**, then click **Next**.

![sentinel_role_search](images/024.png)

- Description of the required roles:

| Name                         | Description                                                                 |
|------------------------------|-----------------------------------------------------------------------------|
| Microsoft Sentinel Contributor | Microsoft Sentinel Contributor                                              |
| Log Analytics Contributor    | Log Analytics Contributor can read all monitoring data and edit monitoring settings. Editing monitoring settings includes adding the VM extension to VMs; reading storage account keys to be able to configure collection of logs from Azure Storage; adding solutions; and configuring Azure diagnostics on all Azure resources. |

- Then, assign these roles to the created application **ANYRUN-App**.

![sentinel_role_select](images/025.png)

### Storage Account

  > **Note:** This article is only required for workflows where you use Azure Blob Storage to keeping file from the endpoint before submitting it to ANY.RUN Sandbox.

- Go to Azure Storage Accounts.

![azure_sa](images/010.png)

- Click **Create**.

![azure_sa_create](images/011.png)

- Type the name of Storage Account and click **Review + Create**.

![azure_sa_review_and_create](images/012.png)

- After that you should open your Storage Account and go to **Access Control (IAM)** > **Add**.

![sa_iam_add](images/013.png)

- Select your App `ANYRUN-App`.

![sa_app_select](images/014.png)

- Find the following roles:

![sa_role_find](images/015.png)

| Role                          | Description                                                                 |
|-------------------------------|-----------------------------------------------------------------------------|
| Storage Account Contributor   | Lets you manage storage accounts, including accessing storage account keys which provide full access to storage account data. |
| Storage Blob Data Contributor | Allows for read, write and delete access to Azure Storage blob containers and data. |

- Open your Storage Account. Go to **Data Storage** > **Containers**.

![sa_navigation](images/016.png)

- Click **Add container**, type the **Name** for it and **Create**.

![sa_container_create](images/017.png)

### Deployment

- After completing the preliminary settings above, you can proceed to deploy the Azure Logic Apps necessary for integrating Microsoft Sentinel and ANY.RUN Sandbox:
  - [ANYRUN-Sandbox-URL](https://github.com/rollehfoh/ANY.RUN/tree/main/connectors/Microsoft/Microsoft%20Sentinel/ANYRUN-Sandbox-URL)
  - [ANYRUN-Sandbox-File](https://github.com/rollehfoh/ANY.RUN/tree/main/connectors/Microsoft/Microsoft%20Sentinel/ANYRUN-Sandbox-File)
  - [ANYRUN-Sandbox-Defender](https://github.com/rollehfoh/ANY.RUN/tree/main/connectors/Microsoft/Microsoft%20Sentinel/ANYRUN-Sandbox-Defender)

## Request Support or Access to ANY.RUN’s Products

Feel free to reach out to us for help with integration, a quote, or a demo via the [contact us form](https://app.any.run/contact-us).
