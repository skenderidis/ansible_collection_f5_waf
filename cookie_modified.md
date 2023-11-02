# Cookie_modified module

The **`cookie_modified`** module has been created to assist with the false-positive of the `VIOL_COOKIE_MODIFIED`violations. It can configure the enforcementType of a cookie to either `allow` or `enforced` based on the cookie settings of a NAP policy.

Below you can find the input/outout parameters for the module

Input:
- **policy_path** (location of policy file)
- **enforcementType** (The enforcementType of the cookie. This can be either `allow`, `enforce`)
- **cookie_name** (name of the cookie that you want to modify the enforcementType)
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

  Playbook to modify the enforcementType for a specific cookie `Temp-Access`
  ```yaml
  - name: File Types
    hosts: localhost
    tasks:
      - name: Allow a specific filetype
        cookie_modified:
          policy_path: policy.yaml
          cookie_name: Temp-Access
          enforcementType: enforce
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
      cookies:                      ### Changes added by ansible module
      - enforcementType: allow      ### Changes added by ansible module
        name: Temp-Access           ### Changes added by ansible module
      enforcementMode: blocking
      name: app1_waf
      template:
        name: POLICY_TEMPLATE_NGINX_BASE
  ```


