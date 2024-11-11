# infra.aap_configuration.license

## Description

An Ansible Role to deploy a license on Ansible Controller.

This will either accept a manifest file, or use redhat subscription account credentials to lookup available subscriptions and use them.

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
|`controller_license`|`see below`|yes|Data structure describing your license for controller, described below.||
|`redhat_subscription_username`|""|no|Red Hat or Red Hat Satellite username to get available subscriptions. Used only for Subscription lookup implementation.||
|`redhat_subscription_password`|""|no|Red Hat or Red Hat Satellite password to get available subscriptions. Used only for Subscription lookup implementation.||

### Secure Logging Variables

The following Variables compliment each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to false as normally the add license task does not include sensitive information.
controller_configuration_license_secure_logging defaults to the value of aap_configuration_secure_logging if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of controller configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`controller_configuration_license_secure_logging`|`false`|no|Whether or not to include the sensitive license role tasks in the log. Set this value to `true` if you will be providing your sensitive values from elsewhere.|
|`aap_configuration_secure_logging`|`false`|no|This variable enables secure logging as well, but is shared across multiple roles, see above.|

## Data Structure

### Manifest vs Subscription

The module and this role can use either a manifest file, or lookup the subscription on your account. Only one method is needed, provide the appropriate variables to use the either method.

### License Variables for using mainfest

|Variable Name|Default Value|Required|Type|Description|
|:---:|:---:|:---:|:---:|:---:|
|`manifest_file`|""|no|obj|File path to a Red Hat subscription manifest (a .zip file)|
|`manifest_url`|""|no|obj|URL containing a Red Hat subscription manifest (a .zip file)|
|`manifest_content`|""|no|obj|Base64 encoded content of Red Hat subscription manifest|
|`manifest`|""|no|obj|DEPRECATED - changed to `manifest_file` (still works as an alias)|
|`manifest_username`|""|no|obj|Optional username for access to `manifest_url`|
|`manifest_password`|""|no|obj|Optional password for access to `manifest_url`|
|`pool_id`|""|no|str|Red Hat or Red Hat Satellite pool_id to attach to|
|`eula_accepted`|""|yes|bool|DEPRECATED since Tower 3.8 - Whether to accept the End User License Agreement for Ansible controller|
|`force`|`false`|no|bool|By default, the license manifest will only be applied if controller is currently unlicensed or trial licensed. When force=true, the license is always applied.|
|`state`|`present`|no|str|Desired state of the resource.|

### License Variables for using Red Hat Subscription

|Variable Name|Default Value|Required|Type|Description|
|:---:|:---:|:---:|:---:|:---:|
|`filters`|"default values"|no|str|dict of filters to use to narrow the subscription. See example below for how to use this.|
|`support_level`|"Self-Support"|no|str|DEPRECATED - changed to `manifest_file` (still works as an alias)|
|`list_num`|0|no|int|List index of the subscription to use, if you want to overide the default, it is recomended to use the filters to limit the pools found.|
|`pool_id`|""|no|str|Red Hat or Red Hat Satellite pool_id to attach to.|
|`force`|`false`|no|bool|By default, the license will only be applied if controller is currently unlicensed or trial licensed. When force=true, the license is always applied.|
|`use_lookup`|`false`|no|bool|Whether or not to lookup subscriptions.|
|`state`|`present`|no|str|Desired state of the resource.|

### Standard License Data Structure

#### Json Example

```json
{
    "controller_license": {
        "manifest_file": "/tmp/my_controller.license",
        "force": true
      }
}
```

#### Yaml Example

```yaml
---
controller_license:
  manifest_url: "https://fileserver.internal/controller_license.zip"
  manifest_username: admin
  manifest_password: password
  force: false
```

## Playbook Examples

### Standard Manifest Role Usage

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
    - {role: infra.aap_configuration.license, when: controller_license is defined}
```

### Standard Subscription lookup Role Usage

```yaml
---
- name: Playbook to configure ansible controller post installation
  hosts: localhost
  connection: local
  vars:
    aap_validate_certs: false
    aap_hostname: controller.example.com
    aap_username: admin
    aap_password: changeme
    redhat_subscription_username: changeme
    redhat_subscription_password: changeme
    controller_license:
      use_lookup: true
      filters:
        product_name: "Red Hat Ansible Automation Platform"
        support_level: "Self-Support"
  roles:
    - {role: infra.aap_configuration.license}
```

## License

[GPL-3.0](https://github.com/redhat-cop/aap_configuration#licensing)

## Author

[Tom Page](https://github.com/Tompage1994)
