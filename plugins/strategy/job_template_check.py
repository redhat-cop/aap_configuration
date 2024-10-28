# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


from ansible.errors import AnsibleError
from ansible.module_utils._text import to_native
from ansible.module_utils.parsing.convert_bool import boolean
import os

DOCUMENTATION = """
    name: job_template_check
    short_description: Checks whether Job Templates exist within Controller before executing the playbook
    description:
        - Checks whether Job Templates exist within Controller before executing the playbook
        - Utilises the `controller_launch_jobs` variable and checks whether the Job Templates within Controller exist
    version_added: "3.0.0"
    author: Tom Page (@Tompage1994)
"""

# Attempt to import the ControllerAPIModule class from either collection
try:
    from ansible_collections.ansible.controller.plugins.module_utils.controller_api import ControllerAPIModule
except ImportError:
    try:
        from ansible_collections.awx.awx.plugins.module_utils.controller_api import ControllerAPIModule
    except ImportError:
        raise AnsibleError("This strategy requires either the ansible.controller or awx.awx collection to be installed. Please install and try again.")

from ansible.plugins.strategy import StrategyBase


class StrategyModule(StrategyBase):

    def handle_error(self, **kwargs):
        # self._tqm._stdout_callback.error("Required dependencies not met. Exiting playbook." + to_native(kwargs.get('msg')))
        raise AnsibleError(
            "Required dependencies not met. Exiting playbook. Could not find Job Template '{0}' on Controller."
            .format(to_native(kwargs['query']['name'])))

    def get_connection_params_from_hosts(self, inventory, variable_manager, play_context, connection_vars):
        """
        Retrieve connection parameters from any host in the inventory.
        """

        result = {}
        for v in connection_vars:
            result[v] = None

        # Iterate over all hosts in the inventory to find the connection parameters
        for host in inventory.get_hosts():
            host_vars = variable_manager.get_vars(host=host, play=play_context)

            # Check each variable and stop once we find a value
            for v in connection_vars:
                result[v] = result[v] or (str(host_vars.get(v)) if host_vars.get(v) is not None else None)

            # If all parameters are found, break early
            if all(value is not None for value in result.values()):
                break

        return result

    def run(self, iterator, play_context):

        connection_vars = [
            'controller_host',
            'controller_username',
            'controller_password',
            'controller_validate_certs',
            'controller_oauthtoken',
        ]

        host_params = self.get_connection_params_from_hosts(self._inventory, self._variable_manager, iterator._play, connection_vars)
        connection_params = {
            'controller_host': host_params['controller_host'] or os.getenv('CONTROLLER_HOST') or '127.0.0.1',
            'controller_username': host_params['controller_username'] or os.getenv('CONTROLLER_USERNAME') or 'admin',
            'controller_password': host_params['controller_password'] or os.getenv('CONTROLLER_PASSWORD') or 'password',
            'validate_certs': boolean(host_params['controller_validate_certs'] or os.getenv('CONTROLLER_VERIFY_SSL') or True),
            'controller_oauthtoken': host_params['controller_oauthtoken'] or os.getenv('CONTROLLER_OAUTH_TOKEN'),
        }

        # Create our module
        module = ControllerAPIModule(argument_spec={}, direct_params=connection_params, error_callback=self.handle_error)

        # Job template name to check
        jt_dependencies = []
        for host in self._inventory.get_hosts():
            jt_dependencies += list(self._variable_manager.get_vars(host=host, play=iterator._play).get('controller_launch_jobs') or [])

        for jt in jt_dependencies:
            module.get_exactly_one('job_templates', name_or_id=jt)

        # Proceed with the standard task execution if dependencies are met
        return super().run(iterator, play_context)
