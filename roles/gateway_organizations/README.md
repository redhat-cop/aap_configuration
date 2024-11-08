# Ansible Role infra.aap_configuration.organizations

## Description

An Ansible Role to add Organizations on Ansible Automation gateway.

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
|`aap_organizations`|`see below`|yes|Data structure describing your organizations Described below.||

### Secure Logging Variables

The following Variables compliment each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to false as normally the add ee_registry task does not include sensitive information.
aap_organizations_secure_logging defaults to the value of aap_configuration_secure_logging if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of automation hub configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`aap_organizations_secure_logging`|`false`|no|Whether or not to include the sensitive Registry role tasks in the log.  Set this value to `true` if you will be providing your sensitive values from elsewhere.|
|`aap_configuration_secure_logging`|`false`|no|This variable enables secure logging as well, but is shared across multiple roles, see above.|

### Asynchronous Retry Variables

The following Variables set asynchronous retries for the role.
If neither of the retries or delay or retries are set, they will default to their respective defaults.
This allows for all items to be created, then checked that the task finishes successfully.
This also speeds up the overall role.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`aap_configuration_async_retries`|50|no|This variable sets the number of retries to attempt for the role globally.|
|`aap_organizations_async_retries`|`aap_configuration_async_retries`|no|This variable sets the number of retries to attempt for the role.|
|`aap_configuration_async_delay`|1|no|This sets the delay between retries for the role globally.|
|`aap_organizations_async_delay`|`aap_configuration_async_delay`|no|This sets the delay between retries for the role.|
|`aap_configuration_loop_delay`|1000|no|This variable sets the loop_delay for the role globally.|
|`aap_organizations_loop_delay`|`aap_configuration_loop_delay`|no|This variable sets the loop_delay for the role.|
|`aap_configuration_async_dir`|`null`|no|Sets the directory to write the results file for async tasks. The default value is set to `null` which uses the Ansible Default of `/root/.ansible_async/`.|

## Data Structure

### Organization Arguments

Options for the `aap_organizations` variable:

| Variable Name | Default Value | Required | Type | Description                                                                      |
|:--------------|:-------------:|:--------:|:----:|:---------------------------------------------------------------------------------|
| `name`        |      N/A      |   yes    | str  | The name of the resource                                                         |
| `new_name`    |      N/A      |    no    | str  | Setting this option will change the existing name (looked up via the name field) |
| `description` |      N/A      |    no    | str  | Description of the organization                                                  |
| `state`       |   `present`   |    no    | str  | Desired state of the resource.                                                   |

### Unique value

- `name`

## Usage

### Json Example

- Create 2 Organizations

```json
{
  "aap_organizations": [
    {
      "name": "Org 1",
      "description": "First Organization"
    },
    {
      "name": "Org 2"
    }
  ]
}
```

### Yaml Example

- Check that "Deprecated Org" doesn't exist
- Check that Org 1 exists
- Get or create Org 2
- Rename Org 3

File name: `data/aap_organizations.yml`

```yaml
---
aap_organizations:
- name: "Deprecated Org"
  state: absent
- name: Org 1
  state: exists
- name: Org 2
- name: Org 3
  new_name: Organization 3
```

### Run Playbook

File name: [manage_data.yml](../../README.md#example-ansible-playbook) can be found in the top-level README.

```shell
ansible-playbook manage_data.yml -e @data/aap_organizations.yml
```

## License

[GPL-3.0](https://github.com/redhat-cop/aap_configuration#licensing)
