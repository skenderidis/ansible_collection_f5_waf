#!/usr/bin/python3
import json
import yaml

from ansible.module_utils.basic import AnsibleModule

#####  VIOL_COOKIE_LENGTH ######

def status_code(policy_json, code):
  default = [400,401,404,407,417,503]
  if code not in default:
    default = [400,401,404,407,417,503,code]
  if "general" in  policy_json["policy"] :
    if "allowedResponseCodes" in  policy_json["policy"]["general"]:
      header_exists, x = value_exists(policy_json["policy"]["general"]["allowedResponseCodes"], code)
      if not header_exists :
        policy_json["policy"]["general"]["allowedResponseCodes"].append(json.loads(str(code)))
      else:
        return policy_json, False, "Failed!. HTTP Response Code: "+ str(code)+" already configured"
    else:
      policy_json["policy"]["general"]["allowedResponseCodes"] = default
  else:
    policy_json["policy"]["general"] = json.loads('{"allowedResponseCodes":['+', '.join(map(str, default))+']}') 

  return policy_json, True, "Success!. HTTP Response Code: "+ str(code)+" is configured"

def value_exists(mod_json, value):
  x = 0
  exists = False
  for i in mod_json:
    if i == value:
      exists = True
      break;
    x = x + 1
  return (exists, x)

def main():
    module = AnsibleModule(
        argument_spec=dict(
            policy_path=dict(type='str', required=True),
            code=dict(type='int', required=True),
            format=dict(type='str', required=True),
        )
    )

    policy_path = module.params['policy_path']
    code = module.params['code']
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


    jData, result, msg = status_code(jData, code)

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