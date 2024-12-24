# Red Hat Communities of Practice AAP Configuration Collection

![pre-commit tests](https://github.com/redhat-cop/aap_configuration/actions/workflows/pre-commit.yml/badge.svg)
![Release](https://github.com/redhat-cop/aap_configuration/actions/workflows/release.yml/badge.svg)
<!-- markdownlint-disable-line MD033 MD034 --><a href="https://raw.githubusercontent.com/redhat-cop/aap_configuration/devel/docs/aap_config_as_code_public_meeting.ics"><img border="0" alt="Google Calendar invite" src="https://www.google.com/calendar/images/ext/gc_button1_en-GB.gif"></a>
<!-- Further CI badges go here as above -->

This Ansible collection allows for easy interaction with AAP via Ansible roles using the modules from the certified collections.

## Getting Help

We are on the Ansible Forums and Matrix, if you want to discuss something, ask for help, or participate in the community, please use the #infra-config-as-code tag on the form, or post to the chat in Matrix.

[Ansible Forums](https://forum.ansible.com/tag/infra-config-as-code)

[Matrix Chat Room](https://matrix.to/#/#aap_config_as_code:ansible.com)

## Requirements

The supported collections that contains the modules are required for this collection to work, you can copy this requirements.yml file example.

```yaml
---
collections:
  - name: ansible.platform
  - name: ansible.hub
  - name: ansible.controller
  - name: ansible.eda
  - name: infra.aap_configuration
...
```

## Links to Ansible Automation Platform Collections

|                                      Collection Name                                |            Purpose            |
|:-----------------------------------------------------------------------------------:|:-----------------------------:|
| ansible.platform repo (no public repo for this collection)                          | gateway/platform modules      |
| [ansible.hub repo](https://github.com/ansible-collections/ansible_hub)              | Automation hub modules        |
| [ansible.controller repo](https://github.com/ansible/awx/tree/devel/awx_collection) | Automation controller modules |
| [ansible.eda repo](https://github.com/ansible/event-driven-ansible)                 | Event Driven Ansible modules  |

## Links to other Validated Configuration Collections for Ansible Automation Platform

|                                      Collection Name                                       |                      Purpose                      |
|:------------------------------------------------------------------------------------------:|:-------------------------------------------------:|
| [AAP Configuration Extended](https://github.com/redhat-cop/aap_configuration_extended)     | Where other useful roles that don't fit here live |
| [EE Utilities](https://github.com/redhat-cop/ee_utilities)                                 | Execution Environment creation utilities          |
| [AAP installation Utilities](https://github.com/redhat-cop/aap_utilities)                  | Ansible Automation Platform Utilities             |
| [AAP Configuration Template](https://github.com/redhat-cop/aap_configuration_template)     | Configuration Template for this suite             |

## Included content

Click the `Content` button to see the list of content included in this collection.

## Installing this collection

You can install the infra.aap_configuration.collection with the Ansible Galaxy CLI:

```console
ansible-galaxy collection install infra.aap_configuration
```

You can also include it in a `requirements.yml` file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
---
collections:
  - name: infra.aap_configuration
    # If you need a specific version of the collection, you can specify like this:
    # version: ...
```

## Conversion from tower_configuration

If you were using a version of redhat_cop.tower_configuration, please refer to our Conversion Guide here: [Conversion Guide](docs/CONVERSION_GUIDE.md)

## Using this collection

The awx.awx or ansible.controller collection must be invoked in the playbook in order for Ansible to pick up the correct modules to use.

The following command will invoke the collection playbook. This is considered a starting point for the collection.

```console
ansible-playbook infra.aap_configuration.configure_aap.yml
```

Otherwise it will look for the modules only in your base installation. If there are errors complaining about "couldn't resolve module/action" this is the most likely cause.

```yaml
- name: Playbook to configure ansible controller post installation
  hosts: localhost
  connection: local
  vars:
    aap_validate_certs: true
  collections:
    - awx.awx
```

Define following vars here, or in `aap_configs/controller_auth.yml`
`aap_hostname: ansible-controller-web-svc-test-project.example.com`

You can also specify authentication by a combination of either:

- `aap_hostname`, `aap_username`, `aap_password`
- `aap_hostname`, `aap_token`

The OAuth2 token is the preferred method. You can obtain the token through the preferred `controller_token` module, or through the
AWX CLI [login](https://docs.ansible.com/automation-controller/latest/html/controllerapi/authentication.html)
command.

These can be specified via (from highest to lowest precedence):

- direct role variables as mentioned above
- environment variables (most useful when running against localhost)
- a config file path specified by the `controller_config_file` parameter
- a config file at `~/.controller_cli.cfg`
- a config file at `/etc/controller/controller_cli.cfg`

Config file syntax looks like this:

```ini
[general]
host = https://localhost:8043
verify_ssl = true
oauth_token = LEdCpKVKc4znzffcpQL5vLG8oyeku6
```

Controller token module would be invoked with this code:

```yaml
    - name: Create a new token using controller username/password
      awx.awx.token:
        description: 'Creating token to test controller jobs'
        scope: "write"
        state: present
        controller_host: "{{ aap_hostname }}"
        aap_username: "{{ aap_username }}"
        aap_password: "{{ aap_password }}"

```

### Automate the Automation

Every Ansible Controller instance has it's own particularities and needs. Every administrator team has it's own practices and customs. This collection allows adaptation to every need, from small to large scale, having the objects distributed across multiple environments and leveraging Automation Webhook that can be used to link a Git repository and Ansible automation natively.

#### Scale at your needs

The input data can be organized in a very flexible way, letting the user use anything from a single file to an entire file tree to store the controller objects definitions, which could be used as a logical segregation of different applications, as needed in real scenarios.

### Controller Export

The awx command line can export json that is compatible with this collection.
In addition there is an awx.awx/ansible.controller export module that use the awx command line to export.
More details can be found [here](EXPORT_README.md)

### Template Example

A Template to use in order to start using the collections can be found [here](https://github.com/redhat-cop/aap_configuration_template)

### See Also

- [Ansible Using collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html) for more details.

## Release and Upgrade Notes

For details on changes between versions, please see [the changelog for this collection](CHANGELOG.rst).

## Releasing, Versioning and Deprecation

This collection follows [Semantic Versioning](https://semver.org/). More details on versioning can be found [in the Ansible docs](https://docs.ansible.com/ansible/latest/dev_guide/developing_collections.html#collection-versions).

We plan to regularly release new minor or bugfix versions once new features or bugfixes have been implemented.

Releasing the current major version happens from the `devel` branch.

## Roadmap

Adding the ability to use direct output from the awx export command in the roles along with the current data model.

## Contributing to this collection

We welcome community contributions to this collection. If you find problems, please open an issue or create a PR against the [Controller Configuration collection repository](https://github.com/redhat-cop/aap_configuration).
More information about contributing can be found in our [Contribution Guidelines.](https://github.com/redhat-cop/aap_configuration/blob/devel/.github/CONTRIBUTING.md)

We have a community meeting every 4 weeks. Find the agenda in the [issues](https://github.com/redhat-cop/aap_configuration/issues) and the calendar invitation below:

<!-- markdownlint-disable-next-line MD033 MD034 -->
<a target="_blank" href="https://raw.githubusercontent.com/redhat-cop/aap_configuration/devel/docs/aap_config_as_code_public_meeting.ics"><img border="0" alt="Google Calendar invite" src="https://www.google.com/calendar/images/ext/gc_button1_en-GB.gif"></a>

## Code of Conduct

This collection follows the Ansible project's
[Code of Conduct](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html).
Please read and familiarize yourself with this document.

## Licensing

GNU General Public License v3.0 or later.

See [LICENSE](LICENSE) to see the full text.
