# VIOL_HTTP_PROTOCOL module

The **`http_protocol`** module has been created to assist with the false-positive of the `VIOL_HTTP_PROTOCOL` violations. It can allow/disallow of the subviolations defined under the `VIOL_HTTP_PROTOCOL` violation on the NGINX App Protect or F5 AWAF declarative waf policy. The list of allowed subviolations are:

1. Unparsable request content
1. Several Content-Length headers
1. POST request with Content-Length: 0
2. Null in request
1. No Host header in HTTP/1.1 request
1. Multiple host headers 
1. Host header contains IP address 
1. High ASCII characters in headers 
1. Header name with no header value 
1. Content length should be a positive number 
1. Chunked request with Content-Length header 
1. Check maximum number of parameters 
1. Check maximum number of headers 
1. Unescaped space in URL 
1. Body in GET or HEAD requests 
1. Bad multipart/form-data request parsing
1. Bad multipart parameters parsing 
1. Bad HTTP version
1. Bad host header value
1. Check maximum number of cookies

It's important to note that only specific key/value pairs within the JSON files are modified, while other aspects of the policy remain unchanged.
In the JSON below you can find the key/values that the module will modify.

```json
{
  "policy": {
    "blocking-settings": {
      "http-protocols": [
        {
          "description": "Body in GET or HEAD requests",
          "enabled": false
        }
      ]
    }
  }
}
```

Below you can find the input/outout parameters for the module

**Input**:
- **policy_path** (location of policy file)
- **http_protocol** (Sub-violation that you want to disable/enable)
- **format** (*json* or *yaml*)
- **enabled** (*True* or *False*. Defaults to True)

**Output**:
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

2. Run the Ansible playbook to allow the subviolation **Body in GET or HEAD requests**
    ```yaml
    - name: VIOL_HTTP_PROTOCOL
      hosts: localhost
      collections:
        - skenderidis.f5_awaf   
      tasks:
        - name: Disable/Enable HTTP Protocol Violations
          viol_http_protocol:
            policy_path: waf_policy.yaml
            http_protocol: Body in GET or HEAD requests
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
        blocking-settings:
          http-protocols:
          - description: Body in GET or HEAD requests
            enabled: false
        enforcementMode: transparent
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
2. Run the Ansible playbook to allow the subviolation **Body in GET or HEAD requests**.
    ```yaml
    - name: VIOL_HTTP_PROTOCOL
      hosts: localhost
      collections:
        - skenderidis.f5_awaf   
      tasks:
        - name: Disable/Enable HTTP Protocol Violations
          viol_http_protocol:
            policy_path: waf_policy.json
            http_protocol: Body in GET or HEAD requests
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
        "blocking-settings": {
          "http-protocols": [
            {
              "description": "Body in GET or HEAD requests",
              "enabled": false
            }
          ]
        }
      }
    }
    ```