# Url module

The **`url`** module has been created to assist with the false-positive of the `VIOL_URL` violations. It can allow/disallow urls on an NGINX App Protect or an F5 AWAF declarative waf policy.

```json
{
  "policy": {
    "urls": [
      {
        "name": "index.php",
        "allowed": true
      }
    ]
  }
}
```

Below you can find the input/outout parameters for the module

Input:
- **policy_path** (location of policy file)
- **url** (URL that you want to disable/enable)
- **enabled** (*True* or *False*. Defaults to True)
- **format** (*json* or *yaml*)

Output
- **policy** (Policy output)
- **msg** (Message from the module)
- **changed** (True/False)


## Example of using the ansible module with a YAML waf policy

1. Input policy `waf_policy.yaml`.
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

2. Run the Ansible playbook to allow a specific **url**
    ```yaml
    - name: File Types
      hosts: localhost
      tasks:
        - name: Allow a specific url
          url:
            url: index.php
            enabled: True
            policy_path: waf_policy.yaml
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
        name: waf_policy
        template:
          name: POLICY_TEMPLATE_NGINX_BASE
        urls:
        - allowed: true
          name: index.php
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

2. Run the Ansible playbook to modify the **URL length** for a specific filetype
    ```yaml
    - name: File Types
      hosts: localhost
      tasks:
        - name: Allow a specific filetype
          viol_url_length:
            policy_path: waf_policy.json
            filetype: php
            length: 2048
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
            "allowed": true
          }
        ]
      }
    }
    ```



