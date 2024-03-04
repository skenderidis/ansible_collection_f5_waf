# VIOL_QUERY_STRING_LENGTH module

The **`viol_query_string_length`** module has been created to assist with the false-positive of the `VIOL_QUERY_STRING_LENGTH` violations. It can modify the configured length on the file type extensions of a NAP/AWAF policy.

Below you can find the input/outout parameters for the module

Input:
- **policy_path** (location of policy file)
- **filetype** (name of the file extension that you want to modify the length)
- **length** (the length that you would like to configure for a spefic file extension)
- **format** (*json* or *yaml*)

Output
- **policy** (Policy output)
- **msg** (Message from the module)
- **changed** (True/False)

## Examples of using the module on a playbook
  Input policy `waf_policy.yaml`
  
  ```yaml
  apiVersion: appprotect.f5.com/v1beta1
  kind: APPolicy
  metadata:
    name: waf_policy
  spec:
    policy:
      applicationLanguage: utf-8
      enforcementMode: blocking
      name: policy
      template:
        name: POLICY_TEMPLATE_NGINX_BASE
  ```

  RUN Playbook to modify the `Query String Length` for a specific filetype `php`
  ```yaml
  - name: File Types
    hosts: localhost
    tasks:
      - name: Allow a specific filetype
        viol_query_string_length:
          policy_path: waf_policy.yaml
          filetype: php
          length: 2048
          format: yaml
  ```

  Output of updated policy.
  ```yaml
  apiVersion: appprotect.f5.com/v1beta1
  kind: APPolicy
  metadata:
    name: waf_policy
  spec:
    policy:
      applicationLanguage: utf-8
      enforcementMode: blocking
      filetypes:                          ### Changes added by ansible module
      - checkQueryStringLength: true      ### Changes added by ansible module
        name: php                         ### Changes added by ansible module
        queryStringLength: 2048           ### Changes added by ansible module
      name: waf_policy
      template:
        name: POLICY_TEMPLATE_NGINX_BASE
  ```



