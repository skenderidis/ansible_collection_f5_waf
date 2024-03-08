# ENFORCEMENT module

The **`enforcement`** module has been created to allow the user modify the enforcementMode of the NGINX App Protect or F5 AWAF declarative waf policy. The allowed entries for the enforcementMode key are:

1. blocking
1. transparent

Below you can find the input/outout parameters for the module

Input:
- **policy_path** (location of policy file)
- **enforcement** (*blocking* or *transparent*.)
- **format** (*json* or *yaml*)

Output
- **policy** (Policy output)
- **msg** (Message from the module)
- **changed** (True/False)

> Note: By using this module the policy file will be updated with the new configuration.

> It's important to note that only specific key/value pairs within the JSON files are modified, while other aspects of the policy remain unchanged.

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

2. Run the Ansible playbook to make the policy to **transparent**
    ```yaml
    - name: Change enforcement mode
      hosts: localhost
      collections:
        - skenderidis.f5_awaf   
      tasks:
        - name: Change enforcement mode
          enforcement_mode:
            policy_path: waf_policy.yaml
            enforcement: transparent
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
2. Run the Ansible playbook to make the policy to **transparent**
    ```yaml
    - name: Change enforcement mode
      hosts: localhost
      collections:
        - skenderidis.f5_awaf   
      tasks:
        - name: Change enforcement mode
          enforcement_mode:
            policy_path: waf_policy.json
            enforcement: transparent
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
        "enforcementMode": "transparent",
      }
    }
    ```