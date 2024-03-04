#!/usr/bin/python3
import json
import yaml

from ansible.module_utils.basic import AnsibleModule


#####  VIOL_THREAT_CAMPAIGNS
def threat_campaigns(policy_json, name, enabled):
    if "threat-campaigns" in policy_json["policy"] and isinstance(policy_json["policy"]["threat-campaigns"], list):
        # Check if the threat campaign already exists
        exists, x = key_exists(policy_json["policy"]["threat-campaigns"], "name", name)
        if exists:
            # Check if the current enabled status matches the provided enabled status
            if policy_json["policy"]["threat-campaigns"][x]["isEnabled"] == enabled:
                return policy_json, False, f"Failed! Threat Campaign {name} is already {'enabled' if enabled else 'disabled'}"
            else:
                # Update the enabled status of the threat campaign
                policy_json["policy"]["threat-campaigns"][x]["isEnabled"] = enabled
        else:
            # Add the threat campaign with the provided enabled status
            policy_json["policy"]["threat-campaigns"].append({
                "name": name,
                "isEnabled": enabled
            })
    else:
        # If 'threat-campaigns' key does not exist, create it and add the threat campaign with the provided enabled status
        policy_json["policy"]["threat-campaigns"] = [{
            "name": name,
            "isEnabled": enabled
        }]

    # Return the modified policy JSON, indicating a successful configuration
    return policy_json, True, f"Success! Threat Campaign {name} {'enabled' if enabled else 'disabled'}"

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
            format=dict(type='str', required=True),
            name=dict(type='str', required=True),
            enabled=dict(type='bool', required=False, default=False)
        )
    )
    # Put ansible inputs as python variables 
    policy_path = module.params['policy_path']
    enabled = module.params['enabled']
    format = module.params['format'].lower()
    name = module.params['name']

    
    # Read the policy file 
    try:
        with open(policy_path, 'r') as file:
            policy_content = file.read()
    except Exception as e:
        module.fail_json(msg=f"Failed to read file: {str(e)}")

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

    updated_policy_data, is_changed, message = threat_campaigns(policy_data, name, enabled)


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