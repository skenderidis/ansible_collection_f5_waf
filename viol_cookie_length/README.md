# VIOL_COOKIE_LENGTH module

The **`viol_cookie_length`** module has been created to assist with the false-positive of the `VIOL_COOKIE_LENGTH` violations. It can modify the allowed length for the Cookies of a NAP/AWAF policy

Below you can find the input/outout parameters for the module

Input:
- **policy_path** (location of policy file)
- **value** (the length that you would like to configure for the Cookie headers)
- **format** (*json* or *yaml*)

Output
- **policy** (Policy output)
- **msg** (Message from the module)
- **changed** (True/False)

## Examples of using the module on a playbook

1. Input policy `app1_waf.yaml`

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

2. Playbook to modify the configured length for Cookies.
  ```yaml
  - name: Configure Cookie Length
    hosts: localhost
    collections:
      - skenderidis.f5_awaf
    tasks:
      - name: Modify the allowed length of the cookies
        cookie_length:
          value: 4096
          policy_path: app1_waf.yaml
          format: yaml
        register: result
  ```

3.  Updated policy.
  ```yaml
  apiVersion: appprotect.f5.com/v1beta1
  kind: APPolicy
  metadata:
    name: app1_waf
  spec:
    policy:
      applicationLanguage: utf-8
      enforcementMode: blocking
      cookie-settings:                  ### Changes added by ansible module
        maximumCookieHeaderLength: 4096   ### Changes added by ansible module
      name: app1_waf
      template:
        name: POLICY_TEMPLATE_NGINX_BASE
  ```
