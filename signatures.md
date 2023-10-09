# Signatures module

The **`signatures`** ansible module helps disable/enable signatures either globally or on a specific entity. The entities supported by NAP are `urls / headers / parameters / cookies`.

Below you can find the input/outout parameters for the module

Input:
- **policy_path** (location of policy file)
- **signature_id** (signature ID that you want to disable/enable)
- **format** (json or yaml)
- **enabled** (**True** or **False**. Defaults to True)
- **entity_type** (urls/headers/parameters/cookies) **optional**
- **entity** (the name of the entity you want to configure the signature override) **optional**

Output
- **policy** (the output of the policy)
- **msg** (Message from the module)
- **changed** (if there was a change in the configuration)


## Examples of using the module on a playbook

### Disable a signature globaly
  Input policy `app1_waf.yaml`
  
  ```yml
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

  Ansible Playbook using the `signatures` module.
  ```yml
  - name: Attack signatures
    hosts: localhost
    tasks:
      - name: Disable Signature globaly
        signatures:
          signature_id: 200001834
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

  Modified policy.
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
      signatures:                     ### Changes added by ansible module
      - enabled: false                ### Changes added by ansible module
        signatureId: 200001834        ### Changes added by ansible module
      template:
        name: POLICY_TEMPLATE_NGINX_BASE
  ```


1. Disable a signature on a URL entity
  ```yaml
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
