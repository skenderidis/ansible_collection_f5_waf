# Signatures module

The **`signatures`** module has been created to assist with the false-positive of the `VIOL_ATTACK_SIGNATURE` violations. It can disable/enable signatures either globally or on a specific entity. The supported entities as per the NGINX App Protect configuration are the following: 
1. `urls`
2. `headers`
3. `parameters`
4. `cookies`


Below you can find the input/outout parameters for the module

Input:
- **policy_path** (location of policy file)
- **signature_id** (signature ID that you want to disable/enable)
- **format** (*json* or *yaml*)
- **enabled** (*True* or *False*. Defaults to False)
- **entity_type** (**Optional** - Signature can be disabled on `urls`, `headers`, `parameters`, `cookies`) 
- **entity** (**Optional** - The name of the entity you want to configure the signature override) 

Output
- **policy** (Policy output)
- **msg** (Message from the module)
- **changed** (True/False)


> Note: By using this module the policy file will be updated with the new configuration.

## Examples of using the module on a playbook

### Disable a signature globally
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

  Playbook to disable signature globally.
  ```yaml
  - name: Attack signatures
    hosts: localhost
    tasks:
      - name: Disable signature globaly
        signatures:
          signature_id: 200001834
          enabled: False
          policy_path: "app1_waf.yaml"
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
      enforcementMode: blocking
      name: app1_waf
      signatures:                     ### Changes added by ansible module
      - enabled: false                ### Changes added by ansible module
        signatureId: 200001834        ### Changes added by ansible module
      template:
        name: POLICY_TEMPLATE_NGINX_BASE
  ```


### Disable a signature on a URL
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


  Playbook to disable signature on URL.
  ```yaml
  - name: Attack signatures
    hosts: localhost
    tasks:
      - name: Disable signature on a URL
        signatures:
          signature_id: 200001834
          enabled: False
          entity_type: urls
          entity: /index.php          
          policy_path: "app1_waf.yaml"
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
      enforcementMode: blocking
      name: app1_waf
      template:
        name: POLICY_TEMPLATE_NGINX_BASE
      urls:                               ### Changes added by ansible module
      - name: /index.php                  ### Changes added by ansible module
        signatureOverrides:               ### Changes added by ansible module
        - enabled: false                  ### Changes added by ansible module
          signatureId: 200001834          ### Changes added by ansible module
  ```


### Disable a signature on a parameter
  Input policy `app1_waf.yaml`.
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

  Playbook to disable signature on Parameter.
  ```yaml
  - name: Attack signatures
    hosts: localhost
    tasks:
      - name: Disable signature on Parameter
        signatures:
          signature_id: 200001834
          enabled: False
          entity_type: parameters
          entity: users          
          policy_path: "app1_waf.yaml"
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
      enforcementMode: blocking
      name: app1_waf
      parameters:                         ### Changes added by ansible module
      - name: users                       ### Changes added by ansible module
        signatureOverrides:               ### Changes added by ansible module
        - enabled: false                  ### Changes added by ansible module
          signatureId: 200001834          ### Changes added by ansible module
      template:
        name: POLICY_TEMPLATE_NGINX_BASE
  ```
