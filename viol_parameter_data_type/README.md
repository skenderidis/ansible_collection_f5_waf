# VIOL_PARAMETER_DATA_TYPE module

The **`viol_parameter_data_type`** module has been created to assist with the false-positive of the `VIOL_PARAMETER_DATA_TYPE` violations. It can modify the data-type configured for each parameter. The list of the `Data types` are:

1. alpha-numeric
1. binary
1. phone
1. email
1. boolean
1. integer
1. decimal

Below you can find the input/outout parameters for the module

Input:
- **policy_path** (location of policy file)
- **parameter_name** (The name of the parameter you want to modify)
- **data_type** (Data Type configured for the parameter)
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
  - name: File Types
    hosts: localhost
    collections:
      - skenderidis.f5_awaf   
    tasks:
      - name: Disable threat_campaign
        viol_parameter_data_type:
          policy_path: policy.yaml
          parameter_name: test
          data_type: integer
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
