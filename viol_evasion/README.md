# VIOL_EVASION module

The **`viol_evasion`** module has been created to assist with the false-positive of the `VIOL_EVASION` violations. It can allow/disallow of the subviolations defined under the `VIOL_EVASION` violation on the NGINX App Protect or F5 AWAF declarative waf policy. The list of allowed subviolations are:

1. %u decoding
1. Apache whitespace
1. Bad unescape
1. Bare byte decoding
1. Directory traversals
1. IIS backslashes
1. IIS Unicode codepoints
1. Multiple decoding

```json
{
  "policy": {
    "blocking-settings": {
      "evasions": [
        {
          "description": "IIS backslashes",
          "enabled": false
        }
      ]
    }
  }
}
```

Below you can find the input/outout parameters for the module

Input:
- **policy_path** (location of policy file)
- **subviolation** (Sub-violation that you want to disable/enable)
- **format** (*json* or *yaml*)
- **enabled** (*True* or *False*. Defaults to True)

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

2. Run the Ansible playbook to allow the subviolation  **IIS Unicode codepoints**
    ```yaml
    - name: VIOL_EVASION
      hosts: localhost
      collections:
        - skenderidis.f5_awaf   
      tasks:
        - name: Modify Evasion techniques
          viol_evasion:
            policy_path: waf_policy.yaml
            evasion: IIS Unicode codepoints
            enabled: True
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
        blocking-settings:
          evasions:
          - description: IIS Unicode codepoints
            enabled: true
        enforcementMode: blocking
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
2. Run the Ansible playbook to allow the subviolation  **IIS Unicode codepoints**
    ```yaml
    - name: VIOL_EVASION
      hosts: localhost
      collections:
        - skenderidis.f5_awaf   
      tasks:
        - name: Modify Evasion techniques
          viol_evasion:
            policy_path: waf_policy.json
            evasion: IIS Unicode codepoints
            enabled: True
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
        "blocking-settings": {
          "evasions": [
            {
              "description": "IIS Unicode codepoints",
              "enabled": false
            }
          ]
        }
      }
    }
    ```
