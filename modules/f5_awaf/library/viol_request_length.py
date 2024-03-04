#!/usr/bin/python3
import json
import yaml

from ansible.module_utils.basic import AnsibleModule

# Function to adjust the request length constraint in the security policy JSON
def request_length(policy_json, name, length):
    # Check if the 'filetypes' key exists in the policy JSON
    if "filetypes" in policy_json["policy"] and isinstance(policy_json["policy"]["filetypes"], list):
        # Check if the request length constraint already exists for the specified name
        filetype_exists, x = key_exists(policy_json["policy"]["filetypes"], "name", name)
        if filetype_exists:
            # If the constraint exists and has the same request length, return no change
            if policy_json["policy"]["filetypes"][x].get("requestLength") == length:
                return policy_json, False, f"No Change! Request Length already configured"
            else:
                # Update the request length and ensure 'checkRequestLength' is set to True
                policy_json["policy"]["filetypes"][x]["requestLength"] = length
                if not "checkRequestLength" in policy_json["policy"]["filetypes"][x]:
                    policy_json["policy"]["filetypes"][x]["checkRequestLength"] = True
        else:
            # If the constraint doesn't exist, add it with the specified request length and 'checkRequestLength' set to True
            policy_json["policy"]["filetypes"].append({"name": name, "requestLength": length, "checkRequestLength": True})
    else:
        # If 'filetypes' key doesn't exist, create it and add the request length constraint
        policy_json["policy"]["filetypes"] = [{"name": name, "requestLength": length, "checkRequestLength": True}]
    
    # Return the modified policy JSON, along with a success message
    return policy_json, True, f"Success! Request Length adjusted to {length}"

# Function to check if a key-value pair exists in a list of dictionaries
def key_exists(mod_json, key, value):
    for index, item in enumerate(mod_json):
        if key in item and item[key] == value:
            return True, index
    return False, None


def main():
    # Define the expected arguments for the Ansible module
    module = AnsibleModule(
        argument_spec=dict(
            policy_path=dict(type='str', required=True),
            filetype=dict(type='str', required=True),
            format=dict(type='str', required=True),
            length=dict(type='int', required=True)
        )
    )

    # Retrieve parameters from the module input
    policy_path = module.params['policy_path']
    filetype = module.params['filetype']
    format = module.params['format'].lower()
    length = module.params['length']
    

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


    # Adjust the Request length in the policy JSON
    updated_policy_data, is_changed, message = request_length(policy_data, filetype, length)

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
