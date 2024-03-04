# Url module

The **`url`** module has been created to assist with the false-positive of the `VIOL_URL` violations. It can allow/disallow urls on the App Protect Policy. 


Below you can find the input/outout parameters for the module

Input:
- **policy_path** (location of policy file)
- **url** (URL that you want to disable/enable)
- **format** (*json* or *yaml*)
- **enabled** (*True* or *False*. Defaults to True)

Output
- **policy** (Policy output)
- **msg** (Message from the module)
- **changed** (True/False)


## Examples of using the module on a playbook

1. Input policy `waf_policy.yaml`.
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


2. RUN Playbook to allow the url **index.php**.
  ```yaml
  - name: File Types
    hosts: localhost
    tasks:
      - name: Allow a specific url
        url:
          url: index.php
          enabled: True
          policy_path: waf_policy.yaml
          format: yaml
        register: result
  ```

3. Output of updated policy.
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
      urls:                   ### Changes added by ansible module
      - allowed: true         ### Changes added by ansible module
        name: index.php       ### Changes added by ansible module
  ```
