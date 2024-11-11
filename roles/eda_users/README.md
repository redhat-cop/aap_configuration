# infra.aap_configuration.aap_user_accounts

## Description

An Ansible Role to create users in EDA Controller.

## Variables

|Variable Name|Default Value|Required|Description|Example|
|:---|:---:|:---:|:---|:---|
|`platform_state`|"present"|no|The state all objects will take unless overridden by object default|'absent'|
|`aap_hostname`|""|yes|URL to the Ansible Automation Platform Server.|127.0.0.1|
|`aap_validate_certs`|`true`|no|Whether or not to validate the Ansible Automation Platform Server's SSL certificate.||
|`aap_username`|""|no|Admin User on the Ansible Automation Platform Server. Either username / password or oauthtoken need to be specified.||
|`aap_password`|""|no|Platform Admin User's password on the Server.  This should be stored in an Ansible Vault at vars/platform-secrets.yml or elsewhere and called from a parent playbook.||
|`aap_token`|""|no|Controller Admin User's token on the Ansible Automation Platform Server. This should be stored in an Ansible Vault at or elsewhere and called from a parent playbook. Either username / password or oauthtoken need to be specified.||
|`aap_request_timeout`|`10`|no|Specify the timeout in seconds Ansible should use in requests to the controller host.||
|`aap_user_accounts`|`see below`|yes|Data structure describing your users Described below.||

### Secure Logging Variables

The following Variables compliment each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to false as normally the add group_roles task does not include sensitive information.
eda_configuration_users_secure_logging defaults to the value of aap_configuration_secure_logging if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of automation hub configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`eda_configuration_users_secure_logging`|`false`|no|Whether or not to include the sensitive Registry role tasks in the log.  Set this value to `true` if you will be providing your sensitive values from elsewhere.|
|`aap_configuration_secure_logging`|`false`|no|Whether or not to include the sensitive Registry role tasks in the log.  Set this value to `true` if you will be providing your sensitive values from elsewhere.|

### Asynchronous Retry Variables

The following Variables set asynchronous retries for the role.
If neither of the retries or delay or retries are set, they will default to their respective defaults.
This allows for all items to be created, then checked that the task finishes successfully.
This also speeds up the overall role.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`aap_configuration_async_retries`|50|no|This variable sets the number of retries to attempt for the role globally.|
|`eda_configuration_users_secure_logging`|`aap_configuration_async_retries`|no|This variable sets the number of retries to attempt for the role.|
|`aap_configuration_async_delay`|1|no|This sets the delay between retries for the role globally.|
|`eda_configuration_users_async_retries`|`aap_configuration_async_delay`|no|This sets the delay between retries for the role.|
|`aap_configuration_loop_delay`|1000|no|This variable sets the loop_delay for the role globally.|
|`eda_configuration_users_async_delay`|`aap_configuration_loop_delay`|no|This variable sets the loop_delay for the role.|
|`aap_configuration_async_dir`|`null`|no|Sets the directory to write the results file for async tasks. The default value is set to `null` which uses the Ansible Default of `/root/.ansible_async/`.|

## Data Structure

### user Variables

|Variable Name|Default Value|Required|Type|Description|
|:---:|:---:|:---:|:---:|:---:|
|`username`|""|yes|str|Username. Must contain only letters, numbers, and `@.+-_` characters.|
|`new_username`|""|no|str|Setting this option will change the existing username (looked up via the name field.)|
|`first_name`|""|no|str|First ame of the user.|
|`last_name`|""|no|str|Last name of the user.|
|`email`|""|no|str|User's email address.|
|`password`|""|yes|str|Password to use for the user.|
|`update_secrets`|true|no|bool|Setting true will always change password if user specifies password. Password will only change if false if other fields change.|
|`is_superuser`|""|no|bool|Make user as superuser.|
|`roles`|""|yes|list|Roles the user will have. Current acceptable values are: Viewer, Auditor, Editor, Contributor, Operator, Admin.|
|`state`|`present`|no|str|Desired state of the user.|

### Standard user Data Structure

#### Yaml Example

```yaml
---
eda_users:
- username: jane_doe
  first_name: Jane
  last_name: Doe
  email: jdoe@example.com
  password: my_password1
  update_secrets: false
  roles:
    - Auditor
    - Contributor
```

## Playbook Examples

### Standard Role Usage

```yaml
---
- name: Add user to EDA Controller
  hosts: localhost
  connection: local
  gather_facts: false
  vars:
    eda_validate_certs: false
  # Define following vars here, or in eda_configs/eda_auth.yml
  # controller_host: ansible-eda-web-svc-test-user.example.com
  # eda_token: changeme
  pre_tasks:
    - name: Include vars from eda_configs directory
      ansible.builtin.include_vars:
        dir: ./vars
        extensions: ["yml"]
      tags:
        - always
  roles:
    - infra.aap_configuration.eda_users
```

## License

[GPLv3+](https://github.com/redhat-cop/eda_configuration#licensing)

## Author

[Tom Page](https://github.com/Tompage1994/)
