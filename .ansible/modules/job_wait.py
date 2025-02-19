# This is a mocked Ansible module generated by ansible-lint
from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = '''
module: job_wait

short_description: Mocked
version_added: "1.0.0"
description: Mocked

author:
    - ansible-lint (@nobody)
'''
EXAMPLES = '''mocked'''
RETURN = '''mocked'''


def main():
    result = dict(
        changed=False,
        original_message='',
        message='')

    module = AnsibleModule(
        argument_spec=dict(),
        supports_check_mode=True,
    )
    module.exit_json(**result)


if __name__ == "__main__":
    main()
