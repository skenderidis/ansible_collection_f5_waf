# VIOL_ATTACK_SIGNATURE module

The **viol_attack_signature** module has been created to assist with the false-positive of the `VIOL_ATTACK_SIGNATURE` violations. It can can disable/enable signatures on a specific entity on the NGINX App Protect or F5 AWAF declarative waf policy. The supported entities are the following: 
1. `urls`
2. `headers`
3. `parameters`
4. `cookies`

```json
{
  "policy": {
    "urls": [
      {
        "name": "index.php",
        "signatureOverrides": [
          {
            "signatureId": 204855,
            "enabled": true
          }
        ]
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
- **entity_type** (Signature can be disabled on `urls`, `headers`, `parameters`, `cookies`) 
- **entity** (**Optional** - The name of the entity you want to configure the signature override. If not provided, it will be configured on the wildcard entity) 

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

2. Run the Ansible playbook to disable signature on a specific **url**
    ```yaml
    - name: Disable signature on an entity
      hosts: localhost
      collections:
        - skenderidis.f5_awaf   
      tasks:
        - name: Disable signature on an entity
          viol_attack_signature:
            policy_path: waf_policy.yaml
            signature_id: 200001834
            enabled: true
            entity_type: urls
            entity: index.php 
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
        urls:
        - name: index.php
          signatureOverrides:
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
    - name: Disable signature on an entity
      hosts: localhost
      collections:
        - skenderidis.f5_awaf   
      tasks:
        - name: Disable signature on an entity
          viol_attack_signature:
            policy_path: waf_policy.json
            signature_id: 200001834
            enabled: true
            entity_type: urls
            entity: index.php 
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
        "urls": [
          {
            "name": "index.php",
            "signatureOverrides": [
              {
                "signatureId": 204855,
                "enabled": true
              }
            ]
          }
        ]
      }
    }
    ```
