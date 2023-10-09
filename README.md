# nap-ansible

Violations 

| Violations  | module | Status | | |
| ------------- | ------------- | ------------- | ------------- |
| Disable Violation  | violation  |  100%  | [Examples](#) |
| VIOL_ATTACK_SIGNATURE  | signatures  |  100%  | [Examples](viol_attack_signature.md) |
| VIOL_FILETYPE | file_types  |  100%  | [Examples](viol_filetype.md)| 
| VIOL_POST_DATA_LENGTH | file_length  |  100%  | [Examples](file_length.md) |
| VIOL_QUERY_STRING_LENGTH | file_length  |  100%  | [Examples](file_length.md) |
| VIOL_REQUEST_LENGTH | file_length  |  100%  | [Examples](file_length.md) |
| VIOL_URL_LENGTH | file_length  |  100%  | [Examples](file_length.md) |
| VIOL_HTTP_PROTOCOL | http_compliance  |  100%  | [Examples](/http_compliance/) |
| VIOL_EVASION | evasion  |  100%  | [Examples](/evasion/) |
| VIOL_URL  |  url  |  100%  | [Examples](#)  |
| VIOL_METHOD  |  method  |  100%  | [Examples](#)  |
| VIOL_HEADER_LENGTH  |    |  100%  | [Examples](#)  |
| VIOL_COOKIE_LENGTH  |    |  100%  | [Examples](#)  |
| VIOL_COOKIE_MODIFIED  |    | 100%  | [Pending]() |
| VIOL_HTTP_RESPONSE_STATUS  |    | 100%  | [Pending]() |
| VIOL_THREAT_CAMPAIGN  |    |  100%  | [Pending]() |
| VIOL_PARAMETER  |    |  100%  | [Pending]() |
| VIOL_MANDATORY_HEADER  |    | 100%  | [Pending]() |
| VIOL_MANDATORY_PARAMETER  |    | 100%  | [Pending]() |
| VIOL_PARAMETER_EMPTY_VALUE  |    | 100%  | [Pending]() |
| VIOL_PARAMETER_REPEATED  |    | 100%  | [Pending]() |
| VIOL_PARAMETER_LOCATION  |    | 100%  | [Pending]() |
| VIOL_PARAMETER_DATA_TYPE  |    | 100%  | [Pending]() |
| VIOL_PARAMETER_NAME_METACHAR  |    |  100%  | [Pending]() |
| VIOL_PARAMETER_VALUE_METACHAR  |    |  100%  | [Pending]() |
| VIOL_URL_METACHAR  |    |  100%  | [Pending]() |
| VIOL_HEADER_METACHAR  |    |  0%  | [Pending]() |
| VIOL_MANDATORY_REQUEST_BODY  |    |  0%  | [Pending]() |
| VIOL_PARAMETER_ARRAY_VALUE  |    |  0%  | [Pending]() |
| VIOL_PARAMETER_MULTIPART_NULL_VALUE  |    |  0%  | [Pending]() |
| VIOL_PARAMETER_NUMERIC_VALUE  |    |  0%  | [Pending]() |
| VIOL_PARAMETER_STATIC_VALUE  |    |  0%  | [Pending]() |
| VIOL_PARAMETER_VALUE_BASE64  |    |  0%  | [Pending]() |
| VIOL_PARAMETER_VALUE_LENGTH  |    |  0%  | [Pending]() |
| VIOL_PARAMETER_VALUE_REGEXP  |    |  0%  | [Pending]() |
| VIOL_RATING_THREAT  |    |  0%  | [Pending]() |
| VIOL_RATING_NEED_EXAMINATION  |    |  0%  | [Pending]() |
| VIOL_BOT_CLIENT  |    |  0%  | [Pending]() |
| VIOL_ASM_COOKIE_MODIFIED  |    |  0%  | [Pending]() |
| VIOL_BLACKLISTED_IP  |    |  0%  | [Pending]() |
| VIOL_COOKIE_EXPIRED  |    |  0%  | [Pending]() |
| VIOL_COOKIE_MALFORMED  |    |  0%  | [Pending]() |
| VIOL_DATA_GUARD  |    |  0%  | [Pending]() |
| VIOL_ENCODING  |    |  0%  | [Pending]() |
| VIOL_FILE_UPLOAD  |    |  0%  | [Pending]() |
| VIOL_FILE_UPLOAD_IN_BODY  |    |  0%  | [Pending]() |
| VIOL_GRAPHQL_MALFORMED  |    |  0%  | [Pending]() |
| VIOL_GRAPHQL_FORMAT  |    |  0%  | [Pending]() |
| VIOL_GRAPHQL_INTROSPECTION_QUERY  |    |  0%  | [Pending]() |
| VIOL_GRAPHQL_ERROR_RESPONSE  |    |  0%  | [Pending]() |
| VIOL_GRPC_FORMAT  |    |  0%  | [Pending]() |
| VIOL_GRPC_MALFORMED  |    |  0%  | [Pending]() |
| VIOL_GRPC_METHOD  |    |  0%  | [Pending]() |
| VIOL_JSON_FORMAT  |    |  0%  | [Pending]() |
| VIOL_JSON_MALFORMED  |    |  0%  | [Pending]() |
| VIOL_JSON_SCHEMA  |    |  0%  | [Pending]() |
| VIOL_REQUEST_MAX_LENGTH  |    |  0%  | [Pending]() |
| VIOL_URL_CONTENT_TYPE  |    |  0%  | [Pending]() |
| VIOL_XML_FORMAT  |    |  0%  | [Pending]() |
| VIOL_XML_MALFORMED  |    |  0%  | [Pending]() |




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
