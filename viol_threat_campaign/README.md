# VIOL_THREAT_CAMPAIGN module

The **`viol_threat_campaign`** module has been created to assist with the false-positive of the `VIOL_THREAT_CAMPAIGN` violations. It is used to disable/enable theat campaign signatures.

Below you can find the input/outout parameters for the module

Input:
- **policy_path** (location of policy file)
- **name** (Threat Campaign name that you want to disable/enable)
- **format** (*json* or *yaml*)
- **enabled** (*True* or *False*. Defaults to False)

Output
- **policy** (Policy output)
- **msg** (Message from the module)
- **changed** (True/False)


> Note: By using this module the policy file will be updated with the new configuration.

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

  Playbook to disable threat campaign signature.
  ```yaml
  - name: VIOL_THREAT_CAMPAIGN
    hosts: localhost
    collections:
      - skenderidis.f5_awaf   
    tasks:
      - name: Disable threat campaign
        viol_threat_campaign:
          name: PHPUnit Eval_stdin Remote Code Execution
          enabled: False
          policy_path: waf_policy.yaml
          format: yaml
        register: result
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
      enforcementMode: blocking
      name: waf_policy
      template:
        name: POLICY_TEMPLATE_NGINX_BASE
      threat-campaigns:                                 ### Changes added by ansible module
      - isEnabled: false                                ### Changes added by ansible module
        name: PHPUnit Eval_stdin Remote Code Execution  ### Changes added by ansible module