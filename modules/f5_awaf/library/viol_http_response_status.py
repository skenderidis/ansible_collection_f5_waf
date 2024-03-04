#!/usr/bin/python3
import json
import yaml

from ansible.module_utils.basic import AnsibleModule

#####  VIOL_COOKIE_LENGTH ######

def status_code(policy_json, code):

    # Default list of HTTP response codes
    default = [400, 401, 404, 407, 417, 503]

    # Check if the code is not in the default list, add it to the list
    if code not in default:
        default.append(code)

    # Check if the 'general' key exists in the policy JSON
    if "general" in policy_json["policy"]:
        # Check if 'allowedResponseCodes' key exists under 'general'
        if "allowedResponseCodes" in policy_json["policy"]["general"]:
            # Check if the specified HTTP response code already exists
            exists, x = value_exists(policy_json["policy"]["general"]["allowedResponseCodes"], code)
            if not exists:
                # If the HTTP response code does not exist, add it to the list
                policy_json["policy"]["general"]["allowedResponseCodes"].append(code)
            else:
                # If the HTTP response code is already configured, return with an error message
                return policy_json, False, f"No Change! HTTP Response Code: {code} already configured"
        else:
            # If 'allowedResponseCodes' key does not exist, create it with the default list
            policy_json["policy"]["general"]["allowedResponseCodes"] = default
    else:
        # If 'general' key does not exist, create it with the default list
        policy_json["policy"]["general"] = {"allowedResponseCodes": default}

    # Return the modified policy JSON, indicating a successful adjustment
    return policy_json, True, f"Success! HTTP Response Code: {code} is configured"


# Function to check if a key-value pair exists in a list of dictionaries
def value_exists(mod_json, value):
    exists = False
    for i, item in enumerate(mod_json):
        if item == value:
            exists = True
            break
    return exists, i if exists else None


def main():
    module = AnsibleModule(
        argument_spec=dict(
            policy_path=dict(type='str', required=True),
            code=dict(type='int', required=True),
            format=dict(type='str', required=True),
        )
    )

    policy_path = module.params['policy_path']
    code = module.params['code']
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


    updated_policy_data, is_changed, message = status_code(policy_data, code)

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