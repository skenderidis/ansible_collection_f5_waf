# Managing Security Policies with Ansible Modules for F5 and NGINX Web Application Firewall (WAF)
Web Application Firewalls (WAFs) are essential components of modern cybersecurity infrastructure, protecting web applications from a variety of threats including SQL injection, cross-site scripting (XSS), and other malicious activities. In this guide, we'll explore how to leverage Ansible modules to manage security policies for BIGIP AWAF and NGINX AppProtect using JSON and YAML configuration files.

**Prerequisites**
Ansible Installed: Ensure that Ansible is installed on your local machine or Ansible control node.


Violations Supported

| Violations  | module | Support | Status | |
| ------------- | ------------- | ------------- | ------------- | ------------- |
| Manage Blocking Settings  | blocking_settings  |  AWAF / NAP  |  100%  | [Examples](#) |
| Manage Enforcement Mode | enforcement_mode  |  AWAF / NAP  |  100%  | [Examples](#) |
| VIOL_ATTACK_SIGNATURE  | viol_attack_signature  |  AWAF / NAP  |  100%  | [Examples](signatures.md) |
| VIOL_ATTACK_SIGNATURE  | viol_attack_signature_global  |  AWAF / NAP  |  100%  | [Examples](signatures.md) |
| VIOL_FILETYPE | viol_filetype  |  AWAF / NAP  |  100%  | [Examples](file_types.md)| 
| VIOL_POST_DATA_LENGTH | viol_post_data_length  |  AWAF / NAP  |  100%  | [Examples](file_length.md) |
| VIOL_QUERY_STRING_LENGTH | viol_query_string_length  |  AWAF / NAP  |  100%  | [Examples](file_length.md) |
| VIOL_REQUEST_LENGTH | viol_request_length  |  AWAF / NAP  |  100%  | [Examples](file_length.md) |
| VIOL_URL_LENGTH | viol_url_length  |  AWAF / NAP  |  100%  | [Examples](file_length.md) |
| VIOL_HTTP_PROTOCOL | viol_http_protocol  |  AWAF / NAP  |  100%  | [Examples](http_protocol.md) |
| VIOL_EVASION | viol_evasion  |  AWAF / NAP  |  100%  | [Examples](evasion.md) |
| VIOL_URL  |  viol_url  |  AWAF / NAP  |  100%  | [Examples](url.md) |
| VIOL_METHOD  |  viol_method  |  AWAF / NAP  |  100%  | [Examples](method.md) |
| VIOL_HEADER_LENGTH  |  viol_header_length  |  AWAF / NAP  |  100%  | [Examples](header_length.md) |
| VIOL_COOKIE_LENGTH  |  viol_cookie_length  |  AWAF / NAP  |  100%  | [Examples](cookie_length.md) |
| VIOL_COOKIE_MODIFIED  |  viol_cookie_modified  |  AWAF / NAP  | 100%  | [Examples](cookie_modified.md) |
| VIOL_HTTP_RESPONSE_STATUS  |  viol_http_response_status  |  AWAF / NAP  | 100%  | [Examples](status_code.md) |
| VIOL_THREAT_CAMPAIGN  |  viol_threat_campaign |  AWAF / NAP  |  100%  | [Examples](threat_campaign.md) |
| VIOL_PARAMETER  |  viol_parameter  |  AWAF / NAP  |  100%  | [Examples](parameter.md) |
| VIOL_MANDATORY_HEADER  |  viol_mandatory_header  |  AWAF / NAP  | 100%  | [Examples](mandatory_header.md) |
| VIOL_MANDATORY_PARAMETER  | viol_mandatory_parameter   |  AWAF / NAP  | 100%  | [Examples](mandatory_parameter.md) |
| VIOL_PARAMETER_EMPTY_VALUE  |  viol_parameter_empty_value  |  AWAF / NAP  | 100%  | [Examples](parameter_empty.md) |
| VIOL_PARAMETER_REPEATED  |  viol_parameter_repeated  |  AWAF / NAP  | 100%  | [Examples](parameter_repeated.md) |
| VIOL_PARAMETER_DATA_TYPE  |  viol_parameter_data_type  |  AWAF / NAP  | 100%  | [Examples](parameter_data_type.md) |
| VIOL_PARAMETER_LOCATION  |    |  - / -  | 0%  | [Pending]() |
| VIOL_PARAMETER_NAME_METACHAR  |    |  - / -  |  0%  | [Pending]() |
| VIOL_PARAMETER_VALUE_METACHAR  |    |  - / -  |  0%  | [Pending]() |
| VIOL_URL_METACHAR  |    |  - / -  |  0%  | [Pending]() |
| VIOL_HEADER_METACHAR  |    |  - / -  |  0%  | [Pending]() |
| VIOL_MANDATORY_REQUEST_BODY  |    |  - / -  |  0%  | [Pending]() |
| VIOL_PARAMETER_ARRAY_VALUE  |    |  - / -  |  0%  | [Pending]() |
| VIOL_PARAMETER_MULTIPART_NULL_VALUE  |    |  - / -  |  0%  | [Pending]() |
| VIOL_PARAMETER_NUMERIC_VALUE  |    |  - / -  |  0%  | [Pending]() |
| VIOL_PARAMETER_STATIC_VALUE  |    |  - / -  |  0%  | [Pending]() |
| VIOL_PARAMETER_VALUE_BASE64  |    |  - / -  |  0%  | [Pending]() |
| VIOL_PARAMETER_VALUE_LENGTH  |    |  - / -  |  0%  | [Pending]() |
| VIOL_PARAMETER_VALUE_REGEXP  |    |  - / -  |  0%  | [Pending]() |
| VIOL_RATING_THREAT  |    |  - / -  |  0%  | [Pending]() |
| VIOL_RATING_NEED_EXAMINATION  |    |  - / -  |  0%  | [Pending]() |
| VIOL_BOT_CLIENT  |    |  - / -  |  0%  | [Pending]() |
| VIOL_ASM_COOKIE_MODIFIED  |    |  - / -  |  0%  | [Pending]() |
| VIOL_BLACKLISTED_IP  |    |  - / -  |  0%  | [Pending]() |
| VIOL_COOKIE_EXPIRED  |    |  - / -  |  0%  | [Pending]() |
| VIOL_COOKIE_MALFORMED  |    |  - / -  |  0%  | [Pending]() |
| VIOL_DATA_GUARD  |    |  - / -  |  0%  | [Pending]() |
| VIOL_ENCODING  |    |  - / -  |  0%  | [Pending]() |
| VIOL_FILE_UPLOAD  |    |  - / -  |  0%  | [Pending]() |
| VIOL_FILE_UPLOAD_IN_BODY  |    |  - / -  |  0%  | [Pending]() |
| VIOL_GRAPHQL_MALFORMED  |    |  - / -  |  0%  | [Pending]() |
| VIOL_GRAPHQL_FORMAT  |    |  - / -  |  0%  | [Pending]() |
| VIOL_GRAPHQL_INTROSPECTION_QUERY  |    |  - / -  |  0%  | [Pending]() |
| VIOL_GRAPHQL_ERROR_RESPONSE  |    |  - / -  |  0%  | [Pending]() |
| VIOL_GRPC_FORMAT  |    |  - / -  |  0%  | [Pending]() |
| VIOL_GRPC_MALFORMED  |    |  - / -  |  0%  | [Pending]() |
| VIOL_GRPC_METHOD  |    |  - / -  |  0%  | [Pending]() |
| VIOL_JSON_FORMAT  |    |  - / -  |  0%  | [Pending]() |
| VIOL_JSON_MALFORMED  |    |  - / -  |  0%  | [Pending]() |
| VIOL_JSON_SCHEMA  |    |  - / -  |  0%  | [Pending]() |
| VIOL_REQUEST_MAX_LENGTH  |    |  - / -  |  0%  | [Pending]() |
| VIOL_URL_CONTENT_TYPE  |    |  - / -  |  0%  | [Pending]() |
| VIOL_XML_FORMAT  |    |  - / -  |  0%  | [Pending]() |
| VIOL_XML_MALFORMED  |    |  - / -  |  0%  | [Pending]() |




## VIOL_ATTACK_SIGNATURE
The `signatures` ansible module helps disable/enable signatures either globally or on a specific entity. The entities supported from NAP are ***`urls / headers / parameters / cookies`***

Input:
- policy_path (location of policy file)
- signature_id (signature ID that you want to disable/enable)
- format (json or yaml)
- enabled (**True** or **False**. Defaults to True)
- entity_type (urls/headers/parameters/cookies) **optional**
- entity (the name of the entity you want to configure the signature override) **optional**

Output
- policy (the output of the policy)
- msg (Message from the module)
- chaged (if there was a change in the configuration)

### Examples of using the module on a playbook

1. Disable a signature globaly
```yml
- name: Attack signatures
  hosts: localhost
  tasks:
    - name: Disable Signature globaly
      signatures:
        signature_id: 13972332
        enabled: False
        policy_path: "policy.yaml"
        format: yaml
      register: result

    - name: Display Module Output
      debug:
        var: result.policy

    - name: Display Module Output
      debug:
        var: result.msg
```

1. Disable a signature on a URL entity
```yml
- name: Attack signatures
  hosts: localhost
  tasks:
    - name: Disable Signature on a URL entity
      signatures:
        signature_id: 13972332
        enabled: False
        policy_path: "policy.yaml"
        entity_type: urls
        entity: /index.php
        format: yaml
      register: result

    - name: Display Module Output
      debug:
        var: result.policy

    - name: Display Module Output
      debug:
        var: result.msg
```

1. Disable a signature on a Header entity
```yml
- name: Attack signatures
  hosts: localhost
  tasks:
    - name: Disable Signature on a URL entity
      signatures:
        signature_id: 13972332
        enabled: False
        policy_path: "policy.yaml"
        entity_type: headers
        entity: Referer
        format: yaml
      register: result

    - name: Display Module Output
      debug:
        var: result.policy

    - name: Display Module Output
      debug:
        var: result.msg
```

## VIOL_FILETYPE

The `file_types` module helps disable/enable file extensions that have been configured on the `disallowed` list or have not been configured on the explicit `allowed` list. 

Input:
- policy_path (location of policy file)
- filetype (extensions that you want to disable/enable)
- format (json or yaml)
- enabled (True or False. Defaults to True)

Output
- policy (the output of the policy)
- msg (Message from the module)
- chaged (if there was a change in the configuration)

### Examples of using the module on a playbook

1. Disable a signature globaly
```yml
- name: File Types
  hosts: localhost
  tasks:
    - name: Allow File type
      signatures:
        filetype: "bak"
        policy_path: "policy.yaml"
        format: yaml
        enabled: True
      register: result

    - name: Display Module Output
      debug:
        var: result.policy

    - name: Display Module Output
      debug:
        var: result.msg
```
