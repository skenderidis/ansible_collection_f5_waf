# HTTP_protocol

The **`method`** module has been created to assist with the false-positive of the `VIOL_METHOD` violations. It can add methods onto the allowed list of the App Protect Policy. 

Below you can find the input/outout parameters for the module

Input:
- **policy_path** (location of policy file)
- **method** (Method you want to allow)
- **format** (*json* or *yaml*)

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
        method:
          method: DELETE
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
      methods:                  ### Changes added by ansible module
      - name: DELETE            ### Changes added by ansible module
      name: app1_waf
      template:
        name: POLICY_TEMPLATE_NGINX_BASE
  ```
