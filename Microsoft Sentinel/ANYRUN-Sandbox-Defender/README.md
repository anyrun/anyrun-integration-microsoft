<p align="center">
    <a href="#readme">
        <img alt="ANY.RUN logo" src="https://raw.githubusercontent.com/anyrun/anyrun-sdk/b3dfde1d3aa018d0a1c3b5d0fa8aaa652e80d883/static/logo.svg">
    </a>
</p>

______________________________________________________________________

# ANY.RUN Malware Sandbox Integration with Microsoft Sentinel and Defender for Endpoint for automated file and URL analysis

## Overview

This template makes the incident enrichment process in Microsoft Sentinel even more automated if you are also using Microsoft Defender for Endpoint (MDE). 
In this case, the entire automation mechanism can be combined into Azure Logic App and Azure Function App, leveraging MDE's capabilities to extract files from UNIX- or Windows-endpoints using the bash and PowerShell script we offer.

This Logic App allows you to send URLs and files contained in the incident entities for analysis in ANY.RUN Sandbox. The playbook enables initiating Live Response sessions to hosts connected to Microsoft Defender for Endpoint. Within these Live Response sessions, a script is launched that extracts files from the endpoint and sends them for temporary storage to an Azure Blob Storage container. Once the file arrives in Blob Storage, the Logic App retrieves it and forwards it for analysis to ANY.RUN API.

After the analysis is completed in ANY.RUN Sandbox, its key results (verdict, score, and tags) enrich the incident. They help you obtain more detailed information on your sample. Additionally, IOCs discovered during the analysis in ANY.RUN Sandbox will be added to the Sentinel TI Portal.

## Requirements:
- ANY.RUN API-Key
- Microsoft Sentinel
- Azure Logic App (Flex Consumption plan)
- Azure Function App (Flex Consumption plan)
- Azure Blob Storage
- Microsoft Defender for Endpoint

## Deployment

### Deploy Azure Logic App template

- Click below to deploy Azure Logic App with **Flex Consumption plan**

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fanyrun%2Fanyrun-integration-microsoft%2Fmain%2FMicrosoft%2520Sentinel%2FANYRUN-Sandbox-Defender%2FANYRUN-Sandbox-Defender.json)

- Enter the parameters required for deploying the Logic App.

![logic_app_deployment](images/011.png)

- Description of the required parameters:

| Parameter Name                   | Description                                                                 |
|----------------------------------|-----------------------------------------------------------------------------|
| logicAppName                     | Workflow Name.                                                              |
| azureTenantId                    | Azure Tenant ID for authentication.                                         |
| azureClientId                    | Azure Client ID for authentication.                                         |
| azureClientSecret                | Azure Client Secret for authentication.                                     |
| keyVaultName                     | Key Vault name.                                                             |
| keyVaultUri                      | Key Vault URI.                                                              |
| azureBlobStorageAccountName      | Azure Blob Storage Account Name.                                            |
| azureBlobStorageConnectionString | Azure Blob Storage Connection String.                                       |
| azureBlobStorageContainerName    | Azure Blob Storage Container Name.                                          |
| logAnalyticsWorkspaceName        | Log Analytics Workspace Name.                                               |
| functionAppName                  | Name of the Function App to call (deployed before).                         |

## Storage Account Configuration

To generate an SAS token for Azure Blob Storage, you need to assign the appropriate role directly to the Logic App.

- Open your Storage Account.

- Navigate to **Access Control (IAM)** and click Add.

![storage_logic_app](images/010.png)

- Specify the Logic App `ANYRUN-Sandbox-Defender`.

- Select the following role:

| Name                       | Description                                                                 |
|----------------------------|-----------------------------------------------------------------------------|
| Storage Account Contributor | Lets you manage storage accounts, including accessing storage account keys which provide full access to storage account data. |

## Microsoft Defender for Endpoint configuration and additional script

