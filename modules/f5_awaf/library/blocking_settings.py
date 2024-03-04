#!/usr/bin/python3
import json
import yaml

from ansible.module_utils.basic import AnsibleModule

def blocking_settings(policy_json, viol_name, block, alarm):
    # Check if the 'blocking-settings' key exists in the policy JSON
    if "blocking-settings" in policy_json["policy"] and isinstance(policy_json["policy"]["blocking-settings"], list):
        # Check if the 'violations' key exists in the 'blocking-settings' section
        if "violations" in policy_json["policy"]["blocking-settings"] and isinstance(policy_json["policy"]["blocking-settings"]["violations"], list):
            # Check if the specified violation already exists
            exists, x = key_exists(policy_json["policy"]["blocking-settings"]["violations"], "name", viol_name)
            if exists:
                # If the violation exists and has the same settings, return with an error message
                if policy_json["policy"]["blocking-settings"]["violations"][x].get("block") == block and \
                        policy_json["policy"]["blocking-settings"]["violations"][x].get("alarm") == alarm:
                    return policy_json, False, f"No Change! Blocking settings for '{viol_name}' already set to block ({block}) and alarm ({alarm})"
                else:
                    # Modify the violation settings
                    policy_json["policy"]["blocking-settings"]["violations"][x]["block"] = block
                    policy_json["policy"]["blocking-settings"]["violations"][x]["alarm"] = alarm
                    return policy_json, True, f"Success! Blocking settings modified for '{viol_name}' to block ({block}) and alarm ({alarm})"
            else:
                # If the violation does not exist, add it to the 'violations' list
                policy_json["policy"]["blocking-settings"]["violations"].append({
                    "name": viol_name,
                    "block": block,
                    "alarm": alarm
                })
        else:
            # If the 'violations' key does not exist, create it and add the specified violation
            policy_json["policy"]["blocking-settings"]["violations"] = [{
                "name": viol_name,
                "block": block,
                "alarm": alarm
            }]
    else:
        # If 'blocking-settings' key does not exist, create it and add the specified violation
        policy_json["policy"]["blocking-settings"] = {
            "violations": [{
                "name": viol_name,
                "block": block,
                "alarm": alarm
            }]
        }

    # Return the modified policy JSON, indicating a successful configuration
    return policy_json, True, f"Success! Blocking settings modified for '{viol_name}' to block ({block}) and alarm ({alarm})"

# Function to check if a key-value pair exists in a list of dictionaries
def key_exists(mod_json, key, value):
    for index, item in enumerate(mod_json):
        # Check if the item has the key and its value matches
        if key in item and item[key] == value:
            return True, index
    return False, None

def main():
    module = AnsibleModule(
        argument_spec=dict(
            policy_path=dict(type='str', required=True),
            violation=dict(type='str', required=True),
            alarm=dict(type='bool', required=False, default=False),
            block=dict(type='bool', required=False, default=False),
            format=dict(type='str', required=True)
        )
    )

    # Put ansible inputs as python variables 
    policy_path = module.params['policy_path']
    alarm = module.params['alarm']
    block = module.params['block']
    format = module.params['format'].lower()
    viol_name = module.params['violation']

    # Define allowed violations

    allowed_values = ["VIOL_ASM_COOKIE_MODIFIED", "VIOL_ATTACK_SIGNATURE", "VIOL_BLACKLISTED_IP", "VIOL_BOT_CLIENT", "VIOL_COOKIE_EXPIRED", "VIOL_COOKIE_LENGTH", "VIOL_COOKIE_MALFORMED", "VIOL_COOKIE_MODIFIED", "VIOL_DATA_GUARD", "VIOL_ENCODING", "VIOL_EVASION", "VIOL_FILETYPE", "VIOL_FILE_UPLOAD", "VIOL_FILE_UPLOAD_IN_BODY", "VIOL_GRAPHQL_MALFORMED", "VIOL_GRAPHQL_FORMAT", "VIOL_GRAPHQL_INTROSPECTION_QUERY", "VIOL_GRAPHQL_ERROR_RESPONSE", "VIOL_GRPC_FORMAT", "VIOL_GRPC_MALFORMED", "VIOL_GRPC_METHOD", "VIOL_HEADER_LENGTH", "VIOL_HEADER_METACHAR", "VIOL_HTTP_PROTOCOL", "VIOL_HTTP_RESPONSE_STATUS", "VIOL_JSON_FORMAT", "VIOL_JSON_MALFORMED", "VIOL_JSON_SCHEMA", "VIOL_MANDATORY_PARAMETER", "VIOL_MANDATORY_REQUEST_BODY", "VIOL_METHOD", "VIOL_PARAMETER", "VIOL_PARAMETER_ARRAY_VALUE", "VIOL_PARAMETER_DATA_TYPE", "VIOL_PARAMETER_EMPTY_VALUE", "VIOL_PARAMETER_LOCATION", "VIOL_PARAMETER_MULTIPART_NULL_VALUE", "VIOL_PARAMETER_NAME_METACHAR", "VIOL_PARAMETER_NUMERIC_VALUE", "VIOL_PARAMETER_REPEATED", "VIOL_PARAMETER_STATIC_VALUE", "VIOL_PARAMETER_VALUE_BASE64", "VIOL_PARAMETER_VALUE_LENGTH", "VIOL_PARAMETER_VALUE_METACHAR", "VIOL_PARAMETER_VALUE_REGEXP", "VIOL_POST_DATA_LENGTH", "VIOL_QUERY_STRING_LENGTH", "VIOL_RATING_THREAT", "VIOL_RATING_NEED_EXAMINATION", "VIOL_REQUEST_LENGTH", "VIOL_REQUEST_MAX_LENGTH", "VIOL_THREAT_CAMPAIGN", "VIOL_URL", "VIOL_URL_CONTENT_TYPE", "VIOL_URL_LENGTH", "VIOL_URL_METACHAR", "VIOL_XML_FORMAT", "VIOL_XML_MALFORMED"]

    if viol_name not in allowed_values:
      module.fail_json(msg=f"'{viol_name}' is  not a valid value for the 'viol_name' variable. It can be any of the following: {list(allowed_values)}.")

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

    updated_policy_data, is_changed, message = blocking_settings(policy_data, viol_name,block,alarm)

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
