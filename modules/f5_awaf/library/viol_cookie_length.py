#!/usr/bin/python3
import json
import yaml

from ansible.module_utils.basic import AnsibleModule

def cookie_length(policy_json, length):
    # Limiting the length within a valid range
    length = max(1, min(length, 65536))
    
    # Check if cookie-settings exist in the policy
    if "cookie-settings" in policy_json["policy"]:
        # Check if the maximumCookieHeaderLength is already configured
        if policy_json["policy"]["cookie-settings"].get("maximumCookieHeaderLength") == length:
            return policy_json, False, f"No Change! Cookie length is already set to {length}"
        else:
            policy_json["policy"]["cookie-settings"]["maximumCookieHeaderLength"] = length
    else:
        policy_json["policy"]["cookie-settings"] = {"maximumCookieHeaderLength": length}

    return policy_json, True, f"Success! Cookie length is set to {length} "

def main():
    module = AnsibleModule(
        argument_spec=dict(
            policy_path=dict(type='str', required=True),
            length=dict(type='int', required=True),
            format=dict(type='str', required=True),
            enabled=dict(type='bool', required=False, default=False)
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

    updated_policy_data, is_changed, message = cookie_length(policy_data, length)

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