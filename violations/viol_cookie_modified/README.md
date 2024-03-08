# VIOL_COOKIE_MODIFIED module

The **`viol_cookie_modified`** module has been created to assist with the false-positive of the `VIOL_COOKIE_MODIFIED`violations. It can configure the enforcementType of a cookie to either `allow` or `enforced` based on the cookie settings of the NGINX App Protect or F5 AWAF declarative waf policy.

It's important to note that only specific key/value pairs within the JSON files are modified, while other aspects of the policy remain unchanged.
In the JSON below you can find the key/values that the module will modify.

```json
{
  "policy": {
    "cookies": [
      {
        "enforcementType": "allow",
        "name": "user"
      }
    ]
  }
}
```

Below you can find the input/outout parameters for the module

**Input**:
- **policy_path** (location of policy file)
- **enforcementType** (the enforcementType of the cookie. This can be either `allow`, `enforce`)
- **cookie_name** (name of the cookie that you want to modify the enforcementType)
- **format** (*json* or *yaml*)

**Output**:
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

2. Run the Ansible playbook to modify the enforcementType for a specific cookie `user`
    ```yaml
    - name: VIOL_COOKIE_MODIFIED
      hosts: localhost
      tasks:
        - name: Modify the enforcementType of cookies
          viol_cookie_modified:
            policy_path: waf_policy.yaml
            cookie_name: user
            enforcementType: enforce
            format: yaml
    ```

3. Updated waf policy
  ```yaml
  apiVersion: appprotect.f5.com/v1beta1
  kind: APPolicy
  metadata:
    name: app1_waf
  spec:
    policy:
      applicationLanguage: utf-8
      cookies:
      - enforcementType: allow
        name: user
      enforcementMode: blocking
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
2. Run the Ansible playbook to modify the enforcementType for a specific cookie `user`
    ```yaml
    - name: VIOL_COOKIE_MODIFIED
      hosts: localhost
      tasks:
        - name: Modify the enforcementType of cookies
          viol_cookie_modified:
            policy_path: waf_policy.json
            cookie_name: user
            enforcementType: enforce
            format: json
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
        "cookies": [
          {
            "enforcementType": "allow",
            "name": "user"
          }
        ]
      }
    }
    ```