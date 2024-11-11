# infra.aap_configuration.hub_collection_remote

## Description

An Ansible Role to create a Collection Remote Repository.

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
|`hub_collection_remotes`|`see below`|yes|Data structure describing your collection remote repository, described below.||

The `aap_configuration_async_dir` variable sets the directory to write the results file for async tasks.
The default value is set to  `null` which uses the Ansible Default of `/root/.ansible_async/`.

### Secure Logging Variables

The following Variables compliment each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to false as normally the add repository task does not include sensitive information.
hub_configuration_repository_secure_logging defaults to the value of aap_configuration_secure_logging if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of automation hub configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`hub_configuration_collection_remote_secure_logging`|`false`|no|Whether or not to include the sensitive Namespace role tasks in the log.  Set this value to `true` if you will be providing your sensitive values from elsewhere.|
|`aap_configuration_secure_logging`|`false`|no|This variable enables secure logging as well, but is shared across multiple roles, see above.|

### Asynchronous Retry Variables

The following Variables set asynchronous retries for the role.
If neither of the retries or delay or retries are set, they will default to their respective defaults.
This allows for all items to be created, then checked that the task finishes successfully.
This also speeds up the overall role.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`aap_configuration_async_timeout`|1000|no|This variable sets the async timeout for the role globally.|
|`hub_configuration_collection_remote_async_timeout`|`aap_configuration_async_timeout`|no|This variable sets the async timeout for the role.|
|`aap_configuration_async_retries`|50|no|This variable sets the number of retries to attempt for the role globally.|
|`hub_configuration_collection_remote_async_retries`|`aap_configuration_async_retries`|no|This variable sets the number of retries to attempt for the role.|
|`aap_configuration_loop_delay`|1000|no|This variable sets the loop_delay for the role globally.|
|`hub_configuration_collection_remote_loop_delay`|`aap_configuration_loop_delay`|no|This variable sets the loop_delay for the role.|
|`aap_configuration_async_delay`|1|no|This sets the delay between retries for the role globally.|
|`hub_configuration_collection_remote_async_delay`|`aap_configuration_async_delay`|no|This sets the delay between retries for the role.|

## Data Structure

### Collection Remote Variables

|Variable Name|Default Value|Required|Description|Example|
|:---:|:---:|:---:|:---:|:---:|
|`name`|``|yes| Repository name. Probably one of community, validated, or rh-certified||
|`url`|`https://cloud.redhat.com/api/automation-hub/`|no|(`ah_repository_certified`)Remote URL for the repository.|`https://console.redhat.com/api/automation-hub/content/`|
|`url`|`https://galaxy.ansible.com/api/`|no|(`ah_repository_community`)Remote URL for the repository.||
|`auth_url`|`https://sso.redhat.com/auth/realms/redhat-external/protocol/openid-connect/token`|no|(`ah_repository_certified`)Remote URL for the repository authentication if separate.||
|`token`|``|no|Token to authenticate to the remote repository.||
|`policy`|`immediate`|no|The policy to use when downloading content. Can be one of `immediate`, `When syncing, download all metadata and content now.`.||
|`requirements`|``|no|Requirements, a list of collections in [requirements file format](https://docs.ansible.com/ansible/latest/collections_guide/collections_installing.html#install-multiple-collections-with-a-requirements-file) to limit thedownload from remote. This will only download provided collections. This is only the list under collections. See examples for usage.||
|`requirements_file`|``|no|A yaml requirements file to download from remote. In requirements file format. Exclusive with `requirements` ||
|`username`|``|no|Username to authenticate to the remote repository.||
|`password`|``|no|Password to authenticate to the remote repository.||
|`tls_validation`|`true`|no|Whether to use TLS validation against the remote repository|true|
|`client_key`|``|no|A PEM encoded private key file used for authentication||
|`client_cert`|``|no|A PEM encoded client certificate used for authentication||
|`ca_cert`|``|no|A PEM encoded CA certificate used for authentication||
|`client_key_path`|``|no|Path to a PEM encoded private key file used for authentication||
|`client_cert_path`|``|no|Path to a PEM encoded client certificate used for authentication||
|`ca_cert_path`|``|no|Path to a PEM encoded CA certificate used for authentication||
|`download_concurrency`|`10`|no| Number of concurrent collections to download.||
|`max_retries`|`0`|no|Retries to use when running sync. Default is 0 which does not limit.||
|`rate_limit`|`8`|no|Limits total download rate in requests per second.||
|`signed_only`|`false`|no|Only download signed collections|false|
|`sync_dependencies`|`true`|no|Whether to download dependencies when syncing collections.|false|
|`proxy_url`|``|no|The URL for the proxy. Defaults to global `proxy_url` variable.||
|`proxy_username`|``|no|The username for the proxy authentication. Defaults to global `proxy_username` variable.||
|`proxy_password`|``|no|The password for the proxy authentication. Defaults to global `proxy_password` variable.||
|`state`|`present`|no|Desired state of the collection_remote. Either `present` or `absent`.||

### Standard Project Data Structure

#### Yaml Example

```yaml
---
hub_collection_remotes:
  - name: community-infra
    url: https://beta-galaxy.ansible.com/
    requirements:
      - name: infra.ee_utilities
      - name: infra.aap_configuration
```

## Playbook Examples

### Standard Role Usage

```yaml
---
- name: Add repository to Automation Hub
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
    - infra.aap_configuration.hub_collection_remote
```

## License

[GPLv3+](https://github.com/ansible/galaxy_collection#licensing)
