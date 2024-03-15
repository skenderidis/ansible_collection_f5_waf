#!/usr/bin/python3
import json
import yaml

from ansible.module_utils.basic import AnsibleModule

# Function to override a signature on a specific entity in the security policy.
def override_signature_on_entity(policy_json, signature_id, location, entity_name, enabled):
    # Check if the specified location exists in the policy JSON
    if location in policy_json["policy"] and isinstance(policy_json["policy"][location], list):
        # Check if the entity exists in the specified location
        entity_exists, x = key_exists(policy_json["policy"][location], "name", entity_name)
        if entity_exists:
            # Check if signature overrides exist for the entity
            if "signatureOverrides" in policy_json["policy"][location][x] and isinstance(policy_json["policy"][location][x]["signatureOverrides"], list):
                # Check if the specified signature ID exists in the entity's signature overrides
                signature_exists, y = key_exists(policy_json["policy"][location][x]["signatureOverrides"], "signatureId", signature_id)
                if signature_exists:
                    # If the signature override settings match the provided settings, return with an error message
                    if policy_json["policy"][location][x]["signatureOverrides"][y].get("enabled") == enabled:
                        return policy_json, False, f"Alert! SignatureID: {signature_id} on entity '{entity_name}' is already set to {'enabled' if enabled else 'disabled'}"
                    else:
                        # Modify the signature override settings
                        policy_json["policy"][location][x]["signatureOverrides"][y]["enabled"] = enabled
                else:
                    # Add the new signature override to the entity's signature overrides
                    policy_json["policy"][location][x]["signatureOverrides"].append({
                        "signatureId": signature_id,
                        "enabled": enabled
                    })
            else:
                # If no signature overrides exist for the entity, create a new list and add the signature override
                policy_json["policy"][location][x]["signatureOverrides"] = [{
                    "signatureId": signature_id,
                    "enabled": enabled
                }]
        else:
            # If the entity does not exist, add it along with the new signature override
            policy_json["policy"][location].append({
                "name": entity_name,
                "signatureOverrides": [{
                    "signatureId": signature_id,
                    "enabled": enabled
                }]
            })
    else:
        # If the specified location does not exist, create it and add the entity along with the new signature override
        policy_json["policy"][location] = [{
            "name": entity_name,
            "signatureOverrides": [{
                "signatureId": signature_id,
                "enabled": enabled
            }]
        }]

    # Return the modified policy JSON, indicating a successful configuration
    return policy_json, True, f"Success! SignatureID: {signature_id} on entity '{entity_name}' set to {'enabled' if enabled else 'disabled'}"

# Function to check if a key-value pair exists in a list of dictionaries
def key_exists(mod_json, key, value):
    for index, item in enumerate(mod_json):
        if key in item and item[key] == value:
            return True, index
    return False, None

def main():
    module = AnsibleModule(
        argument_spec=dict(
            policy_path=dict(type='str', required=True),
            signature_id=dict(type='int', required=True),
            format=dict(type='str', required=True),
            entity_type=dict(type='str', required=True),
            entity=dict(type='str', required=False, default="*"),
            enabled=dict(type='bool', required=False, default=False)
        )
    )
    # Put ansible inputs as python variables 
    policy_path = module.params['policy_path']
    enabled = module.params['enabled']
    sig_id = module.params['signature_id']
    format = module.params['format'].lower()
    entity = module.params['entity']
    entity_type = module.params['entity_type'].lower()

    # Read the policy file 
    try:
        with open(policy_path, 'r') as file:
            policy_content = file.read()
    except Exception as e:
        module.fail_json(msg=f"Failed to read file: {str(e)}")

    if entity == "":
      entity="*"

    # Decode policy content based on format
    try:
        if format == "yaml":
            original_data = yaml.safe_load(policy_content)
            # Removing the Kubernetes key/value pairs
            policy_data = yaml.safe_load(policy_content)["spec"]
        elif format == "json":
            policy_data = json.loads(policy_content)
        else:
            module.fail_json(msg="Unsupported file format. Please provide YAML or JSON.")
    except Exception as e:
        module.fail_json(msg=f"Failed to decode policy content: {str(e)}")

    allowed_values = ["urls", "cookies", "headers", "parameters"]
    if entity_type not in allowed_values :
        module.fail_json(msg=f"'{entity_type}' is  not a valid value for the 'entity_type' variable. It can be any of the following: {list(allowed_values)}.")
        
    updated_policy_data, is_changed, message = override_signature_on_entity(policy_data,sig_id,entity_type,entity,enabled)

    if is_changed:
        # Write back the updated policy
        try:
            with open(policy_path, 'w', encoding='utf-8') as file:
                if format == "yaml":
                    # Adding the updated policy with the original the Kubernetes key/value pairs
                    original_data["spec"]=updated_policy_data
                    policy_data=original_data
                    yaml.dump(policy_data, file, indent=2)
                else:
                    policy_data=updated_policy_data
                    json.dump(updated_policy_data, file, ensure_ascii=False, indent=2)
        except Exception as e:
            module.fail_json(msg=f"Failed to write updated policy: {str(e)}")

    module.exit_json(
        changed=is_changed,
        msg=message,
        policy=policy_data
    )


if __name__ == '__main__':
    main()