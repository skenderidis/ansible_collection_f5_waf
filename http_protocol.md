# HTTP_Protocol

The **`http_protocol`** module has been created to assist with the false-positive of the `VIOL_HTTP_PROTOCOL` violations. It can allow/disallow of the subviolations defined under the `VIOL_HTTP_PROTOCOL` violation. The list of the subviolations are:

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

## Examples of using the module on a playbook

### Allow a disallowed file type (php)
  Input policy `app1_waf.yaml`
  ```yaml
  apiVersion: appprotect.f5.com/v1beta1
  kind: APPolicy
  metadata:
    name: app1_waf
  spec:
    policy:
      applicationLanguage: utf-8
      enforcementMode: blocking
      name: app1_waf
      template:
        name: POLICY_TEMPLATE_NGINX_BASE
  ```


  Playbook to allow the subviolation **Body in GET or HEAD requests**.
  ```yaml
  - name: File Types
    hosts: localhost
    tasks:
      - name: Allow a specific filetype
        http_protocol:
          subviolation: Body in GET or HEAD requests
          enabled: True
          policy_path: app1_waf.yaml
          format: yaml
        register: result
  ```

  Updated policy.
  ```yaml
  apiVersion: appprotect.f5.com/v1beta1
  kind: APPolicy
  metadata:
    name: app1_waf
  spec:
    policy:
      applicationLanguage: utf-8
      blocking-settings:                                ### Changes added by ansible module
        http-protocols:                                 ### Changes added by ansible module
        - description: Body in GET or HEAD requests     ### Changes added by ansible module
          enabled: true                                 ### Changes added by ansible module
      enforcementMode: blocking
      name: app1_waf
      template:
        name: POLICY_TEMPLATE_NGINX_BASE
  ```
