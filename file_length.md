# File_length module

The **`file_length`** ansible module allows for modification of the confgured length on the file type extensions of a NAP policy.


The `file_types` module helps disable/enable file extensions that have been configured on the `disallowed` list or have not been configured on the explicit `allowed` list. 

Input:
- **policy_path** (location of policy file)
- **filetype** (name of the file extension that you want to configure)
- **length** (the length that you would like to configure for a spefic file extension)
- **type** (The type of the length you want to configure `url`, `request`, `post_data`, `qs_data`)
- **format** (*json* or *yaml*)

Output
- **policy** (the output of the policy)
- **msg** (Message from the module)
- **changed** (if there was a change in the configuration)

### Examples of using the module on a playbook

1. Configure Length for a specific filetype
```yml
- name: File Type Length
  hosts: localhost
  tasks:
    - name: Configure Length
      signatures:
        format: yaml
        policy_path: "policy.yaml"
        filetype: "php"
        type: url
        length: 2048
      register: result

    - name: Display Module Output
      debug:
        var: result.policy

    - name: Display Module Output
      debug:
        var: result.msg
```
