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

def override_signature_global(policy_json, signatureId, enabled):
  if "signatures" in  policy_json["policy"] :
    signature_exists, x = key_exists(policy_json["policy"]["signatures"], "signatureId", signatureId)
    if signature_exists :
      if check_value(policy_json["policy"]["signatures"][x], "enabled", enabled):
        return policy_json, False, "Alert! SignatureID: " + str(signatureId) + " already configured"
      else:
        policy_json["policy"]["signatures"][x]["enabled"] = str(enabled).lower()
    else:
      policy_json["policy"]["signatures"].append(json.loads('{"signatureId": '+str(signatureId)+',"enabled": '+str(enabled).lower()+'}'))
  else:
    policy_json["policy"]["signatures"] = json.loads('[{"signatureId": '+str(signatureId)+',"enabled": '+str(enabled).lower()+'}]')
    
  return policy_json, True, "Success! SignatureID: "+ str(signatureId)+" is configured"

def override_signature_on_entity(policy_json, signatureId, location, entity_name, enabled):
	if location in  policy_json["policy"] :
		header_exists, x = key_exists(policy_json["policy"][location], "name", entity_name)
		if header_exists :
			if "signatureOverrides" in policy_json["policy"][location][x]:
				signature_exists, y = key_exists(policy_json["policy"][location][x]["signatureOverrides"], "signatureId", signatureId)
				if signature_exists :
					if check_value(policy_json["policy"][location][x]["signatureOverrides"][y], "enabled", enabled):
						return policy_json, False, "Alert! SignatureID: "+ str(signatureId)+" on entity " + entity_name+ " is already configured"
					else:					
						policy_json["policy"][location][x]["signatureOverrides"][y]["enabled"] = str(enabled).lower()
				else:
					policy_json["policy"][location][x]["signatureOverrides"].append(json.loads('{"signatureId": '+str(signatureId)+',"enabled": '+str(enabled).lower()+'}'))
			else:
				policy_json["policy"][location][x]["signatureOverrides"] = json.loads('[{"signatureId": '+str(signatureId)+',"enabled": '+str(enabled).lower()+'}]')
		else:
			policy_json["policy"][location].append(json.loads('{"name": "'+entity_name+'","signatureOverrides":[{"signatureId":'+str(signatureId)+',"enabled":'+str(enabled).lower()+'}]}'))
	else:
		policy_json["policy"][location] = json.loads('[{"name": "'+entity_name+'","signatureOverrides": [{"signatureId": '+str(signatureId)+',"enabled": '+str(enabled).lower()+'}]}]') 
	
	return policy_json, True, "Success! SignatureID: "+ str(signatureId)+" on entity " + entity_name+ " is configured"

def main():
    module = AnsibleModule(
        argument_spec=dict(
            policy_path=dict(type='str', required=True),
            signature_id=dict(type='int', required=True),
            format=dict(type='str', required=True),
            entity_type=dict(type='str', required=False),
            entity=dict(type='str', required=False),
        )
    )

    policy_path = module.params['policy_path']
    sig_id = module.params['signature_id']
    if module.params['format'] is not None:
      format = module.params['format'].lower()
    else:
      entity_type = module.params['format']
    if module.params['entity_type'] is not None:
      entity_type = module.params['entity_type'].lower()
    else:
      entity_type = module.params['entity_type']
    entity = module.params['entity']

    if entity_type != None and entity_type != "urls" and entity_type != "cookies" and entity_type != "headers" and entity_type != "parameters":
      module.fail_json(msg=f"'{entity_type}' is  not a valid value for the 'entity_type' variable. It can be any of the following: headers/cookies/parameters/urls or do not define it for disabling the signature globally.")
    
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


    if entity_type is None or entity is None :
      jData, result, msg = override_signature_global(jData,sig_id,False)
    else :
      jData, result, msg = override_signature_on_entity(jData,sig_id,entity_type,entity,False)

    if result :
      module.exit_json(changed=True, msg=msg, policy=jData)
    else :
      module.exit_json(changed=False, msg=msg, policy=jData)
    
#    if (format == "yaml"):
#      yData["spec"] = jData
#      with open('policy_mod', 'w', encoding='utf-8') as f:
#        yaml.dump(yData, f, indent=2)
#    else:
#      with open('policy_mod', 'w', encoding='utf-8') as f:
#        json.dump(jData, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()