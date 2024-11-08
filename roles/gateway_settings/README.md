# Ansible Role infra.aap_configuration.settings

An Ansible role to alter Settings on Ansible Automation Gateway.

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
|`gateway_settings`|`see below`|yes|Data structure describing your gateway_services Described below.||

### Secure Logging Variables

The following Variables compliment each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to false as normally the add ee_registry task does not include sensitive information.
gateway_services_secure_logging defaults to the value of aap_configuration_secure_logging if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of automation hub configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`gateway_services_secure_logging`|`false`|no|Whether or not to include the sensitive Registry role tasks in the log.  Set this value to `true` if you will be providing your sensitive values from elsewhere.|
|`aap_configuration_secure_logging`|`false`|no|This variable enables secure logging as well, but is shared across multiple roles, see above.|

## Data Structure

### Settings arguments

Provide settings as a single dict under `settings_list`.

## Usage

### Json Example

```json
{
  "gateway_settings": {
    "gateway_token_name": "X-DAB-JW-TOKEN",
    "gateway_access_token_expiration": 600,
    "gateway_basic_auth_enabled": true,
    "gateway_proxy_url": "https://localhost:9080",
    "gateway_proxy_url_ignore_cert": false,
    "password_min_length": 0,
    "password_min_digits": 0,
    "password_min_upper": 0,
    "password_min_special": 0,
    "allow_admins_to_set_insecure": false
  }
}

```

### Yaml Example

File name: `data/gateway_settings.yml`

```yaml
---
gateway_settings:
  gateway_token_name: X-DAB-JW-TOKEN
  gateway_access_token_expiration: 600
  gateway_basic_auth_enabled: true
  gateway_proxy_url: https://localhost:9080
  gateway_proxy_url_ignore_cert: false
  password_min_length: 0
  password_min_digits: 0
  password_min_upper: 0
  password_min_special: 0
  allow_admins_to_set_insecure: false


```

## License

[GPL-3.0](https://github.com/redhat-cop/aap_configuration#licensing)
