# blocking_settings Module

The **`blocking_settings`** module has been created to change the `Alarm` and `Block` configuration for the Blocking Setting on the NGINX App Protect or F5 AWAF declarative waf policy. The list of allowed violations are:

1. VIOL_ASM_COOKIE_MODIFIED
1. VIOL_ATTACK_SIGNATURE
1. VIOL_BLACKLISTED_IP
1. VIOL_BOT_CLIENT
1. VIOL_COOKIE_EXPIRED
1. VIOL_COOKIE_LENGTH
1. VIOL_COOKIE_MALFORMED
1. VIOL_COOKIE_MODIFIED
1. VIOL_DATA_GUARD
1. VIOL_ENCODING
1. VIOL_EVASION
1. VIOL_FILETYPE
1. VIOL_FILE_UPLOAD
1. VIOL_FILE_UPLOAD_IN_BODY
1. VIOL_GRAPHQL_MALFORMED
1. VIOL_GRAPHQL_FORMAT
1. VIOL_GRAPHQL_INTROSPECTION_QUERY
1. VIOL_GRAPHQL_ERROR_RESPONSE
1. VIOL_GRPC_MALFORMED
1. VIOL_GRPC_FORMAT
1. VIOL_GRPC_METHOD
1. VIOL_HEADER_LENGTH
1. VIOL_HEADER_METACHAR
1. VIOL_HTTP_PROTOCOL
1. VIOL_HTTP_RESPONSE_STATUS
1. VIOL_JSON_FORMAT
1. VIOL_JSON_MALFORMED
1. VIOL_JSON_SCHEMA
1. VIOL_MANDATORY_PARAMETER
1. VIOL_MANDATORY_REQUEST_BODY
1. VIOL_METHOD
1. VIOL_PARAMETER
1. VIOL_PARAMETER_ARRAY_VALUE
1. VIOL_PARAMETER_DATA_TYPE
1. VIOL_PARAMETER_EMPTY_VALUE
1. VIOL_PARAMETER_LOCATION
1. VIOL_PARAMETER_MULTIPART_NULL_VALUE
1. VIOL_PARAMETER_NAME_METACHAR
1. VIOL_PARAMETER_NUMERIC_VALUE
1. VIOL_PARAMETER_REPEATED
1. VIOL_PARAMETER_STATIC_VALUE
1. VIOL_PARAMETER_VALUE_BASE64
1. VIOL_PARAMETER_VALUE_LENGTH
1. VIOL_PARAMETER_VALUE_METACHAR
1. VIOL_PARAMETER_VALUE_REGEXP
1. VIOL_POST_DATA_LENGTH
1. VIOL_QUERY_STRING_LENGTH
1. VIOL_RATING_THREAT
1. VIOL_RATING_NEED_EXAMINATION
1. VIOL_REQUEST_LENGTH
1. VIOL_REQUEST_MAX_LENGTH
1. VIOL_THREAT_CAMPAIGN
1. VIOL_URL
1. VIOL_URL_CONTENT_TYPE
1. VIOL_URL_LENGTH
1. VIOL_URL_METACHAR
1. VIOL_XML_FORMAT
1. VIOL_XML_MALFORMED


Below you can find the input/outout parameters for the module

**Input**:
- **policy_path** (location of policy file)
- **alarm** (*True* or *False*)
- **block** (*True* or *False*)
- **viol_name** (The name of the Violation you want to modify)
- **format** (*json* or *yaml*)

**Output**
- **policy** (Policy output)
- **msg** (Message from the module)
- **changed** (True/False)

> By using this module the policy file will be updated with the new configuration.

> It's important to note that only specific key/value pairs within the JSON files are modified, while other aspects of the policy remain unchanged.

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

2. Run the Ansible playbook to modify the blocking settings of a specific violation
    ```yaml
    - name: Modify Blocking Settings
      hosts: localhost
      collections:
        - skenderidis.f5_awaf   
      tasks:
        - name: Modify Blocking Settings
          blocking_settings:
            policy_path: waf_policy.yaml
            violation: VIOL_RATING_THREAT
            alarm: true
            block: true
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
          violations:
          - alarm: true
            block: true
            name: VIOL_RATING_THREAT
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

2. Run the Ansible playbook to modify the configured length for HTTP Headers.
    ```yaml
    - name: Modify Blocking Settings
      hosts: localhost
      collections:
        - skenderidis.f5_awaf   
      tasks:
        - name: Modify Blocking Settings
          blocking_settings:
            policy_path: waf_policy.json
            violation: VIOL_RATING_THREAT
            alarm: true
            block: true
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
          "violations": [
            {
              "name": "VIOL_RATING_THREAT",
              "block": true,
              "alarm": true
            }
          ]
        }
      }
    ```
