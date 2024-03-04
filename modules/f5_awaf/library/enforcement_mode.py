#!/usr/bin/python3
import json
import yaml

from ansible.module_utils.basic import AnsibleModule

# Function to configure the enforcementMode in the security policy JSON
def enforcement_mode(policy_json, enforcement):
    # Check if the 'enforcementMode' key exists in the policy JSON
    if "enforcementMode" in policy_json["policy"]:
        # If the maximum enforcementMode is already configured, return with an error message
        if policy_json["policy"]["enforcementMode"] == enforcement:
            return policy_json, False, f"No Change! EnforcementMode is already set to {enforcement}"
        else:
            # Update the enforcementMode
            policy_json["policy"]["enforcementMode"] = enforcement
    else:
        # If 'enforcementMode' key does not exist, create it
        policy_json["policy"]["enforcementMode"] = enforcement

    # Return the modified policy JSON, indicating a successful adjustment
    return policy_json, True, f"Success! EnforcementMode set to {enforcement}"


def main():
    module = AnsibleModule(
        argument_spec=dict(
            policy_path=dict(type='str', required=True),
            enforcement=dict(type='str', required=True),
            format=dict(type='str', required=True)
        )
    )

    # Put ansible inputs as python variables 
    policy_path = module.params['policy_path']
    enforcement = module.params['enforcement']
    format = module.params['format'].lower()

    allowed_values = ["transparent", "blocking"]

    if enforcement not in allowed_values:
      module.fail_json(msg=f"'{enforcement}' is not a valid value for the 'Enforcement' variable. It can be any of the following: {list(allowed_values)}.")

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
   
    updated_policy_data, is_changed, message = enforcement_mode(policy_data, enforcement)

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