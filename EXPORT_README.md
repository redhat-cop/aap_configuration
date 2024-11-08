# Automation Controller Export Documentation

## Description

This is documentation on how to use a the Automation Controller export commands in development. You can also look at the [filetree_create](https://github.com/redhat-cop/aap_configuration_extended/blob/devel/roles/filetree_create/README.md) role as another method to export data.

This command allows exporting all available endpoints for Automation Controller for use in importing, templates, backups and many other uses.

**NOTE:** If you use the awx export option it will NOT use the correct high level variable list naming that is expected by the rest of these roles you will need to correctly name them before being able to use the roles to import the data into your new Controller. See [#332](https://github.com/redhat-cop/aap_configuration/issues/332) for more details.

## Installation

```console
pip3 install awxkit
```

## Basic command options and export methods

```console
awx export --conf.host https://localhost --conf.username admin --conf.password ******** --conf.insecure --help
```

```console
awx export --conf.host https://localhost --conf.username admin --conf.password ******** --conf.insecure --job_templates
```

```yaml
---
- name: Export projects
  hosts: localhost
  connection: local
  gather_facts: false
  collections:
    - ansible.controller
  environment:
     CONTROLLER_HOST: https://localhost
     CONTROLLER_USERNAME: admin
     CONTROLLER_PASSWORD: password
     CONTROLLER_VERIFY_SSL: false

  tasks:
    - name: Export projects
      awx.awx.export: # or ansible.controller.export
        projects: all
      register: export_results

    - name: Show results
      ansible.builtin.debug:
        var: export_results

    - name: Export projects to file
      ansible.builtin.copy:
        content: "{{ export_results | to_nice_yaml(width=50, explicit_start=true, explicit_end=true) }}"
        dest: projects.yaml
...
```

## Available options for this command

|Option|
|:---:|
|applications|
|credentials|
|credential_types|
|execution_environments|
|inventory|
|inventory_sources|
|job_templates|
|notification_templates|
|organizations|
|projects|
|schedules|
|teams|
|users|
|workflow_job_templates|

## Limitations

### Project export

related signature_validation_credential is exported as a credential # not an object.

### Workflow export related items

related instanced groups for workflow nodes prompt on launch for job templates
related labels for workflow nodes prompt on launch for job templates

Keep up to date with these limitations with [this awx issue](https://github.com/ansible/awx/issues/13868)
