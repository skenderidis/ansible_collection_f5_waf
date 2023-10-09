# HTTP_compliance module

The **`http_compliance`** ansible module helps users enable/disable specific HTTP_Protocol sub-violations.

The list of NAP sub-violations

  1. `Unparsable request content`
  1. `Several Content-Length headers`
  1. `POST request with Content-Length: 0`
  1. `Null in request`
  1. `No Host header in HTTP/1.1 request`
  1. `Multiple host headers``Host header contains IP address`
  1. `High ASCII characters in headers`
  1. `Header name with no header value`
  1. `Content length should be a positive number`
  1. `Chunked request with Content-Length header`
  1. `Check maximum number of parameters`
  1. `Check maximum number of headers`
  1. `Unescaped space in URL`
  1. `Body in GET or HEAD requests`
  1. `Bad multipart/form-data request parsing`
  1. `Bad multipart parameters parsing`
  1. `Bad HTTP version`
  1. `Bad host header value`
  1. `Check maximum number of cookies`


Input:
- **policy_path** (location of policy file)
- **subviolation** (the specific subviolation that needs to be enabled/disabled)
- **format** (json or yaml)
- **enabled** (True or False. Defaults to False)

Output
- **policy** (the output of the policy)
- **msg** (Message from the module)
- **changed** (if there was a change in the configuration)

### Examples of using the module on a playbook

1. Disable a signature globaly
```yml
- name: File Types
  hosts: localhost
  tasks:
    - name: Allow File type
      http_compliance:
        subviolation: "Bad HTTP version"
        policy_path: "policy.yaml"
        format: yaml
        enabled: False
      register: result

    - name: Display Module Output
      debug:
        var: result.policy

    - name: Display Module Output
      debug:
        var: result.msg
```
