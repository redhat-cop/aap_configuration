# Ansible Role infra.aap_configuration.authenticator_maps

## Description

An Ansible Role to add Authenticator Maps on Ansible Automation gateway.

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
|`gateway_authenticator_maps`|`see below`|yes|Data structure describing your gateway_authenticator_maps Described below.||

### Secure Logging Variables

The following Variables compliment each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to false as normally the add ee_registry task does not include sensitive information.
gateway_authenticator_maps_secure_logging defaults to the value of aap_configuration_secure_logging if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of automation hub configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`gateway_authenticator_maps_secure_logging`|`false`|no|Whether or not to include the sensitive Registry role tasks in the log.  Set this value to `true` if you will be providing your sensitive values from elsewhere.|
|`aap_configuration_secure_logging`|`false`|no|This variable enables secure logging as well, but is shared across multiple roles, see above.|

### Asynchronous Retry Variables

The following Variables set asynchronous retries for the role.
If neither of the retries or delay or retries are set, they will default to their respective defaults.
This allows for all items to be created, then checked that the task finishes successfully.
This also speeds up the overall role.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`aap_configuration_async_retries`|50|no|This variable sets the number of retries to attempt for the role globally.|
|`gateway_authenticator_maps_async_retries`|`aap_configuration_async_retries`|no|This variable sets the number of retries to attempt for the role.|
|`aap_configuration_async_delay`|1|no|This sets the delay between retries for the role globally.|
|`gateway_authenticator_maps_async_delay`|`aap_configuration_async_delay`|no|This sets the delay between retries for the role.|
|`aap_configuration_loop_delay`|1000|no|This variable sets the loop_delay for the role globally.|
|`gateway_authenticator_maps_loop_delay`|`aap_configuration_loop_delay`|no|This variable sets the loop_delay for the role.|
|`aap_configuration_async_dir`|`null`|no|Sets the directory to write the results file for async tasks. The default value is set to `null` which uses the Ansible Default of `/root/.ansible_async/`.|

## Data Structure

### Authenticator Map Arguments

Options for the `authenticator_maps_list` variable:

| Variable Name       |  Default Value  | Required | Type | Description                                                                                                                                 |
|:--------------------|:---------------:|:--------:|:----:|:--------------------------------------------------------------------------------------------------------------------------------------------|
| `name`              |       N/A       |   yes    | str  | The name of the resource                                                                                                                    |
| `new_name`          |       N/A       |    no    | str  | Setting this option will change the existing name (looked up via the name field)                                                            |
| `authenticator`     |       N/A       |   yes    | str  | The name or ID referencing the [Authenticator](../gateway_authenticators/README.md)                                                                 |
| `new_authenticator` |       N/A       |    no    | str  | The name or ID referencing newly associated authenticator                                                                                   |
| `revoke`            |     `false`     |    no    | bool | If a user does not meet this rule should we revoke the permission                                                                           |
| `map_type`          |     `team`      |    no    | str  | What does the map work on, a team, a user flag or is this an allow rule. choices: ["allow", "is_superuser", "team", "organization", "role"] |
| `role`              |       N/A       |    no    | str  | The name of RBAC Role Definition  to be used for this map                                                                                   |
| `team`              |       N/A       |    no    | str  | A team name this rule works on                                                                                                              |
| `organization`      |       N/A       |    no    | str  | An organization name this rule works on                                                                                                     |
| `triggers`          |      `{}`       |    no    | dict | Trigger information for this rule                                                                                                           |
| `order`             | N/A(`0` by API) |    no    | int  | The order in which this rule should be processed, smaller numbers are of higher precedence                                                  |
| `state`             |    `present`    |    no    | str  | Desired state of the resource.                                                                                                              |

### Unique value

- [`name`, `authenticator`]

## Usage

### Json Example

- Creates 1 authenticator map with map_type == 'organization' => requires value for "organization"
- Creates 1 authenticator map with map_type == 'team' => requires values for "team" and "organization"

```json
{
  "gateway_authenticator_maps": [
    {
      "name": "AMap-1",
      "authenticator": "Authenticator-1",
      "revoke": false,
      "map_type": "organization",
      "organization": "Organization 1",
      "triggers": {
        "always": {},
        "never": {}
      },
      "order": 10
    },
    {
      "name": "AMap-2",
      "authenticator": "Authenticator-2",
      "map_type": "team",
      "team": "Team 1",
      "organization": "Organization 1",
      "role": "Team Member",
      "triggers": {
        "never": {}
      }
    }
  ]
}
```

### Yaml Example

- Creates Authenticator Map with examples of triggers structure
- Renames Authenticator Map and changes Authenticator

```yaml
---
gateway_authenticator_maps:
- name: AuthMap 1
  authenticator: Auth 1
  revoke: true
  map_type: organization
  organization: Organization 1
  role: Organization Admin
  triggers:
    always: { }
    never: { }
    groups:
      has_or:
      - has_or_11
      - has_or_22
      has_and:
      - has_and_1
      - has_and_22
    attributes:
      join_condition: "or"
      attr_1:
        contains: aaa
        matches: "bbb"
        ends_with: "ccc"
      attr_2:
        in:
        - abc1
        - abc2
        - abc3
- name: "AuthMapX"
  new_name: "Authenticator Map X"
  authenticator: "Auth"
  new_authenticator: "Auth 2"
```

### Run Playbook

File name: [manage_data.yml](../../README.md#example-ansible-playbook) can be found in the top-level README.

```shell
ansible-playbook manage_data.yml -e @data/gateway_authenticator_maps.yml
```

## License

[GPL-3.0](https://github.com/redhat-cop/aap_configuration#licensing)
