# infra.aap_configuration.notification_templates

## Description

An Ansible Role to add/update/remove notification templates on Ansible Controller.

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
|`controller_notifications`|`see below`|yes|Data structure describing your notification entries described below. Alias: notification_templates ||

### Enforcing defaults

The following Variables compliment each other.
If Both variables are not set, enforcing default values is not done.
Enabling these variables enforce default values on options that are optional in the controller API.
This should be enabled to enforce configuration and prevent configuration drift. It is recomended to be enabled, however it is not enforced by default.

Enabling this will enforce configurtion without specifying every option in the configuration files.

'controller_configuration_notifications_enforce_defaults' defaults to the value of 'aap_configuration_enforce_defaults' if it is not explicitly called. This allows for enforced defaults to be toggled for the entire suite of controller configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`controller_configuration_notifications_enforce_defaults`|`false`|no|Whether or not to enforce default option values on only the applications role|
|`aap_configuration_enforce_defaults`|`false`|no|This variable enables enforced default values as well, but is shared across multiple roles, see above.|

### Secure Logging Variables

The following Variables compliment each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to false as normally the add notification task does not include sensitive information.
`controller_configuration_notification_secure_logging` defaults to the value of `aap_configuration_secure_logging` if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`controller_configuration_notification_secure_logging`|`false`|no|Whether or not to include the sensitive notification role tasks in the log. Set this value to `true` if you will be providing your sensitive values from elsewhere.|
|`aap_configuration_secure_logging`|`false`|no|This variable enables secure logging as well, but is shared across multiple roles, see above.|

### Asynchronous Retry Variables

The following Variables set asynchronous retries for the role.
If neither of the retries or delay or retries are set, they will default to their respective defaults.
This allows for all items to be created, then checked that the task finishes successfully.
This also speeds up the overall role.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`aap_configuration_async_retries`|30|no|This variable sets the number of retries to attempt for the role globally.|
|`controller_configuration_notification_async_retries`|`{{ aap_configuration_async_retries }}`|no|This variable sets the number of retries to attempt for the role.|
|`aap_configuration_async_delay`|1|no|This sets the delay between retries for the role globally.|
|`controller_configuration_notification_async_delay`|`aap_configuration_async_delay`|no|This sets the delay between retries for the role.|
|`aap_configuration_loop_delay`|0|no|This sets the pause between each item in the loop for the roles globally. To help when API is getting overloaded.|
|`controller_configuration_notifications_loop_delay`|`aap_configuration_loop_delay`|no|This sets the pause between each item in the loop for the role. To help when API is getting overloaded.|
|`aap_configuration_async_dir`|`null`|no|Sets the directory to write the results file for async tasks. The default value is set to `null` which uses the Ansible Default of `/root/.ansible_async/`.|

## Data Structure

### Notification Variables

|Variable Name|Default Value|Required|Type|Description|
|:---:|:---:|:---:|:---:|:---:|
|`name`|""|yes|str|The name of the notification.|
|`new_name`|""|yes|str|Setting this option will change the existing name (looked up via the name field).|
|`copy_from`|""|no|str|Name or id to copy the Notification template from. This will copy an existing notification and change any parameters supplied.|
|`description`|""|no|str|The description of the notification.|
|`organization`|""|no|str|The organization applicable to the notification.|
|`notification_type`|""|no|str|The type of notification to be sent.|
|`notification_configuration`|""|no|str|The notification configuration file. Note providing this field would disable all depreciated notification-configuration-related fields.|
|`messages`|""|no|list|Optional custom messages for notification template. Assumes any instance of two space __ are used for adding variables and removes them. Does not effect single space.|
|`state`|`present`|no|str|Desired state of the resource.|

### Standard Notification Data Structure

#### Json Example

```json
{
  "controller_notifications": [
    {
      "name": "irc-satqe-chat-notification",
      "description": "Notify us on job in IRC!",
      "organization": "Satellite",
      "notification_type": "irc",
      "notification_configuration": {
        "use_tls": false,
        "use_ssl": false,
        "password": "",
        "port": 6667,
        "server": "irc.freenode.com",
        "nickname": "Ansible-controller-Stage-Bot-01",
        "targets": [
          "#my-channel"
        ]
      }
    },
    {
      "name": "Email notification",
      "description": "Send out emails for controller jobs",
      "organization": "Satellite",
      "notification_type": "email",
      "notification_configuration": {
        "username": "",
        "sender": "controller0@example.com",
        "recipients": [
          "admin@example.com"
        ],
        "use_tls": false,
        "host": "smtp.example.com",
        "use_ssl": false,
        "password": "",
        "port": 25
      }
    }
  ]
}
```

#### Yaml Example

```yaml
---
controller_notifications:
  - name: irc-satqe-chat-notification
    description: Notify us on job in IRC!
    organization: Satellite
    notification_type: irc
    notification_configuration:
      use_tls: false
      use_ssl: false
      password: ''  # this is required even if there's no password
      port: 6667
      server: irc.freenode.com
      nickname: Ansible-controller-Stage-Bot-01
      targets:
      - "#my-channel"
    messages:
      success:
        body: '{"fields": {"project": {"id": "11111"},"summary": "Lab {  { job.status
          }} Ansible controller {  { job.name }}","description": "{  { job.status }} in {  {
          job.name }} {  { job.id }} {  {url}}","issuetype": {"id": "1"}}}'
  - name: Email notification
    description: Send out emails for controller jobs
    organization: Satellite
    notification_type: email
    notification_configuration:
      username: ''  # this is required even if there's no username
      sender: controller0@example.com
      recipients:
      - admin@example.com
      use_tls: false
      host: smtp.example.com
      use_ssl: false
      password: ''  # this is required even if there's no password
      port: 25
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
    - {role: infra.aap_configuration.notification_templates, when: controller_notifications is defined}
```

## License

[GPL-3.0](https://github.com/redhat-cop/aap_configuration#licensing)

## Author

[Tom Page](https://github.com/Tompage1994)
[Sean Sullivan](https://github.com/sean-m-sullivan)
