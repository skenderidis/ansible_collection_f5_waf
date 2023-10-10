#!/usr/bin/python3
import json
import yaml

from ansible.module_utils.basic import AnsibleModule

#####  VIOL_HEADER_LENGTH ######

def header_length(policy_json, length):
	if length > 65536:
		length = 65536
	if length < 1:
		length = 1
	if "header-settings" in  policy_json["policy"] :
		if check_value(policy_json["policy"]["header-settings"], "maximumHttpHeaderLength",length):
			return policy_json, False, "Error!. Same Header length is already configured"
		else:		
			policy_json["policy"]["header-settings"]["maximumHttpHeaderLength"] = length
	else:
		policy_json["policy"]["header-settings"] = json.loads('{"maximumHttpHeaderLength": '+str(length)+'}')

	return policy_json, True, "Success!. Header length: "+ str(length)+" is configured"


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
            value=dict(type='int', required=True),
            format=dict(type='str', required=True)
        )
    )

    policy_path = module.params['policy_path']
    value = module.params['value']
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

    jData, result, msg = header_length(jData,value)
    
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