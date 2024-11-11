# infra.aap_configuration.hub_group

## Description

An Ansible Role to create groups in Automation Hub.

## Variables

|Variable Name|Default Value|Required|Description|Example|
|:---:|:---:|:---:|:---:|:---:|
|`aap_hostname`|""|yes|URL to the Ansible Automation Platform Server.|127.0.0.1|
|`aap_username`|""|no|Admin User on the Ansible Automation Platform Server. Either username / password or oauthtoken need to be specified.||
|`aap_password`|""|no|Platform Admin User's password on the Server.  This should be stored in an Ansible Vault at vars/platform-secrets.yml or elsewhere and called from a parent playbook.||
|`aap_validate_certs`|`true`|no|Whether or not to validate the Ansible Automation Platform Server's SSL certificate.||
|`aap_request_timeout`|`10`|no|Specify the timeout Ansible should use in requests to the Galaxy or Automation Hub host.||
|`ah_path_prefix`|""|no|API path used to access the api. Either galaxy, automation-hub, or custom||
|`aap_configuration_async_dir`|`null`|no|Sets the directory to write the results file for async tasks. The default value is set to `null` which uses the Ansible Default of `/root/.ansible_async/`.||
|`ah_groups`|`see below`|yes|Data structure describing your groups, described below.||

### Secure Logging Variables

The following Variables compliment each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to false as normally the add group task does not include sensitive information.
hub_configuration_group_secure_logging defaults to the value of aap_configuration_secure_logging if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of automation hub configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`hub_configuration_group_secure_logging`|`false`|no|Whether or not to include the sensitive Namespace role tasks in the log.  Set this value to `true` if you will be providing your sensitive values from elsewhere.|
|`aap_configuration_secure_logging`|`false`|no|This variable enables secure logging as well, but is shared across multiple roles, see above.|

### Asynchronous Retry Variables

The following Variables set asynchronous retries for the role.
If neither of the retries or delay or retries are set, they will default to their respective defaults.
This allows for all items to be created, then checked that the task finishes successfully.
This also speeds up the overall role.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`aap_configuration_async_retries`|50|no|This variable sets the number of retries to attempt for the role globally.|
|`hub_configuration_group_async_retries`|`aap_configuration_async_retries`|no|This variable sets the number of retries to attempt for the role.|
|`aap_configuration_loop_delay`|1000|no|This variable sets the loop_delay for the role globally.|
|`hub_configuration_group_loop_delay`|`aap_configuration_loop_delay`|no|This variable sets the loop_delay for the role.|
|`aap_configuration_async_delay`|1|no|This sets the delay between retries for the role globally.|
|`hub_configuration_group_async_delay`|`aap_configuration_async_delay`|no|This sets the delay between retries for the role.|

## Data Structure

### Group Variables

|Variable Name|Default Value|Required|Type|Description|
|:---:|:---:|:---:|:---:|:---:|
|`name`|""|yes|str|Group Name. Must be lower case containing only alphanumeric characters and underscores.|
|`perms`|""|yes|str|The list of permissions to add to or remove from the given group. See below for options.|
|`state`|`present`|no|str|Desired state of the group.|
<!-- |`new_name`|""|yes|str|Setting this option will change the existing name (looked up via the name field.| -->
#### perms

The module accepts the following roles:

- For user management, `add_user`, `change_user`, `delete_user`, and `view_user`.
- For group management, `add_group`, `change_group`, `delete_group`, and `view_group`.
- For collection namespace management, `add_namespace`, `change_namespace`, `upload_to_namespace`, and `delete_namespace`.
- For collection content management, `modify_ansible_repo_content`, and `delete_collection`.
- For remote repository configuration, `change_collectionremote` and `view_collectionremote`.
- For container image management, only with private automation hub v4.3.2
  or later, `change_containernamespace_perms`, `change_container`,
  `change_image_tag`, `create_container`, `push_container`, and `delete_containerrepository`.
- For task management, `change_task`, `view_task`, and `delete_task`.
- You can also grant or revoke all permissions with `*` or `all`.

### Standard Project Data Structure

#### Yaml Example

```yaml
---
ah_groups:
  - name: group1
    state: present
```

## Playbook Examples

### Standard Role Usage

```yaml
---
- name: Add group to Automation Hub
  hosts: localhost
  connection: local
  gather_facts: false
  vars:
    aap_validate_certs: false
  # Define following vars here, or in ah_configs/ah_auth.yml
  # ah_host: ansible-ah-web-svc-test-project.example.com
  pre_tasks:
    - name: Include vars from ah_configs directory
      ansible.builtin.include_vars:
        dir: ./vars
        extensions: ["yml"]
      tags:
        - always
  roles:
    - infra.aap_configuration.hub_group
```

## License

[GPLv3+](https://github.com/ansible/galaxy_collection#licensing)

## Author

[Tom Page](https://github.com/Tompage1994/)
