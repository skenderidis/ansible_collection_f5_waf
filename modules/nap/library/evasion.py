#!/usr/bin/python3
import json
import yaml

from ansible.module_utils.basic import AnsibleModule

def is_json(myjson):
  try:
    json.loads(myjson)
  except ValueError as e:
    return False
  return True

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

def value_exists(mod_json, value):
  x = 0
  exists = False
  for i in mod_json:
    if i == value:
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

def check_value_array(mod_json, key, value):
  try:
    if value.isnumeric():
      value = int(value)
    if value in mod_json[key]:
      return True
    else: 
      return False
  except (KeyError , TypeError):
    return False

def evasion_technique(policy_json, name, enabled):
	if "blocking-settings" in  policy_json["policy"] :
		if "evasions" in policy_json["policy"]["blocking-settings"]:
			exists, x = key_exists(policy_json["policy"]["blocking-settings"]["evasions"],"description",name)
			if exists :
				if check_value(policy_json["policy"]["blocking-settings"]["evasions"][x], "enabled", enabled):
					return policy_json, False, "<b>Failed!</b> Evasion technique sub-violation already disabled"
				else:
					policy_json["policy"]["blocking-settings"]["evasions"][x]["enabled"] = enabled
			else:
				policy_json["policy"]["blocking-settings"]["evasions"].append(json.loads('{"description": "'+name+'", "enabled":'+str(enabled).lower()+'}'))
		else:
			policy_json["policy"]["blocking-settings"]["evasions"] = json.loads('[{"description": "'+name+'", "enabled":'+str(enabled).lower()+'}]')
	else:
		policy_json["policy"]["blocking-settings"] = json.loads('{"evasions":[{"description": "'+name+'", "enabled":'+str(enabled).lower()+'}]}') 
	
	return policy_json, True, "<b>Success!</b> Evasion technique sub-violation disabled"

def main():
    module = AnsibleModule(
        argument_spec=dict(
            policy_path=dict(type='str', required=True),
            evasion=dict(type='str', required=True),
            format=dict(type='str', required=True),
            enabled=dict(type='bool', required=False, default=False)
        )
    )

    policy_path = module.params['policy_path']
    enabled = module.params['enabled']
    evasion = module.params['evasion']
    format = module.params['format'].lower()

    allowed_values = ["%u decoding", "Apache whitespace", "Bad unescape", "Bare byte decoding", "Directory traversals","IIS backslashes", "IIS Unicode codepoints", "Multiple decoding"]

    if evasion not in allowed_values :
      module.fail_json(msg=f"'{evasion}' is  not a valid value for the 'evasion' variable. It can be any of the following: {list(allowed_values)}.")
    
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


    jData, result, msg = evasion_technique(jData,evasion,enabled)
    
    

    if result :
      module.exit_json(changed=True, msg=msg, policy=jData)
    else :
      module.exit_json(changed=False, msg=msg, policy=jData)
    

if __name__ == '__main__':
    main()