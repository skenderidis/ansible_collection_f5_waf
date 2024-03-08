# VIOL_PARAMETER module

The **`viol_parameter`** module has been created to assist with the false-positive of the `VIOL_PARAMETER` violations. It can allow/disallow parameters on the NGINX App Protect or F5 AWAF declarative waf policy.

It's important to note that only specific key/value pairs within the JSON files are modified, while other aspects of the policy remain unchanged.
In the JSON below you can find the key/values that the module will modify.

```json
{
  "policy": {
    "parameters": [
      {
        "name": "user",
        "allowed": true
      }
    ]
  }
}
```

**Input**:
- **policy_path** (location of policy file)
- **parameter_name** (The name of the parameter you want to modify)
- **enabled** (*True* or *False*. Defaults to True)
- **format** (*json* or *yaml*)

**Output**:
- **policy** (Policy output)
- **msg** (Message from the module)
- **changed** (True/False)

> Note: By using this module the policy file will be updated with the new configuration.


## Examples of using the module on a playbook
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

2. Run the Ansible playbook to allow a specific **parameter**
    ```yaml
    - name: VIOL_PARAMETER
      hosts: localhost
      collections:
        - skenderidis.f5_awaf   
      tasks:
        - name: Allow/Disallow Parameter
          viol_parameter:
            policy_path: policy.yaml
            parameter_name: user
            enabled: true
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
        enforcementMode: transparent
        name: waf_policy
        parameters:
        - allowed: true
          name: user
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

2. Run the Ansible playbook to allow a specific **parameter**
    ```yaml
    - name: VIOL_PARAMETER
      hosts: localhost
      collections:
        - skenderidis.f5_awaf   
      tasks:
        - name: Allow/Disallow Parameter
          viol_parameter:
            policy_path: policy.json
            parameter_name: user
            enabled: true
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
        "parameters": [
          {
            "name": "user",
            "allowed": true
          }
        ]
      }
    }
    ```