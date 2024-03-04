#!/usr/bin/python3
import json
import yaml

from ansible.module_utils.basic import AnsibleModule

# Function that configures the allowed HTTP Methods in the security policy
def http_method(policy_json, method):
    # Check if the 'methods' key exists in the policy JSON
    if "methods" in policy_json["policy"] and isinstance(policy_json["policy"]["methods"], list):
        # Check if the specified method exists in the 'methods' list
        method_exists, x = key_exists(policy_json["policy"]["methods"], "name", method)
        if method_exists:
            # If the method exists, remove any potential '$action' attribute
            if policy_json["policy"]["methods"][x].get("$action") == "delete":
                del policy_json["policy"]["methods"][x]["$action"]
                return policy_json, True, f"Success! Method '{method}' allowed by removing '$action=delete'"
            else:
                # If the method is already configured, return with an error message
                return policy_json, False, f"Failed! Method '{method}' is already configured"
        else:
            # If the method does not exist, add it to the 'methods' list
            policy_json["policy"]["methods"].append({"name": method})
    else:
        # If 'methods' key does not exist, create it and add the specified method
        policy_json["policy"]["methods"] = [{"name": method}]

    # Return the modified policy JSON, indicating a successful configuration
    return policy_json, True, f"Success! Method '{method}' added to the allowed list"

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
            method=dict(type='str', required=True),
            format=dict(type='str', required=True)
        )
    )

    policy_path = module.params['policy_path']
    method = module.params['method']
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

   
    updated_policy_data, is_changed, message = http_method(policy_data, method)

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