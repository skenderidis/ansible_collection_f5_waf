#!/usr/bin/python3
import json
import yaml

from ansible.module_utils.basic import AnsibleModule

# Function to handle viol_parameter_data_type configuration
def parameter_data_type(policy_json, name, value):
    # Check if "parameters" key exists in the policy
    if "parameters" in policy_json["policy"] and isinstance(policy_json["policy"]["parameters"], list):
        # Check if the parameter with the given name already exists
        parameter_exists, x = key_exists(policy_json["policy"]["parameters"], "name", name)
        if parameter_exists:
            # If parameter exists, check if its datatype is already set to the provided value
            if policy_json["policy"]["parameters"][x].get("datatype") == value:
                return policy_json, False, f"No Change! Parameter '{name}' datatype '{value}' is already configured."
            else:
                # If datatype is different, update the datatype
                policy_json["policy"]["parameters"][x]["datatype"] = value
        else:
            # If parameter doesn't exist, add it with the provided datatype
            policy_json["policy"]["parameters"].append({"name": name, "datatype": value})
    else:
        # If "parameters" key doesn't exist, create it and add the parameter with provided datatype
        policy_json["policy"]["parameters"] = [{"name": name, "datatype": value}]
    
    return policy_json, True, f"Success! Parameter '{name}' datatype '{value}' has been configured."

# Function to check if a key-value pair exists in a list of dictionaries
def key_exists(mod_json, key, value):
    for index, item in enumerate(mod_json):
        if key in item and item[key] == value:
            return True, index
    return False, None

# Main function to execute the Ansible module
def main():
    module = AnsibleModule(
        argument_spec=dict(
            policy_path=dict(type='str', required=True),
            parameter_name=dict(type='str', required=True),
            format=dict(type='str', required=True),
            data_type=dict(type='str', required=True)
        )
    )

    # Retrieve parameters from Ansible input
    policy_path = module.params['policy_path']
    data_type = module.params['data_type']
    name = module.params['parameter_name']
    format = module.params['format'].lower()

    # Allowed values for data_type
    allowed_values = ["alpha-numeric", "binary", "phone", "email", "boolean", "integer", "decimal"]

    # Validate data_type against allowed values
    if data_type not in allowed_values:
        module.fail_json(msg=f"'{data_type}' is not a valid value for the 'data_type' variable. It can be any of the following: {', '.join(allowed_values)}.")

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
    updated_policy_data, is_changed, message = parameter_data_type(policy_data, name, data_type)

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
