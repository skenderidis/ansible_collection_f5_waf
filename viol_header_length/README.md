# VIOL_HEADER_LENGTH module

The **`viol_header_length`** module has been created to assist with the false-positive of the `VIOL_HEADER_LENGTH` violations. It can modify the allowed length for the HTTP headers of the NGINX App Protect or F5 AWAF declarative waf policy.

```json
{
  "policy": {
    "header-settings": {
        "maximumHttpHeaderLength": 2048
    }
  }
}
```

Below you can find the input/outout parameters for the module

Input:
- **policy_path** (location of policy file)
- **length** (the length that you would like to configure for the HTTP headers)
- **format** (*json* or *yaml*)

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

2. Run the Ansible playbook to modify the configured length for HTTP Headers.
    ```yaml
    - name: VIOL_HEADER_LENGTH
      hosts: localhost
      collections:
        - skenderidis.f5_awaf    
      tasks:
        - name: Configure Header Length
          viol_header_length:
            policy_path: waf_policy.yaml
            length: 2048
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
        header-settings:
          maximumHttpHeaderLength: 2048
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

2. Run the Ansible playbook to modify the configured length for HTTP Headers.
    ```yaml
    - name: VIOL_HEADER_LENGTH
      hosts: localhost
      collections:
        - skenderidis.f5_awaf    
      tasks:
        - name: Configure Header Length
          viol_header_length:
            policy_path: waf_policy.json
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
        "header-settings": {
            "maximumHttpHeaderLength": 2048
        }
      }
    }
    ```