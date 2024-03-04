#!/usr/bin/python3
import json
import yaml

from ansible.module_utils.basic import AnsibleModule

# Function to adjust the allowed status of a file type in the security policy JSON.
def illegal_filetype(policy_json, name, enabled):
    # Check if the 'filetypes' key exists in the policy JSON
    if "filetypes" in policy_json["policy"] and isinstance(policy_json["policy"]["filetypes"], list):
        # Check if the specified file type exists in the 'filetypes' list
        filetype_exists, x = key_exists(policy_json["policy"]["filetypes"], "name", name)
        if filetype_exists:
            # If the file type is already allowed, return with an error message
            if policy_json["policy"]["filetypes"][x].get("allowed") == enabled:
                return policy_json, False, f"Failed! File Type {name} already set to {'allowed' if enabled else 'disallowed'}"
            else:
                # Update the allowed status of the file type
                policy_json["policy"]["filetypes"][x]["allowed"] = enabled
        else:
            # If the file type does not exist, add it to the 'filetypes' list with the specified allowed status
            policy_json["policy"]["filetypes"].append({"name": name, "allowed": enabled})
    else:
        # If 'filetypes' key does not exist, create it and add the specified file type with the allowed status
        policy_json["policy"]["filetypes"] = [{"name": name, "allowed": enabled}]
    
    # Return the modified policy JSON, indicating a successful adjustment
    return policy_json, True, f"Success! File Type {name} set to {'allowed' if enabled else 'disallowed'}"


# Function to check if a key-value pair exists in a list of dictionaries
def key_exists(mod_json, key, value):
    exists = False
    for i, item in enumerate(mod_json):
        if key in item and item[key] == value:
            exists = True
            break
    return (exists, i if exists else None)

def main():
    # Define the expected arguments for the Ansible module
    module = AnsibleModule(
        argument_spec=dict(
            policy_path=dict(type='str', required=True),
            filetype=dict(type='str', required=True),
            format=dict(type='str', required=True),
            enabled=dict(type='bool', required=False, default=True)
        )
    )
    # Retrieve parameters from the module input
    policy_path = module.params['policy_path']
    enabled = module.params['enabled']
    filetype = module.params['filetype']
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

    # Update policy data with the new evasion technique configuration
    updated_policy_data, is_changed, message = illegal_filetype(policy_data, filetype, enabled)

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