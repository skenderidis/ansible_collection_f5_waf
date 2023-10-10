# Evasion module

The **`evasion`** module has been created to assist with the false-positive of the `VIOL_EVASION` violations. It can allow/disallow of the subviolations defined under the `VIOL_EVASION` violation. The list of the subviolations are:

1. %u decoding
1. Apache whitespace
1. Bad unescape
1. Bare byte decoding
1. Directory traversals
1. IIS backslashes
1. IIS Unicode codepoints
1. Multiple decoding


Below you can find the input/outout parameters for the module

Input:
- **policy_path** (location of policy file)
- **subviolation** (Sub-violation that you want to disable/enable)
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


  Playbook to allow the subviolation **IIS Unicode codepoints**.
  ```yaml
  - name: File Types
    hosts: localhost
    tasks:
      - name: Allow a specific filetype
        evasion:
          subviolation: IIS Unicode codepoints
          enabled: True
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
      blocking-settings:                        ### Changes added by ansible module
        evasions:                               ### Changes added by ansible module
        - description: IIS Unicode codepoints   ### Changes added by ansible module
          enabled: true                         ### Changes added by ansible module
      enforcementMode: blocking
      name: app1_waf
      template:
        name: POLICY_TEMPLATE_NGINX_BASE
  ```
