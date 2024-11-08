# Ansible Role infra.aap_configuration.routes

## Description

An Ansible Role to configure gateway non-API Routes to services (controller, hub,...) on Ansible Automation gateway.
They define http port and path (**not** starting with prefix /api/) used in gateway and
http port and path in the destination service (gateway, controller, hub, eda).

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
|`gateway_routes`|`see below`|yes|Data structure describing your gateway_routes Described below.||

### Secure Logging Variables

The following Variables compliment each other.
If Both variables are not set, secure logging defaults to false.
The role defaults to false as normally the add ee_registry task does not include sensitive information.
gateway_routes_secure_logging defaults to the value of aap_configuration_secure_logging if it is not explicitly called. This allows for secure logging to be toggled for the entire suite of automation hub configuration roles with a single variable, or for the user to selectively use it.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`gateway_routes_secure_logging`|`false`|no|Whether or not to include the sensitive Registry role tasks in the log.  Set this value to `true` if you will be providing your sensitive values from elsewhere.|
|`aap_configuration_secure_logging`|`false`|no|This variable enables secure logging as well, but is shared across multiple roles, see above.|

### Asynchronous Retry Variables

The following Variables set asynchronous retries for the role.
If neither of the retries or delay or retries are set, they will default to their respective defaults.
This allows for all items to be created, then checked that the task finishes successfully.
This also speeds up the overall role.

|Variable Name|Default Value|Required|Description|
|:---:|:---:|:---:|:---:|
|`aap_configuration_async_retries`|50|no|This variable sets the number of retries to attempt for the role globally.|
|`gateway_routes_async_retries`|`aap_configuration_async_retries`|no|This variable sets the number of retries to attempt for the role.|
|`aap_configuration_async_delay`|1|no|This sets the delay between retries for the role globally.|
|`gateway_routes_async_delay`|`aap_configuration_async_delay`|no|This sets the delay between retries for the role.|
|`aap_configuration_loop_delay`|1000|no|This variable sets the loop_delay for the role globally.|
|`gateway_routes_loop_delay`|`aap_configuration_loop_delay`|no|This variable sets the loop_delay for the role.|
|`aap_configuration_async_dir`|`null`|no|Sets the directory to write the results file for async tasks. The default value is set to `null` which uses the Ansible Default of `/root/.ansible_async/`.|

## Data Structure

### Service Arguments

Options for the `routes_list` variable:

| Variable Name         |    Default Value    | Required | Type | Description                                                                         |
|:----------------------|:-------------------:|:--------:|:----:|:------------------------------------------------------------------------------------|
| `name`                |         N/A         |   yes    | str  | The name of the route                                                               |
| `new_name`            |         N/A         |    no    | str  | Setting this option will change the existing name (looked up via the name field)    |
| `description`         |         ""          |    no    | str  | Description of the route                                                            |
| `gateway_path`        |         N/A         |    no    | str  | Path on the AAP gateway to listen to traffic on                                     |
| `http_port`           |         N/A         |    no    | str  | ID or name referencing the [Http Port](../gateway_http_ports/README.md)             |
| `service_cluster`     |         N/A         |    no    | str  | ID or name referencing the [Service Cluster](../gateway_service_clusters/README.md) |
| `is_service_https`    |       `false`       |    no    | bool | Flag whether or not the service cluster uses https                                  |
| `enable_gateway_auth` | N/A (`true` by API) |    no    | bool | If false, the AAP gateway will not insert a gateway token into the proxied request  |
| `service_path`        |         N/A         |    no    | str  | URL path on the AAP Service cluster to route traffic to                             |
| `service_port`        |         N/A         |    no    | int  | Port on the service cluster to route traffic to                                     |
| `tags`                |         ""          |    no    | str  | Comma-separated string, selects which (tagged) nodes receive traffic from this route|
| `state`               |      `present`      |    no    | str  | README.md#state-variable)                                              |

**Unique value:**

- `name`
- `http_port` + `gateway_path`

**Note**: `gateway_path` can't start with `/api/` prefix

## Usage

### Json Example

- Check that Controller's config route exists
- Update gateway route to the port 8000 and path '/non-api/v2'
- Create or update EDA Route to gateway proxy port (http port) with id 1 and Service Cluster with id 2 (in the database)

```json
{
  "gateway_services": [
    {
      "name": "Controller Config Route",
      "state": "exists"
    },
    {
      "name": "Gateway Non-api Route",
      "http_port": "Port 8000",
      "gateway_path": "/non-api/v2",
      "enable_gateway_auth": false
    },
    {
      "name": "EDA Config Route",
      "service_cluster": 2,
      "http_port": 1,
      "gateway_path": "/config/eda/",
      "service_path": "/config/v1/",
      "service_port": 9000
    }
  ]
}
```

### Yaml Example

- Checks that non-api routes to services exist
- If at least one doesn't exist, playbook fails.

File name: `data/gateway_routes.yml`

```yaml
---
platform_state: exists
routes_list:
- name: "Controller Config route"
  gateway_path: '/config/controller/'
  http_port: Port 8000
- name: "Hub Config route"
- name: 3
- name: 4
```

## License

[GPL-3.0](https://github.com/redhat-cop/aap_configuration#licensing)
