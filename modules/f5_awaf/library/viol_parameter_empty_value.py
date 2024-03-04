#!/usr/bin/python3
import json
import yaml

from ansible.module_utils.basic import AnsibleModule

# Function that configures the 'empty' setting for a parameter in the security policy JSON
def parameter_empty(policy_json, name, enabled):
    # Check if "parameters" key exists in the policy
    if "parameters" in policy_json["policy"] and isinstance(policy_json["policy"]["parameters"], list):
        # Check if the parameter with the given name already exists
        parameter_exists, x = key_exists(policy_json["policy"]["parameters"], "name", name)
        if parameter_exists:
            # If parameter exists, check if 'allowEmptyValue' is already set to the provided value
            if policy_json["policy"]["parameters"][x].get("allowEmptyValue") == enabled:
                return policy_json, False, f"Failed! 'Allow empty values' for parameter '{name}' is already set to {'enabled' if enabled else 'disabled'}"
            else:
                # If not set to the provided value, update it
                policy_json["policy"]["parameters"][x]["allowEmptyValue"] = enabled
        else:
            # If parameter doesn't exist, add it with the provided 'allowEmptyValue'
            policy_json["policy"]["parameters"].append({"name": name, "allowEmptyValue": enabled})
    else:
        # If "parameters" key doesn't exist, create it and add the parameter with provided 'allowEmptyValue'
        policy_json["policy"]["parameters"] = [{"name": name, "allowEmptyValue": enabled}]
    
    return policy_json, True, f"Success! 'Allow empty values' for parameter '{name}' has been set to {'enabled' if enabled else 'disabled'}"

# Function to check if a key-value pair exists in a list of dictionaries
def key_exists(mod_json, key, value):
    for index, item in enumerate(mod_json):
        if key in item and item[key] == value:
            return True, index
    return False, None

# Main function to execute the Ansible module
def main():
    module = AnsibleModule(
        argument_spec=dict(
            policy_path=dict(type='str', required=True),
            parameter_name=dict(type='str', required=True),
            format=dict(type='str', required=True),
            enabled=dict(type='bool', required=False, default=True)
        )
    )

    # Retrieve parameters from Ansible input
    policy_path = module.params['policy_path']
    enabled = module.params['enabled']
    name = module.params['parameter_name']
    format = module.params['format'].lower()
    
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


    # Update policy data with the new parameter 'allowEmptyValue' configuration
    updated_policy_data, is_changed, message = parameter_empty(policy_data, name, enabled)

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
