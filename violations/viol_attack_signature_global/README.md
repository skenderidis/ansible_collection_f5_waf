# VIOL_ATTACK_SIGNATURE_GLOBAL module

The **viol_attack_signature_global** module has been created to assist with the false-positive of the `VIOL_ATTACK_SIGNATURE` violations. It can can disable/enable signatures globally on the NGINX App Protect or F5 AWAF declarative waf policy.

It's important to note that only specific key/value pairs within the JSON files are modified, while other aspects of the policy remain unchanged.
In the JSON below you can find the key/values that the module will modify.

```json
{
  "policy": {
    "signatures": [
      {
        "signatureId": 200001834,
        "enabled": false
      }
    ]
  }
}
```

Below you can find the input/outout parameters for the module

Input:
- **policy_path** (location of policy file)
- **signature_id** (signature ID that you want to disable/enable)
- **format** (*json* or *yaml*)
- **enabled** (*True* or *False*. Defaults to False)

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

2. Run the Ansible playbook to disable signature globally
    ```yaml
    - name: Disable signature globaly
      hosts: localhost
      collections:
        - skenderidis.f5_awaf
      tasks:
        - name: Disable signature globaly
          signatures:
            policy_path: waf_policy.yaml
            signature_id: 200001834
            enabled: False
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
        name: waf_policy
        signatures:
        - enabled: false
          signatureId: 200001834
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

2. Run the Ansible playbook to disable signature globally
    ```yaml
    - name: Disable signature globaly
      hosts: localhost
      collections:
        - skenderidis.f5_awaf
      tasks:
        - name: Disable signature globaly
          signatures:
            policy_path: waf_policy.json
            signature_id: 200001834
            enabled: False
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
        "signatures": [
          {
            "signatureId": 200001834,
            "enabled": false
          }
        ]
      }
    }
    ```