# Status_code module

The **`status_code`** module has been created to assist with the false-positive of the `VIOL_HTTP_RESPONSE_STATUS` violations. It can assist by adding the HTTP response code on the allowed list.

Below you can find the input/outout parameters for the module

Input:
- **policy_path** (location of policy file)
- **value** (the length that you would like to configure for the HTTP headers)
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

  Playbook to include the HTTP Status code to the allowed list.
  ```yaml
  - name: File Types
    hosts: localhost
    tasks:
      - name: Modify the allowed length of the HTTP Headers
        status_code:
          code: 409
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
      general:
        allowedResponseCodes:   ### Changes added by ansible module
        - 400                   ### Changes added by ansible module
        - 401                   ### Changes added by ansible module
        - 404                   ### Changes added by ansible module
        - 407                   ### Changes added by ansible module
        - 417                   ### Changes added by ansible module
        - 503                   ### Changes added by ansible module
        - 409                   ### Changes added by ansible module
      name: app1_waf
      template:
        name: POLICY_TEMPLATE_NGINX_BASE
  ```
