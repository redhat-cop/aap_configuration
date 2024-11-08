# AAP Configuration conversion guide

## Background

This is documentation on how to use convert from the older infra collections to the aap_configuration collection.

Previously there were multiple collections
infra.controller_configuration
infra.ah_configuration
infra.eda_configuration

These have been combined along with new roles to configure the gateway aspect of AAP.

It is recommended to use the old collections when interacting with the Ansible Automation Platforms with versions 2.4 or prior. While some aspects of the collection may work, it can have unintended changes or behaviors.
The collections have been revamped to use a single set of connection variables and to standardize variables throughout the collections.

This guide will go through some of the standard variables what they were before and what to change them to.

## Basics

This collection requires other collections to be used. These collections mainly house the roles to wrap around the official certified collections. While these validated collections are not certified or have a level of support, volunteers spend their free time to maintain them, and to try and address any issues that arise quickly.

These collections are

- [ansible.eda](https://console.redhat.com/ansible/automation-hub/repo/published/ansible/eda/) or [upstream](https://galaxy.ansible.com/ui/repo/published/ansible/eda/)
- [ansible.hub](https://console.redhat.com/ansible/automation-hub/repo/published/ansible/hub/) or [upstream](https://galaxy.ansible.com/ui/repo/published/ansible/hub/)
- [ansible.controller](https://console.redhat.com/ansible/automation-hub/repo/published/ansible/controller/) or [awx.awx](https://galaxy.ansible.com/ui/repo/published/awx/awx/)
- [ansible.platform(Gateway collection)](https://console.redhat.com/ansible/automation-hub/repo/published/ansible/platform/)

These collections are required for this collection to work, While ansible.controller and ansible.gateway are only available from [https://console.redhat.com/](https://console.redhat.com/).

## Connection and Global Variables

These are the variables that are used to connect the platform and are the same across all Roles. Various environment variables can be used as specified by their module collections, but it is recommended to use ansible vars as they can be homogenized to be single variables.

### Connection Variables

These are the connection variables, These are used to connect to the platform. These replace things like controller_hostname, ah_host, and other global connection variables.

|Variable Name|Default Value|Required|Description|Example|
|:---|:---:|:---:|:---|:---|
|`aap_hostname`|""|yes|URL to the Ansible Automation Platform Server.|127.0.0.1|
|`aap_validate_certs`|`true`|no|Whether or not to validate the Ansible Automation Platform Server's SSL certificate.||
|`aap_username`|""|no|Admin User on the Ansible Automation Platform Server. Either username / password or oauthtoken need to be specified.||
|`aap_password`|""|no|Platform Admin User's password on the Server.  This should be stored in an Ansible Vault at vars/platform-secrets.yml or elsewhere and called from a parent playbook.||
|`aap_token`|""|no|Controller Admin User's token on the Ansible Automation Platform Server. This should be stored in an Ansible Vault at or elsewhere and called from a parent playbook. Either username / password or oauthtoken need to be specified.||
|`aap_request_timeout`|`10`|no|Specify the timeout in seconds Ansible should use in requests to the Ansible Automation Platform host.||

### Global Variables

Other Variables that will apply to all roles when used globally. Each of these has a per role that can override the default value if you wish to selectively use them. This is useful for things like retries and delay on projects, or secure logging for a role.

|Variable Name|Default Value|Required|Description|
|:---|:---:|:---:|:---|
|`aap_configuration_enforce_defaults`|`false`|no|Whether or not to enforce default option values. This is not universal and it is a best effort to enforce the default values of fields.|
|`aap_configuration_secure_logging`|`false`|no|Whether or not to include the sensitive Registry role tasks in the log.  Set this value to `true` if you will be providing your sensitive values from elsewhere.|
|`aap_configuration_async_retries`|50|no|This variable sets the number of retries to attempt for each role globally.|
|`aap_configuration_async_delay`|1|no|This sets the delay between retries for each role globally.|
|`aap_configuration_loop_delay`|1000|no|This variable sets the loop_delay for each role globally.|
|`aap_configuration_async_dir`|`null`|no|Sets the directory to write the results file for async tasks. The default value is set to `null` which uses the Ansible Default of `/root/.ansible_async/`.|

## Role variables

The order these variables and roles get applied by the dispatch role are
Gateway -> Hub -> Controller -> EDA

Below listed are the top level variables for each object in the order they are run by the dispatch role. Also included are the previous values if applicable

gateway_configuration vars:

- gateway_authenticators
- gateway_authenticator_maps
- gateway_settings
- aap_applications
- http_ports
- aap_organizations
- gateway_service_nodes
- gateway_gateway_service_keys
- gateway_service_clusters
- gateway_services
- gateway_role_user_assignments
- gateway_routes
- aap_teams

ah_configuration vars:

- aap_teams <- ah_groups
- aap_user_accounts <- ah_users
- hub_namespaces <- ah_namespaces
- hub_collections <- ah_collections
- hub_ee_registries <- ah_ee_registries
- hub_ee_repositories <- ah_ee_repositories
- hub_ee_images <- ah_ee_images
- hub_collection_remotes <- ah_collection_remotes
- hub_collection_repositories <- ah_collection_repositories
- hub_group_roles <- ah_group_roles
- hub_roles <- ah_roles

controller_configuration vars:

- controller_settings
- aap_organizations < - controller_organizations
- controller_instances
- controller_instance_groups
- controller_labels
- controller_credential_types
- controller_credentials
- controller_credential_input_sources
- controller_execution_environments
- aap_applications < - controller_applications
- controller_notifications
- controller_projects
- controller_inventories
- controller_inventory_sources
- controller_inventory_sources
- controller_hosts
- controller_bulk_hosts
- controller_templates
- controller_workflows
- controller_schedules
- controller_launch_jobs
- controller_workflow_launch_jobs
- aap_user_accounts <- controller_user_accounts

eda_configuration vars:

- eda_controller_tokens
- eda_credential_types
- eda_credentials
- eda_decision_environments
- eda_event_streams
- eda_projects
- eda_rulebook_activations

## Converted variables

### Controller

|Previous Name|New Name|
|:---|:---|
|`controller_hostname`|`aap_hostname`|
|`controller_username`|`aap_username`|
|`controller_password`|`aap_password`|
|`controller_oauthtoken`|`aap_token`|
|`controller_validate_certs`|`aap_validate_certs`|
|`controller_request_timeout`|`aap_request_timeout`|

### Hub

|Previous Name|New Name|
|:---|:---|
|`ah_host`|`aap_hostname`|
|`ah_username`|`aap_username`|
|`ah_password`|`aap_password`|
|`ah_validate_certs`|`aap_validate_certs`|
|`ah_token`|`aap_token`|

### Eda

|Previous Name|New Name|
|:---|:---|
|`eda_host`|`aap_hostname`|
|`eda_username`|`aap_username`|
|`eda_password`|`aap_password`|
|`eda_token`|`aap_token`|
|`eda_validate_certs`|`aap_validate_certs`|
|`eda_request_timeout`|`aap_request_timeout`|

### Role Vars

The following role vars have been updated as well. there are too many as its one for each role, so will go into how the name is crafted.

For example the previous var of
controller_configuration_projects_loop_delay
is still
controller_configuration_projects_loop_delay
however
ah_configuration_collection_repository_async_delay
is now
hub_configuration_collection_repository_loop_delay

These are the following global variables:

- `aap_configuration_enforce_defaults`
- `aap_configuration_secure_logging`
- `aap_configuration_async_retries`
- `aap_configuration_async_delay`
- `aap_configuration_loop_delay`
- `aap_configuration_async_dir`

This is the format that is used for each using the appropriate prefix

Prefixes

- controller_configuration
- ah_configuration
- gateway
- eda_configuration_

Format:

- `prefix`+`role_name`+`_enforce_defaults`
- `prefix`+`role_name`+`_secure_logging`
- `prefix`+`role_name`+`_async_retries`
- `prefix`+`role_name`+`_async_delay`
- `prefix`+`role_name`+`_loop_delay`
- `prefix`+`role_name`+`_async_dir`

use these to tweak how the role runs, this is particularly useful for projects syncing, long lists of job templates, and other tasks that can take a while to loop around. These all have defaults, and each global var is described above as to what it does.

## Dispatch changes

The dispatch role has changed to use the following order:

- gateway roles
- hub roles
- controller roles
- eda roles

These loop through all the applicable roles to create objects in the AAP. They will skip the role if the variable used in that role is not defined. you can tweak each services set of roles, or only run a single services roles by using the `aap_configuration_dispatcher_roles` variables. Refer to the [Dispatch role readme](roles/eda_controller_tokens/README.md) for more information.

## Roles moved

Any role that was not creating and managing objects on the AAP was moved to the [extended collection](https://github.com/redhat-cop/aap_configuration_extended). This includes lookup plugins, filtree and other roles.
