# VIOL_PARAMETER_REPEATED module

The **`viol_parameter_repeated`** module has been created to assist with the false-positive of the `VIOL_PARAMETER_REPEATED` violations. It can change the settings that allows/disallows a parameter to be repeated on the NGINX App Protect or F5 AWAF declarative waf policy.

Below you can find the input/outout parameters for the module

**Input**:
- **policy_path** (location of policy file)
- **parameter_name** (the name of the parameter you want to modify)
- **enabled** (*True* or *False*. Defaults to True)
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
    "parameters": [
      {
        "name": "user",
        "allowRepeatedParameterName": false
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

2. Run the Ansible playbook to disable the **repeated** settings for a specific parameter
    ```yaml
    - name: VIOL_PARAMETER_REPEATED
      hosts: localhost
      collections:
        - skenderidis.f5_awaf    
      tasks:
        - name: Modify Parameter's repeated setting
          viol_parameter_repeated:
            policy_path: waf_policy.yaml
            parameter_name: user
            enabled: false
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
        - allowRepeatedParameterName: false
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

2. Run the Ansible playbook to disable the **repeated** settings for a specific parameter
    ```yaml
    - name: VIOL_PARAMETER_REPEATED
      hosts: localhost
      collections:
        - skenderidis.f5_awaf    
      tasks:
        - name: Modify Parameter's repeated setting
          viol_parameter_repeated:
            policy_path: waf_policy.json
            parameter_name: user
            enabled: false
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
            "name": "test",
            "allowRepeatedParameterName": false
          }
        ]
      }
    }
    ```