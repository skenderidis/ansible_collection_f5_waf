# VIOL_ENFORCEMENT module

The **`viol_enforcement`** module has been created to allow the user modify the enforcementMode of the waf policy. The allowed entries for the enforcementMode key are:

1. blocking
1. transparent

Below you can find the input/outout parameters for the module

Input:
- **policy_path** (location of policy file)
- **enforcement** (*blocking* or *transparent*.)
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
