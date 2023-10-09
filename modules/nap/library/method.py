#!/usr/bin/python3
import json
import yaml

from ansible.module_utils.basic import AnsibleModule

#####  VIOL_METHOD ######
def http_method(policy_json, method):
	if "methods" in  policy_json["policy"] :
		method_exists, x = key_exists(policy_json["policy"]["methods"], "name", method)
		if method_exists:
			if check_value(policy_json["policy"]["methods"][x], "$action", "delete"):
				del policy_json["policy"]["methods"][x]["$action"]
				return policy_json, True, "Success! Method " + method + " allowed by removing $action=delete"
			else:
				return policy_json, False, "Failed!. Method " + method +  " already configured"
		else:
			policy_json["policy"]["methods"].append(json.loads('{"name": "'+method+'"}'))
	else:
		policy_json["policy"]["methods"] = json.loads('[{"name": "'+method+'"}]')
		
	return policy_json, True, "Success! Method " + method +  " added on the allowed list"

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
            method=dict(type='str', required=True),
            format=dict(type='str', required=True)
        )
    )

    policy_path = module.params['policy_path']
    method = module.params['method']
    format = module.params['format'].lower()
    
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

    jData, result, msg = http_method(jData,method)
    
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