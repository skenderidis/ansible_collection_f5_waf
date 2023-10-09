#!/usr/bin/python3
import json
import yaml

from ansible.module_utils.basic import AnsibleModule

##### VIOL_FILETYPE
def illegal_filetype(policy_json, name, enabled):
	if "filetypes" in policy_json["policy"] :
		filetype_exists, x = key_exists(policy_json["policy"]["filetypes"], "name", name)
		if filetype_exists:
			if check_value(policy_json["policy"]["filetypes"][x], "$action", "delete"):
				del policy_json["policy"]["filetypes"][x]["$action"]
				policy_json["policy"]["filetypes"][x]["allowed"] = enabled		
				return policy_json, False, " Success! File Type allowed and $action=delete removed"
			if check_value(policy_json["policy"]["filetypes"][x], "allowed", enabled):
				return policy_json, False, "Failed! File Type " + name + " already set to allowed"
			else:
				policy_json["policy"]["filetypes"][x]["allowed"] = enabled			
		else:
			policy_json["policy"]["filetypes"].append(json.loads('{"name":"'+name+'","allowed":'+str(enabled).lower()+'}'))
	else:
		policy_json["policy"]["filetypes"] = json.loads('[{"name":"'+name+'","allowed":'+str(enabled).lower()+'}]')
	
	return policy_json, True, " Success! File Type " + name + " set to allowed"

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
            filetype=dict(type='str', required=True),
            format=dict(type='str', required=True),
            enabled=dict(type='bool', required=False, default=True)
        )
    )

    policy_path = module.params['policy_path']
    enabled = module.params['enabled']
    filetype = module.params['filetype']
    format = module.params['format'].lower()

    allowed_values = ["url", "request", "post_data", "qs_data"]

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

    jData, result, msg = illegal_filetype(jData,filetype,enabled)

    if result :   
      # if there is a change in the policy, update the file with the new policy and exit the module with a "changed" option
      if (format == "yaml"):
        yData["spec"] = jData
        with open('policy_mod', 'w', encoding='utf-8') as f:
          yaml.dump(yData, f, indent=2)
        module.exit_json(changed=True, msg=msg, policy=yData)
      else:
        with open('policy_mod', 'w', encoding='utf-8') as f:
          json.dump(jData, f, ensure_ascii=False, indent=2)
        module.exit_json(changed=True, msg=msg, policy=jData)
      
    else :
      # if nochange in the policy, update the file with the new policy and exit the module with a "changed" option
      if (format == "yaml"):
        module.exit_json(changed=False, msg=msg, policy=yData)
      else:
        module.exit_json(changed=False, msg=msg, policy=jData)


if __name__ == '__main__':
    main()