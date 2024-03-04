# Header_length module

The **`viol_header_length`** module has been created to assist with the false-positive of the `VIOL_HEADER_LENGTH` violations. It can modify the allowed length for the HTTP headers of a NAP policy

Below you can find the input/outout parameters for the module

Input:
- **policy_path** (location of policy file)
- **length** (the length that you would like to configure for the HTTP headers)
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

  Playbook to modify the configured length for HTTP Headers.
  ```yaml
  - name: VIOL_HEADER_LENGTH
    hosts: localhost
    collections:
      - skenderidis.f5_awaf    
    tasks:
      - name: Configure Header Length
        viol_header_length:
          policy_path: app1_waf.yaml
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
      header-settings:                  ### Changes added by ansible module
        maximumHttpHeaderLength: 4096   ### Changes added by ansible module
      name: app1_waf
      template:
        name: POLICY_TEMPLATE_NGINX_BASE
  ```
