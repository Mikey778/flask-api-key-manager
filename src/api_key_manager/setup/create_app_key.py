import sys
import os
up_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')
sys.path.append(up_dir)
from api_key_manager import ApiKeyManager
import json
from validate_email import validate_email



if __name__ == '__main__':
    exit_message = "Usage: python create_app_key user email project_name"
    if len(sys.argv) != 4:
        
        exit(exit_message)
    else:
        user = sys.argv[1]
        email = sys.argv[2]
        project_name = sys.argv[3]
        email_is_valid = validate_email(email)
    if not email_is_valid:
        exit('Please provide a valid email \n{}'.format(exit_message))
        

    api_key_manager = ApiKeyManager()
    obj = api_key_manager.create_key(user, email, project_name)

    # groom obj response for json conversion
    obj['createdAt'] = str(obj['createdAt'])
    obj['expirationDate'] = str(obj['expirationDate'])
    del obj['_id']

    obj_string = json.dumps(obj, indent=4)
    app_name = obj['application'].replace(' ','_')
    file_out = '{}_{}.json'.format(obj['uuid'], app_name)
    print(obj_string)
    this_path = os.path.dirname(os.path.realpath(__file__))
    file_out_path = this_path+'/keys/'+file_out
    with open(file_out_path, 'w') as f:
        f.write(obj_string)
