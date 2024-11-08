# Ansible Role infra.aap_configuration.authenticators

## Description

An Ansible Role to add Authenticators on Ansible Automation gateway.

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
|`gateway_authenticators`|`see below`|yes|Data structure describing your gateway_authenticators Described below.||

### Secure Logging Variables

The following Variables compliment each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to false as normally the add ee_registry task does not include sensitive information.
gateway_authenticators_secure_logging defaults to the value of aap_configuration_secure_logging if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of automation hub configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`gateway_authenticators_secure_logging`|`false`|no|Whether or not to include the sensitive Registry role tasks in the log.  Set this value to `true` if you will be providing your sensitive values from elsewhere.|
|`aap_configuration_secure_logging`|`false`|no|This variable enables secure logging as well, but is shared across multiple roles, see above.|

### Asynchronous Retry Variables

The following Variables set asynchronous retries for the role.
If neither of the retries or delay or retries are set, they will default to their respective defaults.
This allows for all items to be created, then checked that the task finishes successfully.
This also speeds up the overall role.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`aap_configuration_async_retries`|50|no|This variable sets the number of retries to attempt for the role globally.|
|`gateway_authenticators_async_retries`|`aap_configuration_async_retries`|no|This variable sets the number of retries to attempt for the role.|
|`aap_configuration_async_delay`|1|no|This sets the delay between retries for the role globally.|
|`gateway_authenticators_async_delay`|`aap_configuration_async_delay`|no|This sets the delay between retries for the role.|
|`aap_configuration_loop_delay`|1000|no|This variable sets the loop_delay for the role globally.|
|`gateway_authenticators_loop_delay`|`aap_configuration_loop_delay`|no|This variable sets the loop_delay for the role.|
|`aap_configuration_async_dir`|`null`|no|Sets the directory to write the results file for async tasks. The default value is set to `null` which uses the Ansible Default of `/root/.ansible_async/`.|

## Data Structure

### Authenticator Arguments

Options for the `authenticators_list` variable:

| Variable Name    |    Default Value    | Required | Type | Description                                                                                                                  |
|:-----------------|:-------------------:|:--------:|:----:|:-----------------------------------------------------------------------------------------------------------------------------|
| `name`           |         N/A         |   yes    | str  | The name of the resource                                                                                                     |
| `new_name`       |         N/A         |    no    | str  | Setting this option will change the existing name (looked up via the name field)                                             |
| `slug`           |         N/A         |    no    | str  | An immutable identifier for the authenticator                                                                                |
| `enabled`        | N/A(`false` by API) |    no    | bool | Enable/Disable the authenticator                                                                                             |
| `create_objects` | N/A(`true` by API)  |    no    | bool | Allow authenticator to create objects (users, teams, organizations)                                                          |
| `remove_users`   | N/A(`true` by API)  |    no    | bool | When a user authenticates from this source should they be removed from any other groups they were previously added to        |
| `configuration`  |         N/A         |    no    | dict | The required configuration for this source (dict keys specified by the module in 'type')                                     |
| `type`           |         N/A         |    no    | str  | The type of authentication service this is. Can be one of the modules: `ansible_base.authentication.authenticator_plugins.*` |
| `order`          |  N/A (`1` by API)   |    no    | int  | The order in which an authenticator will be tried. This only pertains to username/password authenticators                    |
| `state`          |      `present`      |    no    | str  | Desired state of the resource.                                                                                               |

### Unique value

- `name`
- `slug` (can't be used as an identificator)

## Usage

### Json Example

- Creates local authenticator
- Renames authenticator

```json
{
  "gateway_authenticators": [
    {
      "name": "local authenticator",
      "slug": "local-authenticator",
      "type": "ansible_base.authentication.authenticator_plugins.local",
      "enabled": true,
      "configuration": {}
    },
    {
      "name": "github authenticator",
      "new_name": "New GitHub Authenticator"
    }
  ]
}
```

### Yaml Example

- Deletes 1 authenticator
- Creates an AzureAD authenticator with configuration provided by the `ansible_base.authentication.authenticator_plugins.azuread` module
  - configuration class can be found in [in ansible-django-base](https://github.com/ansible/django-ansible-base/tree/devel/ansible_base/authentication/authenticator_plugins)

File name: `data/gateway_authenticators.yml`

```yaml
---
gateway_authenticators:
- name: "Deprecated Authenticator"
  state: absent
- name: Auth AzureAD
  type: 'ansible_base.authentication.authenticator_plugins.azuread'
  slug: authenticator-azuread
  enabled: true
  configuration:
    CALLBACK_URL: 'https://127.0.0.1'
    KEY: 'oidc-key'
    SECRET: 'oidc-secret'
```

### Run Playbook

File name: [manage_data.yml](../../README.md#example-ansible-playbook) can be found in the top-level README.

```shell
ansible-playbook manage_data.yml -e @data/gateway_authenticators.yml
```

## License

[GPL-3.0](https://github.com/redhat-cop/aap_configuration#licensing)
