# VIOL_QUERY_STRING_LENGTH module

The **`viol_request_length`** module has been created to assist with the false-positive of the `VIOL_QUERY_STRING_LENGTH` violations. It can modify the configured query string length on the file type extensions of an NGINX App Protect or an F5 AWAF declarative waf policy.

```json
{
  "policy": {
    "filetypes": [
      {
        "name": "php",
        "queryStringLength": 2048,
        "checkQueryStringLength": true
      }
    ]
  }
}
```


Below you can find the input/outout parameters for the module

Input:
- **policy_path** (location of policy file)
- **filetype** (name of the file extension that you want to modify the length)
- **length** (the length that you would like to configure for a spefic file extension)
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
      name: policy
      template:
        name: POLICY_TEMPLATE_NGINX_BASE
  ```

2. Run the Ansible playbook to modify the **Query String length** for a specific filetype
    ```yaml
    - name: VIOL_QUERY_STRING_LENGTH
      hosts: localhost
      collections:
        - skenderidis.f5_awaf   
      tasks:
        - name: Modify Query String Length
          viol_query_string_length:
            policy_path: waf_policy.yaml
            filetype: php
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
        filetypes:
        - checkQueryStringLength: true
          name: php
          queryStringLength: 2048
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


2. Run the Ansible playbook to modify the **Query String length** for a specific filetype
    ```json
    - name: VIOL_QUERY_STRING_LENGTH
      hosts: localhost
      collections:
        - skenderidis.f5_awaf   
      tasks:
        - name: Modify Query String Length
          viol_query_string_length:
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
        "filetypes": [
          {
            "name": "php",
            "queryStringLength": 2048,
            "checkQueryStringLength": true
          }
        ]
      }
    }
    ```