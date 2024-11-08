# Ansible Role infra.aap_configuration.service_keys

## Description

An Ansible Role to configure Service Keys on Ansible Automation gateway.

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
|`gateway_service_keys`|`see below`|yes|Data structure describing your gateway_service_keys Described below.||

### Secure Logging Variables

The following Variables compliment each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to false as normally the add ee_registry task does not include sensitive information.
gateway_service_keys_secure_logging defaults to the value of aap_configuration_secure_logging if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of automation hub configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`gateway_service_keys_secure_logging`|`false`|no|Whether or not to include the sensitive Registry role tasks in the log.  Set this value to `true` if you will be providing your sensitive values from elsewhere.|
|`aap_configuration_secure_logging`|`false`|no|This variable enables secure logging as well, but is shared across multiple roles, see above.|

### Asynchronous Retry Variables

The following Variables set asynchronous retries for the role.
If neither of the retries or delay or retries are set, they will default to their respective defaults.
This allows for all items to be created, then checked that the task finishes successfully.
This also speeds up the overall role.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`aap_configuration_async_retries`|50|no|This variable sets the number of retries to attempt for the role globally.|
|`gateway_service_keys_async_retries`|`aap_configuration_async_retries`|no|This variable sets the number of retries to attempt for the role.|
|`aap_configuration_async_delay`|1|no|This sets the delay between retries for the role globally.|
|`gateway_service_keys_async_delay`|`aap_configuration_async_delay`|no|This sets the delay between retries for the role.|
|`aap_configuration_loop_delay`|1000|no|This variable sets the loop_delay for the role globally.|
|`gateway_service_keys_loop_delay`|`aap_configuration_loop_delay`|no|This variable sets the loop_delay for the role.|
|`aap_configuration_async_dir`|`null`|no|Sets the directory to write the results file for async tasks. The default value is set to `null` which uses the Ansible Default of `/root/.ansible_async/`.|

## Data Structure

### Service Key Arguments

Options for the `gateway_service_keys` variable:

| Variable Name            |   Default Value    | Required | Type | Description                                                                      |
|:-------------------------|:------------------:|:--------:|:----:|:---------------------------------------------------------------------------------|
| `name`                   |        N/A         |   yes    | str  | The name of the resource                                                         |
| `new_name`               |        N/A         |    no    | str  | Setting this option will change the existing name (looked up via the name field) |
| `is_active`              | N/A (true by API)  |    no    | bool | Flag for setting the active state of the Service Key                             |
| `service_cluster`        |        N/A         |    no    | str  | ID or name referencing the [Service Cluster](../gateway_service_clusters/README.md)      |
| `algorithm`              | N/A (HS256 by API) |    no    | str  | Algorithm to use for this Service Key. Choices: ["HS256", "HS384", "HS512"]      |
| `secret`                 |        N/A         |    no    | str  | A secret to use for this Service Key. Non-editable                               |
| `secret_length`          |        N/A         |    no    | int  | The number of random bytes in the secret                                         |
| `mark_previous_inactive` |        N/A         |    no    | bool | If true any other secret keys for this service will become inactive              |
| `state`                  |     `present`      |    no    | str  | README.md#state-variable)                                           |

**Unique value:**

- `name`

## Usage

### Json Example

- Check the service key exists (in the database):
- Create a service key

```json
{
  "gateway_service_keys": [
    {
      "name": "Key 1",
      "state": "exists"
    },
    {
      "name": "Key 2",
      "algorithm": "HS512",
      "secret": "this-is-secret",
      "service_cluster": "Automation Controller"
    }
  ]
}
```

### Yaml Example

- Create inactive key for Controller service
- Delete key (if exists)

File name: `data/gateway_service_keys.yml`

```yaml
---
gateway_service_keys:
- name: "Controller Key 1"
  is_active: false
  service_cluster: controller
  secret: "gateway-secret"
- name: "Some secret key"
  state: absent
```

## License

[GPL-3.0](https://github.com/redhat-cop/aap_configuration#licensing)
