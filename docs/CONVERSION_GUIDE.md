# Red Hat Communities of Practice Controller Configuration Collection Conversion Guide

## REQUIREMENTS

The AWX.AWX OR ANSIBLE.CONTROLLER collections MUST be installed in order for this collection to work. It is recommended they be invoked in the playbook in the following way.

## Using this collection

The awx.awx or ansible.controller collection must be invoked in the playbook in order for ansible to pick up the correct modules to use.

Otherwise it will look for the modules only in your base installation. If there are errors complaining about "couldn't resolve module/action" this is the most likely cause.

```yaml
- name: Playbook to configure ansible controller post installation
  hosts: localhost
  connection: local
  vars:
    aap_validate_certs: false
  collections:
    - awx.awx
    - infra.aap_configuration
```

## Variable name changes

### Major Variable names changed

The Following Variables need to be changed:

|Tower Variable Name|Controller Variable Name|
|:---:|:---:|
|`tower_ad_hoc_commands`|`controller_ad_hoc_commands`|
|`tower_ad_hoc_commands_cancel`|`controller_ad_hoc_commands_cancel`|
|`tower_applications`|`controller_applications`|
|`tower_credential_input_sources`|`controller_credential_input_sources`|
|`tower_credential_types`|`controller_credential_types`|
|`tower_credentials`|`controller_credentials`|
|`tower_execution_environments`|`controller_execution_environments`|
|`tower_groups`|`controller_groups`|
|`tower_hosts`|`controller_hosts`|
|`tower_instance_groups`|`controller_instance_groups`|
|`tower_inventories`|`controller_inventories`|
|`tower_inventory_sources`|`controller_inventory_sources`|
|`tower_launch_jobs`|`controller_launch_jobs`|
|`tower_templates`|`controller_templates`|
|`tower_cancel_jobs`|`controller_cancel_jobs`|
|`tower_labels`|`controller_labels`|
|`tower_license`|`controller_license`|
|`tower_notifications`|`controller_notifications`|
|`tower_organizations`|`controller_organizations`|
|`tower_projects`|`controller_projects`|
|`tower_rbac`|`controller_roles`|
|`tower_schedules`|`controller_schedules`|
|`tower_settings`|`controller_settings`|
|`tower_teams`|`controller_teams`|
|`tower_user_accounts`|`controller_user_accounts`|
|`tower_workflows`|`controller_workflows`|
|`tower_workflow_launch_jobs`|`controller_workflow_launch_jobs`|

### Authentication Credentials

|Tower Variable Name|Controller Variable Name|
|:---:|:---:|
|`tower_username`|`aap_username`|
|`tower_password`|`aap_password`|
|`tower_oauthtoken`|`controller_oauthtoken`|
|`tower_hostname`|`aap_hostname`|
|`tower_config_file`|`controller_config_file`|
|`tower_validate_certs`|`aap_validate_certs`|

### Specific Changes in Roles

### Projects

|Tower Variable Name|Controller Variable Name|Reason|
|:---:|:---:|:---:|
|`default_environment`|`custom_virtualenv`|`environments now refer to Execution Environments`|

## Notes

Making these changes should be all the ones you need to make in order to use the updated collection.
However there have been many changes and this list is in no way final or all encompassing.
