#!/usr/bin/python3
import json
import yaml

from ansible.module_utils.basic import AnsibleModule

# Function to handle enabling/disabling of evasion techniques
def evasion_technique(policy_json, name, enabled):
    if "blocking-settings" in policy_json["policy"] and isinstance(policy_json["policy"]["blocking-settings"], list):
        # Check if 'evasions' key exists under 'blocking-settings'
        if "evasions" in policy_json["policy"]["blocking-settings"]:
            # Check if the evasion technique already exists
            exists, x = key_exists(policy_json["policy"]["blocking-settings"]["evasions"], "description", name)
            if exists:
                # If the evasion technique exists, update its 'enabled' status if needed
                if policy_json["policy"]["blocking-settings"]["evasions"][x].get("enabled") == enabled:
                    return policy_json, False, f"No Change! Evasion technique sub-violation '{name}' already set to {'enabled' if enabled else 'disabled'}"
                else:
                    policy_json["policy"]["blocking-settings"]["evasions"][x]["enabled"] = enabled
            else:
                # If the evasion technique doesn't exist, add it with the provided 'enabled' status
                policy_json["policy"]["blocking-settings"]["evasions"].append({"description": name, "enabled": enabled})
        else:
            # If 'evasions' key doesn't exist, create it and add the evasion technique with the provided 'enabled' status
            policy_json["policy"]["blocking-settings"]["evasions"] = [{"description": name, "enabled": enabled}]
    else:
        # If 'blocking-settings' key doesn't exist, create it along with 'evasions' and add the evasion technique
        policy_json["policy"]["blocking-settings"] = {"evasions": [{"description": name, "enabled": enabled}]}

    return policy_json, True, f"Success! Evasion technique sub-violation '{name}' set to {'enabled' if enabled else 'disabled'}"

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
            evasion=dict(type='str', required=True),
            format=dict(type='str', required=True),
            enabled=dict(type='bool', required=False, default=False)
        )
    )

    # Retrieve input parameters from Ansible
    policy_path = module.params['policy_path']
    enabled = module.params['enabled']
    evasion = module.params['evasion']
    format = module.params['format'].lower()

    # Define allowed evasion techniques
    allowed_values = ["%u decoding", "Apache whitespace", "Bad unescape", "Bare byte decoding", "Directory traversals",
                      "IIS backslashes", "IIS Unicode codepoints", "Multiple decoding"]

    # Validate the provided evasion technique
    if evasion not in allowed_values:
        module.fail_json(msg=f"'{evasion}' is not a valid evasion technique. Allowed values: {allowed_values}")

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

    # Update policy data with the new evasion technique configuration
    updated_policy_data, is_changed, message = evasion_technique(policy_data, evasion, enabled)

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
