# File_types module

The **`file_types`** module has been created to assist with the false-positive of the `VIOL_FILETYPE` violations. It can allow/disallow file type extensions on the App Protect Policy. 

Below you can find the input/outout parameters for the module

Input:
- **policy_path** (location of policy file)
- **filetype** (extensions that you want to disable/enable)
- **format** (*json* or *yaml*)
- **enabled** (*True* or *False*. Defaults to True)

Output
- **policy** (Policy output)
- **msg** (Message from the module)
- **changed** (True/False)

## Examples of using the module on a playbook

### Allow a disallowed file type (php)
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


  Playbook to allow the file type **php**.
  ```yaml
  - name: File Types
    hosts: localhost
    tasks:
      - name: Allow a specific filetype
        file_types:
          filetype: php
          enabled: True
          policy_path: "app1_waf.yaml"
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
      filetypes:                  ### Changes added by ansible module
      - allowed: true             ### Changes added by ansible module
        name: php                 ### Changes added by ansible module
      name: app1_waf
      template:
        name: POLICY_TEMPLATE_NGINX_BASE
  ```
