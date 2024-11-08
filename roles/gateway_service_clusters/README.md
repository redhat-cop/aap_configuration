# Ansible Role infra.aap_configuration.service_clusters

## Description

An Ansible Role to configure Service Clusters on Ansible Automation gateway.

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
|`gateway_service_clusters`|`see below`|yes|Data structure describing your gateway_service_clusters Described below.||

### Secure Logging Variables

The following Variables compliment each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to false as normally the add ee_registry task does not include sensitive information.
gateway_service_clusters_secure_logging defaults to the value of aap_configuration_secure_logging if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of automation hub configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`gateway_service_clusters_secure_logging`|`false`|no|Whether or not to include the sensitive Registry role tasks in the log.  Set this value to `true` if you will be providing your sensitive values from elsewhere.|
|`aap_configuration_secure_logging`|`false`|no|This variable enables secure logging as well, but is shared across multiple roles, see above.|

### Asynchronous Retry Variables

The following Variables set asynchronous retries for the role.
If neither of the retries or delay or retries are set, they will default to their respective defaults.
This allows for all items to be created, then checked that the task finishes successfully.
This also speeds up the overall role.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`aap_configuration_async_retries`|50|no|This variable sets the number of retries to attempt for the role globally.|
|`gateway_service_clusters_async_retries`|`aap_configuration_async_retries`|no|This variable sets the number of retries to attempt for the role.|
|`aap_configuration_async_delay`|1|no|This sets the delay between retries for the role globally.|
|`gateway_service_clusters_async_delay`|`aap_configuration_async_delay`|no|This sets the delay between retries for the role.|
|`aap_configuration_loop_delay`|1000|no|This variable sets the loop_delay for the role globally.|
|`gateway_service_clusters_loop_delay`|`aap_configuration_loop_delay`|no|This variable sets the loop_delay for the role.|
|`aap_configuration_async_dir`|`null`|no|Sets the directory to write the results file for async tasks. The default value is set to `null` which uses the Ansible Default of `/root/.ansible_async/`.|

## Data Structure

### Service Cluster Arguments

Options for the `gateway_service_nodes` variable:

| Variable Name  | Default Value |      Required      | Type | Description                                                                             |
|:---------------|:-------------:|:------------------:|:----:|:----------------------------------------------------------------------------------------|
| `name`         |      N/A      |        yes         | str  | The name of the resource                                                                |
| `new_name`     |      N/A      |         no         | str  | Setting this option will change the existing name (looked up via the name field)        |
| `service_type` |      N/A      | state is 'present' | str  | The type of service for this cluster. Choices : ["hub", "controller", "eda", "gateway"] |
| `state`        |   `present`   |         no         | str  | README.md#state-variable)                                                  |

**Unique value:**

- `name`
- `service_type`

## Usage

### Json Example

- Check that Controller and EDA (Event Driven Automation) services are deleted (if present) (from the database):
- Check that gateway service exists (in the database)

```json
{
  "platform_state": "absent",
  "gateway_service_clusters": [
    {
      "name": "Automation Controller"
    },
    {
      "name": "Event Driven Automation"
    },
    {
      "name": "AAP gateway",
      "state": "exists"
    }
  ]
}
```

### Yaml Example

- Create or update Controller Service (in the database)
- CHeck that Service with ID 3 exists
- Renames Hub service

File name: `data/service_clusters.yml`

```yaml
---
gateway_service_clusters:
- name: "Automation Controller"
  service_type: controller
  state: present
- name: 3
  state: exists
- name: "Automation Hub"
  new_name: "Ansible Galaxy"
  ```

## License

[GPL-3.0](https://github.com/redhat-cop/aap_configuration#licensing)
