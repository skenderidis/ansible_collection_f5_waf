#!/usr/bin/python3
import json
import yaml

from ansible.module_utils.basic import AnsibleModule


# Function that configures the 'mandatory' setting for a parameter in the security policy JSON
def mandatory_parameter (policy_json, name, enabled):
    # Check if the 'parameters' key exists in the policy JSON
    if "parameters" in policy_json["policy"] and isinstance(policy_json["policy"]["parameters"], list):
        # Check if the specified parameter exists in the 'parameters' list
        parameter_exists, x = key_exists(policy_json["policy"]["parameters"], "name", name)
        if parameter_exists:
            # If the parameter exists, update its 'mandatory' setting
            if policy_json["policy"]["parameters"][x].get("mandatory") == enabled:
                # If the parameter is already configured with the specified status, return with an error message
                return policy_json, False, f"Failed! Parameter '{name}' mandatory setting is already {'enabled' if enabled else 'disabled'}"
            else:
                # Update the 'mandatory' setting of the parameter
                policy_json["policy"]["parameters"][x]["mandatory"] = enabled
        else:
            # If the parameter does not exist, add it to the 'parameters' list with the specified setting
            policy_json["policy"]["parameters"].append({"name": name, "mandatory": enabled})
    else:
        # If 'parameters' key does not exist, create it and add the specified parameter with the setting
        policy_json["policy"]["parameters"] = [{"name": name, "mandatory": enabled}]

    # Return the modified policy JSON, indicating a successful configuration
    return policy_json, True, f"Success! Parameter '{name}' mandatory setting has been configured to {'enabled' if enabled else 'disabled'}"


def key_exists(mod_json, key, value):
  x = 0
  exists = False
  for i in mod_json:
    if key in i:
      if i[key] == value:
        exists = True
        break;
    x = x + 1
  return (exists, x)

def main():
    module = AnsibleModule(
        argument_spec=dict(
            policy_path=dict(type='str', required=True),
            parameter_name=dict(type='str', required=True),
            format=dict(type='str', required=True),
            enabled=dict(type='bool', required=False, default=False)
        )
    )

    policy_path = module.params['policy_path']
    enabled = module.params['enabled']
    parameter_name = module.params['parameter_name']
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

    updated_policy_data, is_changed, message = mandatory_parameter(policy_data, parameter_name, enabled)

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