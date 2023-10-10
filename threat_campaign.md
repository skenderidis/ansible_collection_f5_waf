# Threat_campaign module

The **`threat_campaign`** module has been created to assist with the false-positive of the `VIOL_THREAT_CAMPAIGN` violations. It is used to disable/enable theat campaign signatures.

Below you can find the input/outout parameters for the module

Input:
- **policy_path** (location of policy file)
- **name** (signature ID that you want to disable/enable)
- **format** (*json* or *yaml*)
- **enabled** (*True* or *False*. Defaults to False)

Output
- **policy** (Policy output)
- **msg** (Message from the module)
- **changed** (True/False)


> Note: By using this module the policy file will be updated with the new configuration.

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

  Playbook to disable threat campaign signature.
  ```yaml
  - name: Attack signatures
    hosts: localhost
    tasks:
      - name: disable threat campaign
        threat_campaign:
          name: PHPUnit Eval_stdin Remote Code Execution
          enabled: False
          policy_path: app1_waf.yaml
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
      name: app1_waf
      template:
        name: POLICY_TEMPLATE_NGINX_BASE
      threat-campaigns:                                 ### Changes added by ansible module
      - isEnabled: false                                ### Changes added by ansible module
        name: PHPUnit Eval_stdin Remote Code Execution  ### Changes added by ansible module