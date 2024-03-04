#!/usr/bin/python3
import json
import yaml

from ansible.module_utils.basic import AnsibleModule

# Function to adjust the maximum HTTP header length in the security policy JSON
def header_length(policy_json, length):
    # Limit the length within the acceptable range
    length = max(1, min(length, 65536))

    # Check if the 'header-settings' key exists in the policy JSON
    if "header-settings" in policy_json["policy"]:
        # If the maximum HTTP header length is already configured, return with an error message
        if policy_json["policy"]["header-settings"].get("maximumHttpHeaderLength") == length:
            return policy_json, False, f"No Change! Header length is already set to {length}"
        else:
            # Update the maximum HTTP header length
            policy_json["policy"]["header-settings"]["maximumHttpHeaderLength"] = length
    else:
        # If 'header-settings' key does not exist, create it with the specified maximum HTTP header length
        policy_json["policy"]["header-settings"] = {"maximumHttpHeaderLength": length}

    # Return the modified policy JSON, indicating a successful adjustment
    return policy_json, True, f"Success! Header length set to {length}"


def main():
    module = AnsibleModule(
        argument_spec=dict(
            policy_path=dict(type='str', required=True),
            length=dict(type='int', required=True),
            format=dict(type='str', required=True)
        )
    )

    policy_path = module.params['policy_path']
    length = module.params['length']
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

   
    updated_policy_data, is_changed, message = header_length(policy_data, length)

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