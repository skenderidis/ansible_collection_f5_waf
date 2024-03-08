# viol_filetype Module

The **`viol_filetype`** module has been created to assist with the false-positive of the `VIOL_FILETYPE` violations. It can allow/disallow file type extensions on the NGINX App Protect or F5 AWAF declarative waf policy.

Below you can find the input/outout parameters for the module

**Input**:
- **policy_path** (location of policy file)
- **filetype** (extensions that you want to disable/enable)
- **format** (*json* or *yaml*)
- **enabled** (*True* or *False*. Defaults to True)

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
    "filetypes": [
      {
        "allowed": true,
        "name": "php"
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

2. Run the Ansible playbook to allow the file type **php**.
    ```yaml
    - name: File Types
      hosts: localhost
      tasks:
        - name: Allow/Disallow a specific filetype
          file_types:
            policy_path: waf_policy.yaml
            filetype: php
            enabled: True
            format: yaml
          register: result
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
        filetypes:
        - allowed: true
          name: php
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

2. Run the Ansible playbook to allow the file type **php**.
    ```yaml
    - name: File Types
      hosts: localhost
      tasks:
        - name: Allow/Disallow a specific filetype
          file_types:
            policy_path: waf_policy.json
            filetype: php
            enabled: True
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
        "filetypes": [
          {
            "allowed": true,
            "name": "php"
          }
        ]
      }
    }
    ```




