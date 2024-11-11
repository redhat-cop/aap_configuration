# infra.aap_configuration.credential_types

## Description

An Ansible Role to create/update/remove Credential Types on Ansible Controller.

## Requirements

ansible-galaxy collection install -r tests/collections/requirements.yml to be installed
Currently:
  awx.awx
  or
  ansible.controller

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
|`controller_credential_types`|`see below`|yes|Data structure describing your credential types Described below. Alias: credential_types ||

### Enforcing defaults

The following Variables compliment each other.
If Both variables are not set, enforcing default values is not done.
Enabling these variables enforce default values on options that are optional in the controller API.
This should be enabled to enforce configuration and prevent configuration drift. It is recomended to be enabled, however it is not enforced by default.

Enabling this will enforce configurtion without specifying every option in the configuration files.

'controller_configuration_credential_types_enforce_defaults' defaults to the value of 'aap_configuration_enforce_defaults' if it is not explicitly called. This allows for enforced defaults to be toggled for the entire suite of controller configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`controller_configuration_credential_types_enforce_defaults`|`false`|no|Whether or not to enforce default option values on only the applications role|
|`aap_configuration_enforce_defaults`|`false`|no|This variable enables enforced default values as well, but is shared across multiple roles, see above.|

### Secure Logging Variables

The following Variables compliment each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to false as normally the add credential type task does not include sensitive information.
controller_configuration_credential_types_secure_logging defaults to the value of aap_configuration_secure_logging if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`controller_configuration_credential_types_secure_logging`|`false`|no|Whether or not to include the sensitive Credential Type role tasks in the log. Set this value to `true` if you will be providing your sensitive values from elsewhere.|
|`aap_configuration_secure_logging`|`false`|no|This variable enables secure logging as well, but is shared across multiple roles, see above.|

### Asynchronous Retry Variables

The following Variables set asynchronous retries for the role.
If neither of the retries or delay or retries are set, they will default to their respective defaults.
This allows for all items to be created, then checked that the task finishes successfully.
This also speeds up the overall role.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`aap_configuration_async_retries`|30|no|This variable sets the number of retries to attempt for the role globally.|
|`controller_configuration_credential_types_async_retries`|`aap_configuration_async_retries`|no|This variable sets the number of retries to attempt for the role.|
|`aap_configuration_async_delay`|1|no|This sets the delay between retries for the role globally.|
|`controller_configuration_credential_types_async_delay`|`aap_configuration_async_delay`|no|This sets the delay between retries for the role.|
|`aap_configuration_loop_delay`|0|no|This sets the pause between each item in the loop for the roles globally. To help when API is getting overloaded.|
|`controller_configuration_credential_types_loop_delay`|`aap_configuration_loop_delay`|no|This sets the pause between each item in the loop for the role. To help when API is getting overloaded.|
|`aap_configuration_async_dir`|`null`|no|Sets the directory to write the results file for async tasks. The default value is set to `null` which uses the Ansible Default of `/root/.ansible_async/`.|

## Data Structure

### Credential Type Variables

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`name`|""|yes|Name of Credential Type|
|`new_name`|""|no|Setting this option will change the existing name (looked up via the name field).|
|`description`|`false`|no|The description of the credential type to give more detail about it.|
|`injectors`|""|no|Enter injectors using either JSON or YAML syntax. Refer to the Ansible controller documentation for example syntax. See below on proper formatting.|
|`inputs`|""|no|Enter inputs using either JSON or YAML syntax. Refer to the Ansible controller documentation for example syntax.|
|`kind`|"cloud"|no|The type of credential type being added. Note that only cloud and net can be used for creating credential types.|
|`state`|`present`|no|Desired state of the resource.|

### Formating Injectors

Injectors use a standard Jinja templating format to describe the resource.

Example:

```json
{{ variable }}
```

Because of this it is difficult to provide controller with the required format for these fields.

The workaround is easier to do in yaml with unsafe syntax, to read more about this check out the [documentation](https://docs.ansible.com/ansible/latest/user_guide/playbooks_advanced_syntax.html):

```yaml
!unsafe '{{ variable }}'
```

If you want to use json you will have to use the following format:

```json
{  { variable }}
```

The role will strip the double space between the curly bracket in order to provide controller with the correct format for the Injectors.

### Input and Injector Schema

The following details the data format to use for inputs and injectors. These can be in either YAML or JSON For the most up to date information and more details see [Custom Credential Types - Ansible Controller Documentation](https://docs.ansible.com/automation-controller/latest/html/userguide/credential_plugins.html)

#### Input Schema

```yaml
fields:
  - type: string
    id: username
    label: Username
  - type: string
    id: password
    label: Password
    secret: true
required:
  - username
  - password
```

#### Injector Schema

```json
{
  "file": {
      "template": "[mycloud]\ntoken={{ api_token }}"
  },
  "env": {
      "THIRD_PARTY_CLOUD_API_TOKEN": "{{ api_token }}"
  },
  "extra_vars": {
      "some_extra_var": "{{ username }}:{{ password }}"
  }
}
```

### Standard Credential Type Data Structure

#### Json Example

```json
{
    "controller_credential_types": [
      {
        "name": "REST API Credential",
        "description": "REST API Credential",
        "kind": "cloud",
        "inputs": {
          "fields": [
            {
              "type": "string",
              "id": "rest_username",
              "label": "REST Username"
            },
            {
              "secret": true,
              "type": "string",
              "id": "rest_password",
              "label": "REST Password"
            }
          ],
          "required": [
            "rest_username",
            "rest_password"
          ]
        },
        "injectors": {
          "extra_vars": {
            "rest_password": "{  { rest_password }}",
            "rest_username": "{  { rest_username }}"
          },
          "env": {
            "rest_username_env": "{  { rest_username }}",
            "rest_password_env": "{  { rest_password }}"
          }
        }
      }
    ]
}
```

#### Yaml Example

```yaml
---
controller_credential_types:
- name: REST API Credential
  description: REST API Credential
  inputs:
    fields:
    - type: string
      id: rest_username
      label: REST Username
    - secret: true
      type: string
      id: rest_password
      label: REST Password
    required:
    - rest_username
    - rest_password
  injectors:
    extra_vars:
      rest_password: !unsafe "{{ rest_password }}"
      rest_username: !unsafe "{{ rest_username }}"
    env:
      rest_username_env: !unsafe "{{ rest_username }}"
      rest_password_env: !unsafe "{{ rest_password }}"
```

## Playbook Examples

### Standard Role Usage

```yaml
- name: Playbook to configure ansible controller post installation
  hosts: localhost
  connection: local
  # Define following vars here, or in platform_configs/controller_auth.yml
  # aap_hostname: ansible-controller-web-svc-test-project.example.com
  # aap_username: admin
  # aap_password: changeme
  pre_tasks:
    - name: Include vars from platform_configs directory
      ansible.builtin.include_vars:
        dir: ./yaml
        ignore_files: [controller_config.yml.template]
        extensions: ["yml"]
  roles:
    - {role: infra.aap_configuration.credential_types, when: controller_credential_types is defined}
```

## License

[GPL-3.0](https://github.com/redhat-cop/aap_configuration#licensing)

## Author

[Sean Sullivan](https://github.com/sean-m-sullivan)
