# VIOL_COOKIE_LENGTH module

The **`viol_cookie_length`** module has been created to assist with the false-positive of the `VIOL_COOKIE_LENGTH` violations. It can modify the allowed length for the Cookies of the NGINX App Protect or F5 AWAF declarative waf policy.

```json
{
  "policy": {
    "cookie-settings": {
        "maximumCookieHeaderLength": 2048
    }
  }
}
```

Below you can find the input/outout parameters for the module

Input:
- **policy_path** (location of policy file)
- **value** (the length that you would like to configure for the Cookie headers)
- **format** (*json* or *yaml*)

Output
- **policy** (Policy output)
- **msg** (Message from the module)
- **changed** (True/False)

> Note: By using this module the policy file will be updated with the new configuration.

## Example of using the ansible module with a YAML waf policy
1. Input policy `waf_policy.yaml` 
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

2. Run the Ansible playbook to modify the configured length for Cookies
    ```yaml
    - name: Configure Cookie Length
      hosts: localhost
      collections:
        - skenderidis.f5_awaf
      tasks:
        - name: Modify the allowed length of cookies
          cookie_length:
            value: 4096
            policy_path: waf_policy.yaml
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
      cookie-settings:
        maximumCookieHeaderLength: 4096
      name: app1_waf
      template:
        name: POLICY_TEMPLATE_NGINX_BASE
  ```


## Example of using the ansible module with a JSON waf policy
1. Input policy `waf_policy.json`
    ```json
    {
      "policy": {
        "applicationLanguage": "utf-8",
        "enforcementMode": "blocking",
        "name": "waf_policy",
        "template": {
          "name": "POLICY_TEMPLATE_NGINX_BASE"
        }
      }
    }
    ```

2. Run the Ansible playbook to modify the configured length for Cookies
    ```yaml
    - name: Configure Cookie Length
      hosts: localhost
      collections:
        - skenderidis.f5_awaf
      tasks:
        - name: Modify the allowed length of cookies
          cookie_length:
            value: 4096
            policy_path: waf_policy.json
            format: json
          register: result
    ```


3. Updated waf policy
    ```json
    {
      "policy": {
        "name": "waf_policy",
        "template": {
          "name": "POLICY_TEMPLATE_NGINX_BASE"
        },
        "applicationLanguage": "utf-8",
        "enforcementMode": "blocking",
        "cookie-settings": {
            "maximumCookieHeaderLength": 4096
        }
      }
    }
    ```

