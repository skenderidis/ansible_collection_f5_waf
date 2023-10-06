# nap-ansible

Violations 

| Violations  | module | Status | | 
| ------------- | ------------- | ------------- | ------------- |
| VIOL_ATTACK_SIGNATURE  | signatures  |  100%  | [Examples](#viol_attack_signature) |
| VIOL_FILETYPE | file_types  |  100%  | [Examples](##VIOL_FILETYPE)| 
| VIOL_POST_DATA_LENGTH | file_length  |  100%  | [Examples](/file_length/) |
| VIOL_QUERY_STRING_LENGTH | file_length  |  100%  | [Examples](/file_length/) |
| VIOL_REQUEST_LENGTH | file_length  |  100%  | [Examples](/file_length/) |
| VIOL_URL_LENGTH | file_length  |  100%  | [Examples](/file_length/) |
| VIOL_HTTP_COMPLIANCE | http_compliance  |  100%  | [Examples](/http_compliance/) |
| VIOL_EVASION | evasion  |  100%  | [Examples](/evasion/) |
| VIOL_PARAMETER_VALUE_BASE64  |    |  0%  | [Pending]() |
| VIOL_MANDATORY_HEADER  |    |  0%  | [Pending]() |
| VIOL_COOKIE_MODIFIED  |    |  0%  | [Pending]() |
| VIOL_THREAT  |    |  0%  | [Pending]() |
| VIOL_URL  |    |  0%  | [Pending]() |
| VIOL_HEADER_LENGTH  |    |  0%  | [Pending]() |
| VIOL_COOKIE_LENGTH  |    |  0%  | [Pending]() |
| VIOL_HEADER_METACHAR  |    |  0%  | [Pending]() |
| VIOL_PARAMETER_NAME_METACHAR  |    |  0%  | [Pending]() |
| VIOL_PARAMETER_VALUE_METACHAR  |    |  0%  | [Pending]() |
| VIOL_URL_METACHAR  |    |  0%  | [Pending]() |
| VIOL_METHOD  |    |  0%  | [Pending]() |
| VIOL_BOT_CLIENT  |    |  0%  | [Pending]() |
| VIOL_HTTP_RESPONSE_STATUS  |    |  0%  | [Pending]() |
|   |    |  0%  | [Pending]() |
|   |    |  0%  | [Pending]() |
|   |    |  0%  | [Pending]() |
|   |    |  0%  | [Pending]() |

VIOL_PARAMETER_VALUE_BASE64

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
