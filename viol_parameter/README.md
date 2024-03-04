# VIOL_PARAMETER module

The **`viol_parameter`** module has been created to assist with the false-positive of the `VIOL_PARAMETER` violations. It can allow/disallow parameters on the waf policy. 

Input:
- **policy_path** (location of policy file)
- **parameter_name** (The name of the parameter you want to modify)
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


  Playbook to allow the subviolation **IIS Unicode codepoints**.
  ```yaml
  - name: VIOL_PARAMETER
    hosts: localhost
    collections:
      - skenderidis.f5_awaf   
    tasks:
      - name: Allow/Disallow Parameter
        viol_parameter:
          policy_path: policy.yaml
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
      blocking-settings:                          ### Changes added by ansible module
        evasions:                                 ### Changes added by ansible module
        - description: IIS Unicode codepoints     ### Changes added by ansible module
          enabled: true                           ### Changes added by ansible module
      enforcementMode: blocking
      name: app1_waf
      template:
        name: POLICY_TEMPLATE_NGINX_BASE
  ```
