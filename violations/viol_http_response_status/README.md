# VIOL_HTTP_RESPONSE_STATUS module

The **`viol_http_response_status`** module has been created to assist with the false-positive of the `VIOL_HTTP_RESPONSE_STATUS` violations. It can assist by adding the HTTP response code on the allowed list of the NGINX App Protect or F5 AWAF declarative waf policy.

Below you can find the input/outout parameters for the module

**Input**:
- **policy_path** (location of policy file)
- **code** (the HTTP Response code that you would like to allow)
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
    "general": {
      "allowedResponseCodes": [
        400,
        401,
        404,
        407,
        417,
        503,
        409
      ]
    }
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

2. Run the Ansible playbook to include the HTTP Status code to the allowed list
    ```yaml
    - name: VIOL_HTTP_RESPONSE_STATUS
      hosts: localhost
      collections:
        - skenderidis.f5_awaf   
      tasks:
        - name: Modify HTTP Response Code
          viol_http_response_status:
            policy_path: waf_policy.yaml
            code: 409
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
        general:
          allowedResponseCodes:
          - 400
          - 401
          - 404
          - 407
          - 417
          - 503
          - 409
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

2. Run the Ansible playbook to include the HTTP Status code to the allowed list
    ```yaml
    - name: VIOL_HTTP_RESPONSE_STATUS
      hosts: localhost
      collections:
        - skenderidis.f5_awaf   
      tasks:
        - name: Modify HTTP Response Code
          viol_http_response_status:
            policy_path: waf_policy.json
            code: 409
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
        "general": {
          "allowedResponseCodes": [
            400,
            401,
            404,
            407,
            417,
            503,
            409
          ]
        }
      }
    }
    ```




