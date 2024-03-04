#!/usr/bin/python3
import json
import yaml

from ansible.module_utils.basic import AnsibleModule

# Function to handle enabling/disabling HTTP protocol compliance
def http_compliance(policy_json, name, enabled):
    # Check if the 'blocking-settings' key exists in the policy JSON
    if "blocking-settings" in policy_json["policy"] and isinstance(policy_json["policy"]["blocking-settings"], list):
        # Check if 'http-protocols' key exists under 'blocking-settings'
        if "http-protocols" in policy_json["policy"]["blocking-settings"]:
            # Check if the specified HTTP protocol exists in the 'http-protocols' list
            exists, x = key_exists(policy_json["policy"]["blocking-settings"]["http-protocols"], "description", name)
            if exists:
                # If the HTTP protocol compliance status is already as desired, return with an error message
                if policy_json["policy"]["blocking-settings"]["http-protocols"][x].get("enabled") == enabled:
                    return policy_json, False, f"No Change! HTTP Protocol compliance sub-violation '{name}' already set to {'enabled' if enabled else 'disabled'}"
                else:
                    # Update the HTTP protocol compliance status
                    policy_json["policy"]["blocking-settings"]["http-protocols"][x]["enabled"] = enabled
            else:
                # If the HTTP protocol does not exist, add it to the 'http-protocols' list with the specified status
                policy_json["policy"]["blocking-settings"]["http-protocols"].append(
                    {"description": name, "enabled": enabled}
                )
        else:
            # If 'http-protocols' key does not exist, create it and add the specified HTTP protocol with the status
            policy_json["policy"]["blocking-settings"]["http-protocols"] = [{"description": name, "enabled": enabled}]
    else:
        # If 'blocking-settings' key does not exist, create it with the specified HTTP protocol and status
        policy_json["policy"]["blocking-settings"] = {"http-protocols": [{"description": name, "enabled": enabled}]}

    # Return the modified policy JSON, indicating a successful adjustment
    return policy_json, True, f"Success! HTTP Protocol compliance sub-violation '{name}' set to {'enabled' if enabled else 'disabled'}"


# Function to check if a key-value pair exists in a list of dictionaries
def key_exists(mod_json, key, value):
    exists = False
    for i, item in enumerate(mod_json):
        if key in item and item[key] == value:
            exists = True
            break
    return exists, i if exists else None

def main():
    module = AnsibleModule(
        argument_spec=dict(
            policy_path=dict(type='str', required=True),
            http_protocol=dict(type='str', required=True),
            format=dict(type='str', required=True),
            enabled=dict(type='bool', required=False, default=False)
        )
    )

    policy_path = module.params['policy_path']
    enabled = module.params['enabled']
    http_protocol = module.params['http_protocol']
    format = module.params['format'].lower()

    allowed_values = ["Unparsable request content", "Several Content-Length headers", "POST request with Content-Length: 0", "Null in request", "No Host header in HTTP/1.1 request", "Multiple host headers", "Host header contains IP address", "High ASCII characters in headers", "Header name with no header value", "Content length should be a positive number", "Chunked request with Content-Length header", "Check maximum number of parameters", "Check maximum number of headers", "Unescaped space in URL", "Body in GET or HEAD requests", "Bad multipart/form-data request parsing", "Bad multipart parameters parsing", "Bad HTTP version", "Bad host header value", "Check maximum number of cookies"]

    if http_protocol not in allowed_values :
      module.fail_json(msg=f"'{http_protocol}' is  not a valid value for the 'http_protocol' variable. It can be any of the following: {list(allowed_values)}.")
    

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

    # Update policy data with the new evasion technique configuration
    updated_policy_data, is_changed, message = http_compliance(policy_data, http_protocol, enabled)

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