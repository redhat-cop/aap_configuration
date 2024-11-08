# Ansible Role infra.aap_configuration.service_nodes

## Description

An Ansible Role to configure Service Nodes on Ansible Automation gateway.

## Variables

|Variable Name|Default Value|Required|Description|Example|
|:---|:---:|:---:|:---|:---|
|`platform_state`|"present"|no|The state all objects will take unless overridden by object default|'absent'|
|`aap_hostname`|""|yes|URL to the Ansible Automation Platform Server.|127.0.0.1|
|`aap_validate_certs`|`true`|no|Whether or not to validate the Ansible Automation Platform Server's SSL certificate.||
|`aap_username`|""|no|Admin User on the Ansible Automation Platform Server. Either username / password or oauthtoken need to be specified.||
|`aap_password`|""|no|Platform Admin User's password on the Server.  This should be stored in an Ansible Vault at vars/platform-secrets.yml or elsewhere and called from a parent playbook.||
|`aap_token`|""|no|Controller Admin User's token on the Ansible Automation Platform Server. This should be stored in an Ansible Vault at or elsewhere and called from a parent playbook. Either username / password or oauthtoken need to be specified.||
|`aap_request_timeout`|`10`|no|Specify the timeout in seconds Ansible should use in requests to the Ansible Automation Platform host.||
|`gateway_service_nodes`|`see below`|yes|Data structure describing your gateway_service_nodes Described below.||

### Enforcing defaults

The following Variables compliment each other.
If Both variables are not set, enforcing default values is not done.
Enabling these variables enforce default values on options that are optional in the controller API.
This should be enabled to enforce configuration and prevent configuration drift. It is recomended to be enabled, however it is not enforced by default.

Enabling this will enforce configurtion without specifying every option in the configuration files.

'gateway_service_nodes_enforce_defaults' defaults to the value of 'aap_configuration_enforce_defaults' if it is not explicitly called. This allows for enforced defaults to be toggled for the entire suite of controller configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`gateway_service_nodes_enforce_defaults`|`false`|no|Whether or not to enforce default option values on only the applications role|
|`aap_configuration_enforce_defaults`|`false`|no|This variable enables enforced default values as well, but is shared globally.|

### Secure Logging Variables

The following Variables compliment each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to false as normally the add ee_registry task does not include sensitive information.
gateway_service_nodes_secure_logging defaults to the value of aap_configuration_secure_logging if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of automation hub configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`gateway_service_nodes_secure_logging`|`false`|no|Whether or not to include the sensitive Registry role tasks in the log.  Set this value to `true` if you will be providing your sensitive values from elsewhere.|
|`aap_configuration_secure_logging`|`false`|no|This variable enables secure logging as well, but is shared across multiple roles, see above.|

### Asynchronous Retry Variables

The following Variables set asynchronous retries for the role.
If neither of the retries or delay or retries are set, they will default to their respective defaults.
This allows for all items to be created, then checked that the task finishes successfully.
This also speeds up the overall role.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`aap_configuration_async_retries`|50|no|This variable sets the number of retries to attempt for the role globally.|
|`gateway_service_nodes_async_retries`|`aap_configuration_async_retries`|no|This variable sets the number of retries to attempt for the role.|
|`aap_configuration_async_delay`|1|no|This sets the delay between retries for the role globally.|
|`gateway_service_nodes_async_delay`|`aap_configuration_async_delay`|no|This sets the delay between retries for the role.|
|`aap_configuration_loop_delay`|1000|no|This variable sets the loop_delay for the role globally.|
|`gateway_service_nodes_loop_delay`|`aap_configuration_loop_delay`|no|This variable sets the loop_delay for the role.|
|`aap_configuration_async_dir`|`null`|no|Sets the directory to write the results file for async tasks. The default value is set to `null` which uses the Ansible Default of `/root/.ansible_async/`.|

## Data Structure

### Service Node Arguments

Options for the `service_nodes_list` variable:

| Variable Name     | Default Value | Required | Type | Description                                                                      |
|:------------------|:-------------:|:--------:|:----:|:---------------------------------------------------------------------------------|
| `name`            |      N/A      |   yes    | str  | The name of the resource                                                         |
| `new_name`        |      N/A      |    no    | str  | Setting this option will change the existing name (looked up via the name field) |
| `address`         |      N/A      |    no    | str  | Network address for this service                                                 |
| `service_cluster` |      N/A      |    no    | str  | ID or name referencing the [Service Cluster](../gateway_service_clusters/README.md)      |
| `tags`            |      N/A      |    no    | str  | Comma separated list of tags to assign to the node, for filtering route traffic  |
| `state`           |   `present`   |    no    | str  | README.md#state-variable)                                           |

**Unique value:**

- `name`
- `address` + `service_cluster`

## Usage

### Json Example

- Check the node on 10.0.0.1 for EDA service exists (in the database):
- Check the node with ID 1 exists (in the database):

```json
{
  "gateway_service_nodes": [
    {
      "name": "EDA - 10.0.0.1",
      "state": "exists"
    },
    {
      "name": 1,
      "state": "exists"
    }
  ]
}
```

### Yaml Example

- Create node (if not exists) for Controller service (in the database)
- Delete node (if exists) for Automation Hub Service (from the database)

File name: `data/service_nodes.yml`

```yaml
---
gateway_service_nodes:
- name: "Controller Node 1"
  address: 10.0.0.1
  service_cluster: controller
- name: "Hub on 10.0.1.1"
  state: absent
```

## License

[GPL-3.0](https://github.com/redhat-cop/aap_configuration#licensing)
