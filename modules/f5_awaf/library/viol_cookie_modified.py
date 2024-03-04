#!/usr/bin/python3
import json
import yaml

from ansible.module_utils.basic import AnsibleModule

# Function to modify the enforcement type of a cookie in the security policy JSON
def cookie_modified(policy_json, name, enforcementType):
    # Check if the 'cookies' key exists in the policy JSON
    if "cookies" in policy_json["policy"] and isinstance(policy_json["policy"]["cookies"], list):
        # Check if the specified cookie exists in the 'cookies' list
        cookie_exists, x = key_exists(policy_json["policy"]["cookies"], "name", name)
        if cookie_exists:
            # If the enforcement type is already set to the specified value, return with a message indicating no change
            if policy_json["policy"]["cookies"][x].get("enforcementType") == enforcementType:
                return policy_json, False, f"No Change! Cookie '{name}' enforcementType is already set to '{enforcementType}'"
            else:
                # Update the enforcement type of the cookie
                policy_json["policy"]["cookies"][x]["enforcementType"] = enforcementType
        else:
            # If the cookie does not exist, add it to the 'cookies' list with the specified enforcement type
            policy_json["policy"]["cookies"].append(
                json.loads('{"name":"'+name+'","enforcementType":"'+enforcementType+'"}'))
    else:
        # If 'cookies' key does not exist, create it and add the specified cookie with the enforcement type
        policy_json["policy"]["cookies"] = json.loads(
            '[{"name":"'+name+'","enforcementType":"'+enforcementType+'"}]')

    return policy_json, True, f"Success! Cookie '{name}' enforcementType set to '{enforcementType}'"

# Function to check if a key-value pair exists in a list of dictionaries
def key_exists(mod_json, key, value):
    exists = False
    for i, item in enumerate(mod_json):
        if key in item and item[key] == value:
            exists = True
            break
    return (exists, i if exists else None)

def main():
    module = AnsibleModule(
        argument_spec=dict(
            policy_path=dict(type='str', required=True),
            cookie_name=dict(type='str', required=True),
            format=dict(type='str', required=True),
            enforcementType=dict(type='str', required=False, default="allow")
        )
    )

    # Retrieve input parameters from Ansible
    policy_path = module.params['policy_path']
    enforcementType = module.params['enforcementType']
    cookie_name = module.params['cookie_name']
    format = module.params['format'].lower()

    # Define allowed enforcementType
    allowed_values = ["enforce", "allow"]
    if enforcementType not in allowed_values :
        module.fail_json(msg=f"'{enforcementType}' is not a valid value for the 'enforcementType' variable. It can be any of the following: {list(allowed_values)}.")

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

    updated_policy_data, is_changed, message = cookie_modified(policy_data, cookie_name, enforcementType)

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
