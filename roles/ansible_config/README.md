# infra.aap_configuration.ansible_config

## Description

An Ansible Role to create ansible.cfg files based on your Automation Hub servers

## Requirements

ansible-galaxy collection install -r tests/collections/requirements.yml to be installed
Currently:
  awx.awx

## Variables

|Variable Name|Default Value|Required|Description|Example|
|:---:|:---:|:---:|:---:|:---:|
|`ansible_config_mode`|'0644'|no|str|The permissions the resulting ansible config file or directory should have.|
|`ansible_config_owner`|""|no|str|The owner the resulting ansible config file or directory should have.|
|`ansible_config_group`|""|no|str|The group the resulting ansible config file or directory should have.|
|`aap_configuration_working_dir`|"/var/tmp"|no|path|Location to render the ansible config file to.|
|`automation_hub_list`|`[]`|no|list|A list of Automation hubs and galaxies to put in the ansible config, see below for details.|
|`ansible_config_list`|`[{"header":"galaxy","keypairs":[{"key":"ignore_certs","value":"{{ not (aap_validate_certs \| bool) }}"}]}]`|no|list|A set of ansible config settings, a default is set, but can be overridden, see below for details.|
|`ah_token`|""|no|Tower Admin User's token on the Automation Hub Server.  This should be stored in an Ansible Vault at or elsewhere and called from a parent playbook.||
|`ah_path_prefix`|`galaxy`|no|Tower Admin User's token on the Automation Hub Server.  This should be stored in an Ansible Vault at or elsewhere and called from a parent playbook.||

### Secure Logging Variables

The following Variables compliment each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to false as normally the ansible config task does not by default include sensitive information, we highly recommend the use of ansible vault for passwords and tokens.
aap_configuration_ansible_config_secure_logging defaults to the value of aap_configuration_secure_logging if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of automation hub configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`aap_configuration_ansible_config_secure_logging`|`false`|no|Whether or not to include the sensitive ansible config role tasks in the log.  Set this value to `true` if you will be providing your sensitive values from elsewhere.|
|`aap_configuration_secure_logging`|`false`|no|This variable enables secure logging as well, but is shared across multiple roles, see above.|

## Data Structures

### automation_hub_list

|Variable Name|Default Value|Required|Type|Description|
|:---:|:---:|:---:|:---:|:---:|
|`name`|""|yes|str|Name of the Automation Hub or Galaxy Server.|
|`url`|""|yes|str|URL to the Automation Hub or Galaxy Server|
|`auth_url`|""|no|str|URL to the authentication for Automation Hub or Galaxy Server|
|`token`|""|no|str|Automation Hub or Galaxy Server token.|

### ansible_config_list

|Variable Name|Default Value|Required|Type|Description|
|:---:|:---:|:---:|:---:|:---:|
|`header`|""|yes|str|Header of the section that contains keypairs.|
|`keypairs`|`[]`|no|list|List key value pairs for settings in the ansible.cfg.|

### ansible_config_list[].keypairs

|Variable Name|Default Value|Required|Type|Description|
|:---:|:---:|:---:|:---:|:---:|
|`key`|""|yes|str|Key for entry under this header.|
|`value`|""|yes|str|Value for entry for the corresponding key.|

### Standard Project Data Structure

#### Yaml Example

```yaml
---
ansible_config_list:
  - header: galaxy
    keypairs:
      - key: ignore_certs
        value: "{{ not (aap_validate_certs | bool) }}"
      - key: server_list
        value: "{{ automation_hub_list | map(attribute='name') | join(',') }}"

automation_hub_list:
  - name: automation_hub
    url: "{{ah_host}}/api/automation-hub/content/0000001-synclist/"
    auth_url: https://sso.redhat.com/auth/realms/redhat-external/protocol/openid-connect/token
    token: changeme
```

## Playbook Examples

### Standard Role Usage

```yaml
---
- name: Set up Ansible Configuration for usage with PAH
  hosts: localhost
  connection: local
  gather_facts: false
  vars:
    aap_validate_certs: false
  # Define following vars here, or in ah_configs/ah_auth.yml
  # ah_host: ansible-ah-web-svc-test-project.example.com
  # ah_token: changeme
  pre_tasks:
    - name: Include vars from ah_configs directory
      ansible.builtin.include_vars:
        dir: ./vars
        extensions: ["yml"]
      tags:
        - always
  roles:
    - infra.aap_configuration.ansible_config
```

## License

[GPLv3+](https://github.com/ansible/galaxy_collection#licensing)

## Author

[Sean Sullivan](https://github.com/sean-m-sullivan/)
