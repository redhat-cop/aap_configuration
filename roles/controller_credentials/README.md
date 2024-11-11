# infra.aap_configuration.credentials

## Description

An Ansible Role to create/update/remove Credentials on Ansible Controller.

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
|`controller_credentials`|`see below`|yes|Data structure describing your credentials Described below. Alias: credentials ||

### Enforcing defaults

The following Variables compliment each other.
If Both variables are not set, enforcing default values is not done.
Enabling these variables enforce default values on options that are optional in the controller API.
This should be enabled to enforce configuration and prevent configuration drift. It is recomended to be enabled, however it is not enforced by default.

Enabling this will enforce configurtion without specifying every option in the configuration files.

'controller_configuration_credentials_enforce_defaults' defaults to the value of 'aap_configuration_enforce_defaults' if it is not explicitly called. This allows for enforced defaults to be toggled for the entire suite of controller configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`controller_configuration_credentials_enforce_defaults`|`false`|no|Whether or not to enforce default option values on only the applications role|
|`aap_configuration_enforce_defaults`|`false`|no|This variable enables enforced default values as well, but is shared across multiple roles, see above.|

### Secure Logging Variables

The following Variables compliment each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to false as normally the add credentials task does not include sensitive information.
controller_configuration_credentials_secure_logging defaults to the value of aap_configuration_secure_logging if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`controller_configuration_credentials_secure_logging`|`false`|no|Whether or not to include the sensitive Credential role tasks in the log. Set this value to `true` if you will be providing your sensitive values from elsewhere.|
|`aap_configuration_secure_logging`|`false`|no|This variable enables secure logging as well, but is shared across multiple roles, see above.|

### Asynchronous Retry Variables

The following Variables set asynchronous retries for the role.
If neither of the retries or delay or retries are set, they will default to their respective defaults.
This allows for all items to be created, then checked that the task finishes successfully.
This also speeds up the overall role.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`aap_configuration_async_retries`|30|no|This variable sets the number of retries to attempt for the role globally.|
|`controller_configuration_credentials_async_retries`|`{{ aap_configuration_async_retries }}`|no|This variable sets the number of retries to attempt for the role.|
|`aap_configuration_async_delay`|1|no|This sets the delay between retries for the role globally.|
|`controller_configuration_credentials_async_delay`|`aap_configuration_async_delay`|no|This sets the delay between retries for the role.|
|`aap_configuration_loop_delay`|0|no|This sets the pause between each item in the loop for the roles globally. To help when API is getting overloaded.|
|`controller_configuration_credentials_loop_delay`|`aap_configuration_loop_delay`|no|This sets the pause between each item in the loop for the role. To help when API is getting overloaded.|
|`aap_configuration_async_dir`|`null`|no|Sets the directory to write the results file for async tasks. The default value is set to `null` which uses the Ansible Default of `/root/.ansible_async/`.|

## Data Structure

### Credential Variables

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`name`|""|yes|Name of Credential|
|`new_name`|""|no|Setting this option will change the existing name (looked up via the name field).|
|`copy_from`|""|no|Name or id to copy the credential from. This will copy an existing credential and change any parameters supplied.|
|`description`|`false`|no|Description of  of Credential.|
|`organization`|""|no|Organization this Credential belongs to. If provided on creation, do not give either user or team.|
|`credential_type`|""|no|Name of credential type. See below for list of options. More information in Ansible controller documentation. |
|`inputs`|""|no|Credential inputs where the keys are var names used in templating. Refer to the Ansible controller documentation for example syntax. Individual examples can be found at /api/v2/credential_types/ on an controller.|
|`user`|""|no|User that should own this credential. If provided, do not give either team or organization. |
|`team`|""|no|Team that should own this credential. If provided, do not give either user or organization. |
|`state`|`present`|no|Desired state of the resource.|
|`update_secrets`|true|no| true will always change password if user specifies password, even if API gives $encrypted$ for password. false will only set the password if other values change too.|

### Credential types

To get a list of all the available builtin credential types, checkout the ansible doc's link [here](https://docs.ansible.com/automation-controller/latest/html/userguide/credentials.html#credential-types)

### Standard Credential Data Structure

#### Json Example

```json

{
    "controller_credentials": [
      {
        "name": "gitlab",
        "description": "Credentials for GitLab",
        "organization": "Default",
        "credential_type": "Source Control",
        "inputs": {
          "username": "person",
          "password": "password"
        }
      }
    ]
}
```

#### Yaml Example

```yaml
---
controller_credentials:
- name: gitlab
  description: Credentials for GitLab
  organization: Default
  credential_type: Source Control
  inputs:
    username: person
    password: password
- name: hashivault
  description: HashiCorp Vault Secret Lookup example using token auth
  organization: Default
  credential_type: HashiCorp Vault Secret Lookup
  inputs:
    url: https://vault.example.com:8243
    token: token
    cacert: "{{ lookup('ansible.builtin.file', '/path/to/ca-certificates.crt') }}"
    api_version: v2
- name: localuser
  description: Machine Credential example with become_method input
  credential_type: Machine
  inputs:
    username: localuser
    password: password
    become_method: sudo
```

## Playbook Examples

### Standard Role Usage

```yaml
---
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
    - {role: infra.aap_configuration.credentials, when: controller_credentials is defined}
```

## License

[GPL-3.0](https://github.com/redhat-cop/aap_configuration#licensing)

## Author

[Andrew J. Huffman](https://github.com/ahuffman)
[Sean Sullivan](https://github.com/sean-m-sullivan)
