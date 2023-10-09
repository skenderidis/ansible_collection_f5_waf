#!/usr/bin/python3
import json
import yaml

from ansible.module_utils.basic import AnsibleModule

def http_compliance(policy_json, name, enabled):
	if "blocking-settings" in  policy_json["policy"] :
		if "http-protocols" in policy_json["policy"]["blocking-settings"]:
			exists, x = key_exists(policy_json["policy"]["blocking-settings"]["http-protocols"],"description",name)
			if exists:
				if check_value(policy_json["policy"]["blocking-settings"]["http-protocols"][x], "enabled", enabled):
					return policy_json, False, "<b>Failed!</b> HTTP Protocol compliance sub-violation already disabled"
				else:
					policy_json["policy"]["blocking-settings"]["http-protocols"][x]["enabled"] = enabled
			else:
				policy_json["policy"]["blocking-settings"]["http-protocols"].append(json.loads('{"description": "'+name+'", "enabled":'+str(enabled).lower()+'}'))
		else:
			policy_json["policy"]["blocking-settings"]["http-protocols"] = json.loads('[{"description": "'+name+'", "enabled":'+str(enabled).lower()+'}]')
	else:
		policy_json["policy"]["blocking-settings"] = json.loads('{"http-protocols":[{"description": "'+name+'", "enabled":'+str(enabled).lower()+'}]}') 
	
	return policy_json, True, "<b>Success!</b> HTTP Protocol compliance sub-violation disabled"

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

def check_value(mod_json, key, value):
  try:
    if mod_json[key] == value:
      return True
    else: 
      return False
  except (KeyError , TypeError):
    return False

def main():
    module = AnsibleModule(
        argument_spec=dict(
            policy_path=dict(type='str', required=True),
            subviolation=dict(type='str', required=True),
            format=dict(type='str', required=True),
            enabled=dict(type='bool', required=False, default=False)
        )
    )

    policy_path = module.params['policy_path']
    enabled = module.params['enabled']
    subviolation = module.params['subviolation']
    format = module.params['format'].lower()

    allowed_values = ["Unparsable request content", "Several Content-Length headers", "POST request with Content-Length: 0", "Null in request", "No Host header in HTTP/1.1 request", "Multiple host headers", "Host header contains IP address", "High ASCII characters in headers", "Header name with no header value", "Content length should be a positive number", "Chunked request with Content-Length header", "Check maximum number of parameters", "Check maximum number of headers", "Unescaped space in URL", "Body in GET or HEAD requests", "Bad multipart/form-data request parsing", "Bad multipart parameters parsing", "Bad HTTP version", "Bad host header value", "Check maximum number of cookies"]

    if subviolation not in allowed_values :
      module.fail_json(msg=f"'{subviolation}' is  not a valid value for the 'subviolation' variable. It can be any of the following: {list(allowed_values)}.")
    
    try:
        with open(policy_path, 'r') as file:
          policy = file.read()
    except Exception as e:
        module.fail_json(msg=f"Failed to read file: {str(e)}")


    if (format == "yaml"):
      try:
        yData = yaml.safe_load(policy)
        jData = yData["spec"]
      except:
        module.fail_json(msg=f"Input file not YAML")
    else:
      try:
        jData = json.loads(policy)
      except:
        module.fail_json(msg=f"Input file not JSON")


    jData, result, msg = http_compliance(jData,subviolation,enabled)
    
    if result :   
      # if there is a change in the policy, update the file with the new policy and exit the module with a "changed" option
      if (format == "yaml"):
        yData["spec"] = jData
        with open('policy_mod', 'w', encoding='utf-8') as f: 
          yaml.dump(yData, f, indent=2) #Save the json format of the policy
        module.exit_json(changed=True, msg=msg, policy=yData) #Exit and provide the yaml format of the policy
      else:
        with open('policy_mod', 'w', encoding='utf-8') as f:
          json.dump(jData, f, ensure_ascii=False, indent=2) #Save the json format of the policy
        module.exit_json(changed=True, msg=msg, policy=jData)  #Exit and provide the json format of the policy
    else :
      if (format == "yaml"):  # if no change exit the module with a "No change" option
        module.exit_json(changed=False, msg=msg, policy=yData)  #Exit and provide the yaml format of the policy
      else:
        module.exit_json(changed=False, msg=msg, policy=jData)  #Exit and provide the json format of the policy

    

if __name__ == '__main__':
    main()