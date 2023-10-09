# File_length module

The **`file_types`** module has been created to assist with the false-positive of the `VIOL_POST_DATA_LENGTH`, `VIOL_QUERY_STRING_LENGTH`, `VIOL_REQUEST_LENGTH` and `VIOL_URL_LENGTH` violations. It can modify the configured length on the file type extensions of a NAP policy.

Below you can find the input/outout parameters for the module

Input:
- **policy_path** (location of policy file)
- **filetype** (name of the file extension that you want to modify the length)
- **length** (the length that you would like to configure for a spefic file extension)
- **type** (The type of the length you want to configure. This can be any of the following: `url`, `request`, `post_data`, `qs_data`)
- **format** (*json* or *yaml*)

Output
- **policy** (Policy output)
- **msg** (Message from the module)
- **changed** (True/False)

## Examples of using the module on a playbook
  Input policy `app1_waf.yaml`
  
  ```yaml
  apiVersion: appprotect.f5.com/v1beta1
  kind: APPolicy
  metadata:
    name: app1_waf
  spec:
    policy:
      applicationLanguage: utf-8
      enforcementMode: blocking
      name: app1_waf
      template:
        name: POLICY_TEMPLATE_NGINX_BASE
  ```

  Playbook to modify the `post_data` length for a specific filetype `php`
  ```yaml
  - name: File Types
    hosts: localhost
    tasks:
      - name: Allow a specific filetype
        file_length:
          policy_path: policy.yaml
          filetype: php
          type: post_data
          length: 2048
          format: yaml
        register: result
  ```

  Updated policy.
  ```yaml
apiVersion: appprotect.f5.com/v1beta1
kind: APPolicy
metadata:
  name: app1_waf
spec:
  policy:
    applicationLanguage: utf-8
    enforcementMode: blocking
    filetypes:                      ### Changes added by ansible module
    - checkPostDataLength: true     ### Changes added by ansible module
      name: php                     ### Changes added by ansible module
      postDataLength: 2048          ### Changes added by ansible module
    name: app1_waf
    template:
      name: POLICY_TEMPLATE_NGINX_BASE
  ```




1. 
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
