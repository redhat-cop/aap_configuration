# Ansible Role infra.aap_configuration.role_user_assignments

## Description

An Ansible Role to give a user permission to a resource like an organization.

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
|`gateway_role_user_assignments`|`see below`|yes|Data structure describing your gateway_role_user_assignment Described below.||

### Secure Logging Variables

The following Variables compliment each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to false as normally the add ee_registry task does not include sensitive information.
gateway_role_user_assignments_secure_logging defaults to the value of aap_configuration_secure_logging if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of automation hub configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`gateway_role_user_assignments_secure_logging`|`false`|no|Whether or not to include the sensitive Registry role tasks in the log.  Set this value to `true` if you will be providing your sensitive values from elsewhere.|
|`aap_configuration_secure_logging`|`false`|no|This variable enables secure logging as well, but is shared across multiple roles, see above.|

### Asynchronous Retry Variables

The following Variables set asynchronous retries for the role.
If neither of the retries or delay or retries are set, they will default to their respective defaults.
This allows for all items to be created, then checked that the task finishes successfully.
This also speeds up the overall role.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`aap_configuration_async_retries`|50|no|This variable sets the number of retries to attempt for the role globally.|
|`gateway_role_user_assignments_async_retries`|`aap_configuration_async_retries`|no|This variable sets the number of retries to attempt for the role.|
|`aap_configuration_async_delay`|1|no|This sets the delay between retries for the role globally.|
|`gateway_role_user_assignments_async_delay`|`aap_configuration_async_delay`|no|This sets the delay between retries for the role.|
|`aap_configuration_loop_delay`|1000|no|This variable sets the loop_delay for the role globally.|
|`gateway_role_user_assignments_loop_delay`|`aap_configuration_loop_delay`|no|This variable sets the loop_delay for the role.|
|`aap_configuration_async_dir`|`null`|no|Sets the directory to write the results file for async tasks. The default value is set to `null` which uses the Ansible Default of `/root/.ansible_async/`.|

## Data Structure

### Role User Assignments Arguments

Options for the `role_user_assignments` variable:

| Variable Name       | Default Value | Required | Type | Description                                                                                           |
|:--------------------|:-------------:|:--------:|:----:|:------------------------------------------------------------------------------------------------------|
| `role_definition`   |      N/A      |   yes    | str  | The name or id of the role definition to assign to the user.                                          |
| `user`              |      N/A      |    no    | str  | The username or id of the user to assign to the object.                                               |
| `user_ansible_id`   |      N/A      |    no    | str  | Resource id of the user who will receive permissions from this assignment. Alternative to user field. |
| `object_id`         |      N/A      |    no    | int  | Primary key of the object this assignment applies to.                                                 |
| `object_ansible_id` |      N/A      |    no    | str  | Resource id of the object this role applies to. Alternative to the object_id field.                   |
| `state`             |   `present`   |    no    | str  | Desired state of the resource.                                                                        |

**Unique value:**

- [`user`, `object_id`] (`*_ansible_id` alternatives can be provided)

## Usage

### Json Example

- Assign Organization Member role (object_id is an organization with ID 1)

```json
{
  "gateway_role_user_assignments": [
    {
      "role_definition": "Organization Member",
      "user": "Bob",
      "object_id": "1",
    }
  ]
}
```

### Yaml Example

- Assign Team Admin role (object_id is a team with ID 10)

File name: `data/gateway_role_user_assignments.yml`

```yaml
---
gateway_role_user_assignments:
- role_definition: Team Admin
  user: 1
  object_id: 10
```

### Run Playbook

File name: [manage_data.yml](../../README.md#example-ansible-playbook) can be found in the top-level README.

```shell
ansible-playbook manage_data.yml -e @data/gateway_role_user_assignments.yml
```

## License

[GPL-3.0](https://github.com/redhat-cop/aap_configuration#licensing)
