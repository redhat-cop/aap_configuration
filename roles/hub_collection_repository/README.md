# infra.aap_configuration.hub_collection_repository

## Description

An Ansible Role to create a Collection Repository.

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
|`hub_collection_repositories`|`see below`|yes|Data structure describing your collection remote repository, described below.||

The `aap_configuration_async_dir` variable sets the directory to write the results file for async tasks.
The default value is set to  `null` which uses the Ansible Default of `/root/.ansible_async/`.

### Secure Logging Variables

The following Variables compliment each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to false as normally the add repository task does not include sensitive information.
hub_configuration_repository_secure_logging defaults to the value of aap_configuration_secure_logging if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of automation hub configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`hub_configuration_collection_repository_secure_logging`|`false`|no|Whether or not to include the sensitive Namespace role tasks in the log.  Set this value to `true` if you will be providing your sensitive values from elsewhere.|
|`aap_configuration_secure_logging`|`false`|no|This variable enables secure logging as well, but is shared across multiple roles, see above.|

### Asynchronous Retry Variables

The following Variables set asynchronous retries for the role.
If neither of the retries or delay or retries are set, they will default to their respective defaults.
This allows for all items to be created, then checked that the task finishes successfully.
This also speeds up the overall role.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`aap_configuration_async_timeout`|1000|no|This variable sets the async timeout for the role globally.|
|`hub_configuration_collection_repository_async_timeout`|`aap_configuration_async_timeout`|no|This variable sets the async timeout for the role.|
|`aap_configuration_async_retries`|50|no|This variable sets the number of retries to attempt for the role globally.|
|`hub_configuration_collection_repository_async_retries`|`aap_configuration_async_retries`|no|This variable sets the number of retries to attempt for the role.|
|`aap_configuration_loop_delay`|1000|no|This variable sets the loop_delay for the role globally.|
|`hub_configuration_collection_repository_loop_delay`|`aap_configuration_loop_delay`|no|This variable sets the loop_delay for the role.|
|`aap_configuration_async_delay`|1|no|This sets the delay between retries for the role globally.|
|`hub_configuration_collection_repository_async_delay`|`aap_configuration_async_delay`|no|This sets the delay between retries for the role.|

## Data Structure

### Collection Repository Variables

|Variable Name|Default Value|Required|Type|Description|
|:---:|:---:|:---:|:---:|:---:|
|`name`|""|yes|str| Collection Repository name. Probably one of community, validated, rh-certified, or one you have created.|
|`description`|""|no|str|Description to use for the Collection Repository.|
|`retain_repo_versions`|0|no|int|Retain X versions of the Collection repository. Default is 0 which retains all versions.|
|`pulp_labels`|""|no|dict|Pipeline and search options for the collection repository. See additional options below for details.|
|`distribution`|""|no|dict|Distribution options for the collection repository. See additional options below for details. Most users will leave this blank|
|`private`|""|no|boolean|Make the Collection repository private.|
|`remote`|""|no|str|Remote repository name. This is used if the collections use a remote source.|
|`update`|`false`|no|bool|Wait for the Collection repository to finish syncing before returning.|
|`wait`|`true`|no|bool|Wait for the Collection repository to finish syncing before returning.|
|`interval`|1.0|no|float|The interval to request an update from Automation Hub.|
|`timeout`|""|no|int|If waiting for the project to update this will abort after this amount of seconds.|
|`state`|`present`|no|str|Desired state of the collection repository. Either `present` or `absent`.|

#### Additional Option Variables

```yaml
---
pulp_labels:
  pipeline: "approved"
  hide_from_search: ""
distribution:
  name: "foobar"
  state: present
```

|Variable Name|Default Value|Required|Type|Description|
|:---:|:---:|:---:|:---:|:---:|
|`pipeline`|""|no|str|Description to use for the Collection Repository.|
|`hide_from_search`|""|no|str|Pipeline and search options for the collection repository.|
|`name`|""|no|dict|Distribution name to use for this collection repository. Will default to repository name if not provided.|
|`state`|`absent`|no|str|Desired state of the distribution. Either `present` or `absent`.|

### Standard Project Data Structure

#### Yaml Example

```yaml
---
hub_collection_repositories:
  - name: "foobar"
    description: "description of foobar repository"
    pulp_labels:
      pipeline: "approved"
    distribution:
      name: "foobar"
      state: present
    remote: community
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
    - infra.aap_configuration.hub_collection_repository
```

## License

[GPLv3+](https://github.com/ansible/galaxy_collection#licensing)
