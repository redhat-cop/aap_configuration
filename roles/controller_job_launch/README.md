# infra.aap_configuration.job_launch

## Description

An Ansible Role to launch a job template on Ansible Controller.

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
|`controller_launch_jobs`|`see below`|yes|Data structure describing the jobs to launch Described below.||

### Secure Logging Variables

The following Variables compliment each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to false as normally the job launch task does not include sensitive information.
controller_configuration_job_launch_secure_logging defaults to the value of aap_configuration_secure_logging if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of controller configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`controller_configuration_job_launch_secure_logging`|`false`|no|Whether or not to include the sensitive ad_hoc_command role tasks in the log. Set this value to `true` if you will be providing your sensitive values from elsewhere.|
|`aap_configuration_secure_logging`|`false`|no|This variable enables secure logging as well, but is shared across multiple roles, see above.|

## Data Structure

### Job Launch Variables

|Variable Name|Default Value|Required|Type|Description|
|:---:|:---:|:---:|:---:|:---:|
|`name`|""|yes|str|The name or id of the job to launch.|
|`job_type`|""|no|str|Job_type to use for the job, only used if prompt for job_type is set. Run or Check are the options.|
|`inventory`|""|no|str|Inventory to use for the job, only used if prompt for inventory is set.|
|`organization`|""|no|str|Organization the inventory belongs to.|
|`credentials`|""|no|list|TCredential to use for job, only used if prompt for credential is set.|
|`extra_vars`|""|no|dict|extra_vars to use for the Job Template. ask_extra_vars needs to be set to true via controller_job_template module.|
|`limit`|""|no|str|Limit to use for the job_template.|
|`tags`|""|no|str|Specific tags to use for from playbook.|
|`scm_branch`|""|no|str|A specific of the SCM project to run the template on.|
|`skip_tags`|""|no|str|Specific tags to skip from the playbook.|
|`verbosity`|""|no|int|Verbosity level for this job run.|
|`diff_mode`|""|no|bool|Show the changes made by Ansible tasks where supported.|
|`credential_passwords`|""|no|str|Passwords for credentials which are set to prompt on launch.|
|`execution_environment`|Job Template default|no|str|Execution Environment applied as a prompt. Job Template default used if not set. Only allowed if `ask_execution_environment_on_launch` set to true on Job Template|
|`forks`|Job Template default|no|int|Forks applied as a prompt. Job Template default used if not set. Only allowed if `ask_forks_on_launch` set to true on Job Template|
|`instance_groups`|Job Template default|no|str| List of Instance Groups applied as a prompt. Job Template default used if not set. Only allowed if `ask_instance_groups_on_launch` set to true on Job Template|
|`job_slice_count`|Job Template default|no|int|Job Slice Count to use in the job run. Job Template default used if not set. Only allowed if `ask_job_slice_count_on_launch` set to true on Job Template|
|`labels`|Job Template default|no|list|List of labels to use in the job run. Job Template default used if not set. Only allowed if `ask_labels_on_launch` set to true on Job Template|
|`job_timeout`|Job Template default|no|int|Timeout to use in the job run. Job Template default used if not set. Only allowed if `ask_timeout_on_launch` set to true on Job Template|
|`wait`|""|no|bool|Wait for the job to complete.|
|`interval`|2|no|float|The interval to request an update from controller.|
|`timeout`|""|no|int|If waiting for the job to complete this will abort after this amount of seconds.|

### Standard Job Launch Data Structure

#### Yaml Example

```yaml
---
controller_launch_jobs:
  - name: test-template-1

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
    - {role: infra.aap_configuration.job_launch, when: controller_launch_jobs is defined}
```

## License

[GPL-3.0](https://github.com/redhat-cop/aap_configuration#licensing)

## Author

[Sean Sullivan](https://github.com/sean-m-sullivan)
