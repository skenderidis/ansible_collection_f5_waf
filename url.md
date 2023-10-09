# HTTP_protocol

The **`url`** module has been created to assist with the false-positive of the `VIOL_URL` violations. It can allow/disallow urls on the App Protect Policy. 


Below you can find the input/outout parameters for the module

Input:
- **policy_path** (location of policy file)
- **uri** (URL that you want to disable/enable)
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


  Playbook to allow the url **index.php**.
  ```yaml
  - name: File Types
    hosts: localhost
    tasks:
      - name: Allow a specific url
        url:
          url: index.php
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
      enforcementMode: blocking
      name: app1_waf
      template:
        name: POLICY_TEMPLATE_NGINX_BASE
      urls:                   ### Changes added by ansible module
      - allowed: true         ### Changes added by ansible module
        name: index.php       ### Changes added by ansible module
  ```
