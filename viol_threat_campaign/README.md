# VIOL_THREAT_CAMPAIGN module

The **`viol_threat_campaign`** module has been created to assist with the false-positive of the `VIOL_THREAT_CAMPAIGN` violations. It can disable/enable specific theat campaign signatures of an NGINX App Protect or an F5 AWAF declarative waf policy.

  ```json
  {
    "policy": {
      "threat-campaigns": [
        {
          "name": "PHPUnit Eval_stdin Remote Code Execution",
          "isEnabled": false
        }
      ]
    }
  }
  ```

Below you can find the input/outout parameters for the module

Input:
- **policy_path** (location of policy file)
- **name** (Threat Campaign name that you want to disable/enable)
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

2. Run the Ansible playbook to disable a **threat campaign**
    ```yaml
    - name: VIOL_THREAT_CAMPAIGN
      hosts: localhost
      collections:
        - skenderidis.f5_awaf   
      tasks:
        - name: Disable/Enable threat campaigns
          viol_threat_campaign:
            name: PHPUnit Eval_stdin Remote Code Execution
            enabled: False
            policy_path: waf_policy.yaml
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
        template:
          name: POLICY_TEMPLATE_NGINX_BASE
        threat-campaigns:
        - isEnabled: false
          name: PHPUnit Eval_stdin Remote Code Execution
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

2. Run the Ansible playbook to disable a **threat campaign**
    ```yaml
    - name: VIOL_THREAT_CAMPAIGN
      hosts: localhost
      collections:
        - skenderidis.f5_awaf   
      tasks:
        - name: Disable/Enable threat campaigns
          viol_threat_campaign:
            name: PHPUnit Eval_stdin Remote Code Execution
            enabled: False
            policy_path: waf_policy.json
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
        "threat-campaigns": [
          {
            "name": "PHPUnit Eval_stdin Remote Code Execution",
            "isEnabled": false
          }
        ]
      }
    }
    ```