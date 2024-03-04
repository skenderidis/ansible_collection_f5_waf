# VIOL_PARAMETER_EMPTY_VALUE module

The **`viol_parameter_empty_value`** module has been created to assist with the false-positive of the `VIOL_PARAMETER_EMPTY_VALUE` violations. It can modify the settings of the  length for the HTTP headers of a NAP policy

Below you can find the input/outout parameters for the module

Input:
- **policy_path** (location of policy file)
- **parameter_name** (the name of the parameter you want to modify)
- **enabled** (*True* or *False*. Defaults to True)
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
      name: waf_policy
      template:
        name: POLICY_TEMPLATE_NGINX_BASE
  ```

  Playbook to modify the configured length for HTTP Headers.
  ```yaml
  - name: VIOL_PARAMETER_REPEATED
    hosts: localhost
    collections:
      - skenderidis.f5_awaf    
    tasks:
      - name: Modify Parameter's repeated setting
        viol_parameter_repeated:
          policy_path: waf_policy.yaml
          parameter_name: test
          enabled: true
          format: yaml
  ```

  Updated policy.
  ```yaml
  apiVersion: appprotect.f5.com/v1beta1
  kind: APPolicy
  metadata:
    name: waf_policy
  spec:
    policy:
      applicationLanguage: utf-8




      name: waf_policy
      template:
        name: POLICY_TEMPLATE_NGINX_BASE
  ```
