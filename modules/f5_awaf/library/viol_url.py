#!/usr/bin/python3
import json
import yaml

from ansible.module_utils.basic import AnsibleModule

# Function to adjust url illegal url violations
def illegal_url(policy_json, name, enabled):
    # Check if the 'urls' key exists in the policy JSON
    if "urls" in policy_json["policy"] and isinstance(policy_json["policy"]["urls"], list):
        # Check if the specified URL exists in the 'urls' list
        url_exists, x = key_exists(policy_json["policy"]["urls"], "name", name)
        if url_exists:
            # If the URL exists, handle cases based on existing settings
            if policy_json["policy"]["urls"][x].get("$action") == "delete" and enabled==True:
                # If the URL has "$action=delete", remove it and set the 'allowed' status
                del policy_json["policy"]["urls"][x]["$action"]
                policy_json["policy"]["urls"][x]["allowed"] = enabled
                return policy_json, True, f"Success! URL '{name}' allowed by removing the '$action=delete' "
            if policy_json["policy"]["urls"][x].get("allowed") == enabled:
                return policy_json, False, f"No Change! URL '{name}' is already set to {'enabled' if enabled else 'disabled'}"
            else:
                # Update the 'allowed' status of the URL
                policy_json["policy"]["urls"][x]["allowed"] = enabled
        else:
            # If the URL does not exist, add it to the 'urls' list with the specified status
            policy_json["policy"]["urls"].append({"name": name, "allowed": enabled})
    else:
        # If 'urls' key does not exist, create it and add the specified URL with the status
        policy_json["policy"]["urls"] = [{"name": name, "allowed": enabled}]

    # Return the modified policy JSON, indicating a successful adjustment
    return policy_json, True, f"Success! URL '{name}' set to {'enabled' if enabled else 'disabled'}"

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
            url=dict(type='str', required=True),
            format=dict(type='str', required=True),
            enabled=dict(type='bool', required=False, default=False)
        )
    )

    policy_path = module.params['policy_path']
    enabled = module.params['enabled']
    url = module.params['url']
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

    # Update policy data with the new parameter data type configuration
    updated_policy_data, is_changed, message = illegal_url(policy_data, url, enabled)

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