# VIOL_METHOD module

The **`viol_method`** module has been created to assist with the false-positive of the `VIOL_METHOD` violations. It can add methods onto the allowed list of the NGINX App Protect or F5 AWAF declarative waf policy. 

Below you can find the input/outout parameters for the module

**Input**:
- **policy_path** (location of policy file)
- **method** (Method you want to allow)
- **format** (*json* or *yaml*)

**Output**:
- **policy** (Policy output)
- **msg** (Message from the module)
- **changed** (True/False)

> Note: By using this module the policy file will be updated with the new configuration.

> [!IMPORTANT] 
It's important to note that only specific key/value pairs within the JSON files are modified, while other aspects of the policy remain unchanged.
In the JSON below you can find the key/values that the module will modify.

```json
{
  "policy": {
    "methods": [
      {
        "name": "DELETE"
      }
    ]
  }
}
```
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

2. Run the Ansible playbook to allow a **Method**
    ```yaml
    - name: VIOL_METHOD
      hosts: localhost
      collections:
        - skenderidis.f5_awaf   
      tasks:
        - name: Modify Allowed Methods
          viol_method:
            policy_path: waf_policy.yaml
            method: DELETE
            format: yaml
    ```

3. Updated waf policy
    ```yaml
    apiVersion: appprotect.f5.com/v1beta1
    kind: APPolicy
    metadata:
      name: waf_policy
    spec:
      policy:
        applicationLanguage: utf-8
        enforcementMode: blocking
        methods:
        - name: DELETE
        name: waf_policy
        template:
          name: POLICY_TEMPLATE_NGINX_BASE
    ```


## Example of using the ansible module with a JSON waf policy
1. Input policy `waf_policy.json`
    ```json
    {
      "policy": {
        "name": "waf_policy",
        "template": {
          "name": "POLICY_TEMPLATE_NGINX_BASE"
        },
        "applicationLanguage": "utf-8",
        "enforcementMode": "blocking"
      }
    }
    ```
    ```

2. Run the Ansible playbook to allow a **Method**
    ```yaml
    - name: VIOL_METHOD
      hosts: localhost
      collections:
        - skenderidis.f5_awaf   
      tasks:
        - name: Modify Allowed Methods
          viol_method:
            policy_path: waf_policy.json
            method: DELETE
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
        "methods": [
          {
            "name": "DELETE"
          }
        ]
      }
    }
    ```