> **Note:** To allow the connector to extract all files of interest from endpoints (including potentially dangerous ones), we recommend setting `Quarantine` as the default action for your MDE. **!ATTENTION!** Be careful when configuring antivirus policies, as this can be potentially dangerous. See:
>
> - [Configure remediation for Microsoft Defender Antivirus detections](https://learn.microsoft.com/en-us/defender-endpoint/configure-remediation-microsoft-defender-antivirus)
>
> - [Settings for Microsoft Defender Antivirus policy in Microsoft Intune for Windows devices](https://learn.microsoft.com/en-us/intune/intune-service/protect/antivirus-microsoft-defender-settings-windows)

### Enable Live Response Sessions

- Open your [MDE portal](https://security.microsoft.com).

- Navigate to **System** > **Settings** > **Endpoints** > **General** > **Advanced features**.

- Enable the following settings: **Live Response**, **Live Response for Servers**, and **Live Response unsigned script execution**.

![enable_live_response](images/002.png)

### Upload Helper Scripts to the Local Library of Your Endpoints

- Open your MDE portal[](https://security.microsoft.com).

- Navigate to **Assets** > **Devices**.

- Open the required device.

- Click on `...` in the upper right corner and then **Initiate Live Response Session**.

![run_live_response](images/003.png)

- Click **Upload file to library**.

![click_upload_file](images/004.png)

- Click **Upload file to library** again, select the script from your file system (after downloading it from our [library](https://github.com/anyrun/anyrun-integration-microsoft/tree/main/Microsoft%20Sentinel/ANYRUN-Sandbox-Defender/scripts)), or create your own script. After that, click **Submit**.

![select_file_to_upload](images/005.png)

### Declaring Script Names in the Deployed Logic App (Optional)

The Logic App we propose dynamically selects the script extension (.sh or .ps1) depending on the endpoint's operating system. If you need to run a script with a different name from the local library, you can change it in the Logic App.

- Open the deployed **ANYRUN-Sandbox-Defender** Logic App.

- Navigate to **Development Tools** > **Logic app designer**.

- In the Logic app designer, expand the following action blocks: **For each - Host** > **For each - Find file path on the target host** > **Condition - Check if KQL Result is not empty (True)** > **Condition - Windows Machine**.

- In the expanded condition, select the actions **Set variable - Windows OS Script Name** and **Set variable - UNIX OS Script Name** and change the script name to the one you need. Additionally, you might also need to change the script launch parameters in the actions **Set variable - Windows OS Script Parameters** and **Set variable - UNIX OS Script Parameters**. 

![change_script_name](images/006.png)

## Logic App configuration (Optional)

### ANY.RUN Sandbox analysis parameters

ANY.RUN is an interactive online malware analysis service for dynamic and static research of most types of threats using a customizable VM environment. We offer a connector for Microsoft Sentinel, which you can independently adapt to your infrastructure and needs in just a few clicks. You can easily change the parameters used for analyzing the required file.

> **Note:** You can learn more about the capabilities of ANY.RUN Sandbox by reviewing our **[API documentation](https://any.run/api-documentation/)**.

The main setup and customization of the Logic App is available through the graphical editor (**Development tools** > **Logic app designer**) or the code editor (**Development tools** > **Logic app code view**).

- The analysis parameters in ANY.RUN Sandbox are defined in the actions of the deployed Logic App.

- For URL analysis - `HTTP-RunNewURLAnalysis`

![analysis_action_url](images/007.png)

- For File analysis - in the following three actions which are responsible for declaring the parameters:

  - `ANY.RUN general analysis options`

  - `ANY.RUN Windows analysis options`

  - `ANY.RUN Linux analysis options`

![analysis_parameters_file](images/018.png)

- In the `ANY.RUN general analysis options` action, you can modify parameters that define general, OS-independent options such as analysis duration, virtual machine network settings, privacy, and more. For example, if you need to **increase the initial analysis time** for a more detailed examination of the object, select the **opt_timeout** variable and set the desired value in seconds, for example `360`.

![general_parametrs_actions](images/019.png)

- In the `ANY.RUN Windows analysis options` and `ANY.RUN Linux analysis options` actions, you can modify parameters that affect OS-specific virtual machine settings, such as the OS version and configuration, initial object location and launch parameters, and more. For example, if you need to run the analysis on a virtual machine with Windows 11 instead of Windows 10, click on the `ANY.RUN Windows analysis options` action, select the **windows_env_version** variable, and set the value to `11`.

![os_parametrs_actions](images/020.png)

- Description of the main parameters:

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

ANY.RUN Sandbox allows users to perform multiple analyses simultaneously (availability and capability depend on your pricing plan). By default, if a Microsoft Sentinel incident contains multiple files, each analysis will run sequentially (a new file analysis won't start until the previous one is finished).

- To increase the speed of incident enrichment, you can analyze objects simultaneously. To do this, open `For each - URLs` and `For each - detonate files to ANY.RUN Sandbox` loop > `Settings` and increase the `Degree of parallelism` value. Note that you should set a value that does not exceed the number of parallel analyses available at your pricing plan.

![parallel_analysis](images/009.png)

> **Note**: To expand your capabilities by upgrading your pricing plan, [contact us](https://app.any.run/contact-us/?utm_source=anyrungithub&utm_medium=documentation&utm_campaign=sentinel&utm_content=linktocontactus).
