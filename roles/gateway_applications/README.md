# Ansible Role infra.aap_configuration.applications

## Description

An Ansible Role to create/update/remove Applications on Ansible gateway.

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
|`aap_applications`|`see below`|yes|Data structure describing your aap_applications Described below.||

### Enforcing defaults

The following Variables compliment each other.
If Both variables are not set, enforcing default values is not done.
Enabling these variables enforce default values on options that are optional in the controller API.
This should be enabled to enforce configuration and prevent configuration drift. It is recomended to be enabled, however it is not enforced by default.

Enabling this will enforce configurtion without specifying every option in the configuration files.

'aap_applications_enforce_defaults' defaults to the value of 'aap_configuration_enforce_defaults' if it is not explicitly called. This allows for enforced defaults to be toggled for the entire suite of controller configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`aap_applications_enforce_defaults`|`false`|no|Whether or not to enforce default option values on only the applications role|
|`aap_configuration_enforce_defaults`|`false`|no|This variable enables enforced default values as well, but is shared globally.|

### Secure Logging Variables

The following Variables compliment each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to false as normally the add ee_registry task does not include sensitive information.
aap_applications_secure_logging defaults to the value of aap_configuration_secure_logging if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of automation hub configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`aap_applications_secure_logging`|`false`|no|Whether or not to include the sensitive Registry role tasks in the log.  Set this value to `true` if you will be providing your sensitive values from elsewhere.|
|`aap_configuration_secure_logging`|`false`|no|This variable enables secure logging as well, but is shared across multiple roles, see above.|

### Asynchronous Retry Variables

The following Variables set asynchronous retries for the role.
If neither of the retries or delay or retries are set, they will default to their respective defaults.
This allows for all items to be created, then checked that the task finishes successfully.
This also speeds up the overall role.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`aap_configuration_async_retries`|50|no|This variable sets the number of retries to attempt for the role globally.|
|`aap_applications_async_retries`|`aap_configuration_async_retries`|no|This variable sets the number of retries to attempt for the role.|
|`aap_configuration_async_delay`|1|no|This sets the delay between retries for the role globally.|
|`aap_applications_async_delay`|`aap_configuration_async_delay`|no|This sets the delay between retries for the role.|
|`aap_configuration_loop_delay`|1000|no|This variable sets the loop_delay for the role globally.|
|`aap_applications_loop_delay`|`aap_configuration_loop_delay`|no|This variable sets the loop_delay for the role.|
|`aap_configuration_async_dir`|`null`|no|Sets the directory to write the results file for async tasks. The default value is set to `null` which uses the Ansible Default of `/root/.ansible_async/`.|

## Data Structure

### Application Arguments

Options for the `aap_applications` variable:

| Variable Name               |    Default Value    | Required | Type | Description                                                                            |
|:----------------------------|:-------------------:|:--------:|:----:|:---------------------------------------------------------------------------------------|
| `name`                      |         N/A         |   yes    | str  | Name of application                                                                    |
| `new_name`                  |         N/A         |    no    | str  | Setting this option will change the existing name (looked up via the name field).      |
| `organization`              |         N/A         |   yes    | str  | Name of the organization for the application                                           |
| `new_organization`          |         N/A         |    no    | str  | The name or ID referencing newly associated organization                               |
| `algorithm`                 |         N/A         |    no    | str  | The OIDC token signing algorithm for this application. Choices: ["", "RS256", "HS256"] |
| `description`               |         N/A         |    no    | str  | Description to use for the application.                                                |
| `authorization_grant_type`  |         N/A         |   yes    | str  | Grant type for tokens in this application, Choices: ["password", "authorization-code"] |
| `client_type`               |         N/A         |   yes    | str  | Application client type. Choices: ["confidential", "public"]                           |
| `redirect_uris`             |         ""          |    no    | str  | Allowed urls list, space separated. Required with "authorization-code" grant type      |
| `skip_authorization`        | N/A(`false` by API) |   yes    | bool | Set true to skip authorization step for completely trusted applications.               |
| `post_logout_redirect_uris` |         ""          |    no    | str  | Allowed Post Logout URIs list, space separated.                                        |
| `user`                      |         ""          |    no    | str  | The user who owns this application.                                                    |
| `state`                     |      `present`      |    no    | str  | Desired state of the application.                                                      |

### Standard Application Data Structure

#### Json Example

```json
 {
  "aap_applications": [
    {
      "name": "gateway Config Default Application",
      "description": "Generic application, which can be used for oauth tokens",
      "organization": "Default",
      "state": "present",
      "client_type": "confidential",
      "authorization_grant_type": "password"
    }
  ]
}
```

#### Yaml Example

File name: `data/aap_applications.yml`

```yaml
---
aap_applications:
- name: "gateway Config Default Application"
  description: "Generic application, which can be used for oauth tokens"
  organization: "Default"
  state: "present"
  client_type: "confidential"
  authorization_grant_type: "password"
```

## License

[GPL-3.0](https://github.com/redhat-cop/aap_configuration#licensing)
