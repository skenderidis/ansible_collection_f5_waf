# File_types module

The **`file_types`** ansible module helps `Allow/Disallow` file type extensions on a NAP policy.

Below you can find the input/outout parameters for the module


The `file_types` module helps disable/enable file extensions that have been configured on the `disallowed` list or have not been configured on the explicit `allowed` list. 

Input:
- **policy_path** (location of policy file)
- **filetype** (extensions that you want to disable/enable)
- **format** (json or yaml)
- **enabled** (True or False. Defaults to True)

Output
- **policy** (the output of the policy)
- **msg** (Message from the module)
- **changed** (if there was a change in the configuration)

### Examples of using the module on a playbook

1. Disable a signature globaly
```yml
- name: File Types
  hosts: localhost
  tasks:
    - name: Allow File type
      signatures:
        filetype: "bak"
        policy_path: "policy.yaml"
        format: yaml
        enabled: True
      register: result

    - name: Display Module Output
      debug:
        var: result.policy

    - name: Display Module Output
      debug:
        var: result.msg
```
