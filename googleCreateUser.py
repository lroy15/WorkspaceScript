from mxApiCall import mxGetUser
from dotenv import load_dotenv
import os

from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

load_dotenv()
mxUser = mxGetUser()
# Email of the Service Account
SERVICE_ACCOUNT_EMAIL = os.environ.get("CLI_EMAIL")

# Path to the Service Account's Private Key file
#SERVICE_ACCOUNT_FILE_PATH = 'credentialsfile.json'




def create_keyfile_dict():
    variables_keys = {
        "type": os.environ.get("ACC_TYPE"),
        "project_id": os.environ.get("PROJ_ID"),
        "private_key_id": os.environ.get("PRIV_KEY_ID"),
        "private_key": os.environ.get("PRIV_KEY"),
        "client_email": os.environ.get("CLI_EMAIL"),
        "client_id": os.environ.get("CLI_ID"),
        "auth_uri": os.environ.get("AUTH_URI"),
        "token_uri": os.environ.get("TOKEN_URI"),
        "auth_provider_x509_cert_url": os.environ.get("AUTH_PROV"),
        "client_x509_cert_url": os.environ.get("CLI_URL")
    }
    return variables_keys


def create_directory_service(user_email):
    """Build and returns an Admin SDK Directory service object authorized with the service accounts
    that act on behalf of the given user.

    Args:
      user_email: The email of the user. Needs permissions to access the Admin APIs.
    Returns:
      Admin SDK directory service object.
    """

    credentials = ServiceAccountCredentials.from_json_keyfile_dict(

        #create_keyfile_dict()
        {
        "type": os.environ.get("ACC_TYPE"),
        "project_id": os.environ.get("PROJ_ID"),
        "private_key_id": os.environ.get("PRIV_KEY_ID"),
        "private_key": os.environ.get("PRIV_KEY").replace('\\n', '\n'),
        "client_email": os.environ.get("CLI_EMAIL"),
        "client_id": os.environ.get("CLI_ID"),
        "auth_uri": os.environ.get("AUTH_URI"),
        "token_uri": os.environ.get("TOKEN_URI"),
        "auth_provider_x509_cert_url": os.environ.get("AUTH_PROV"),
        "client_x509_cert_url": os.environ.get("CLI_URL")
    },
        'https://www.googleapis.com/auth/admin.directory.user') #scope

    credentials = credentials.create_delegated(user_email)

    service = build('admin', 'directory_v1', credentials=credentials)

    body = { "name": 
            {"familyName":mxUser.name.split(' ')[1] , "givenName": mxUser.name.split(' ')[0]}, 
            "password": os.environ.get("WS_PW"), 
            "primaryEmail": mxUser.email+'@ljroy.com',
            "organizations": [
                {
                #"name": "Google Inc.",
                "title": mxUser.title,
                #"primary": true,
                #"type": "work",
                #"description": "Software engineer",
                "department": mxUser.department
                }
            ] 

    }
    # Call the Admin SDK Directory API
    user_add = service.users().insert(body=body).execute()

mxUserFirstName = mxUser.name.split(' ')[0]
mxUserLastName = mxUser.name.split(' ')[1]

print(f'==User info==\nFirst Name : {mxUserFirstName}\nLast Name : {mxUserLastName}\nEmail : {mxUser.email}@ljroy.com\nTitle : {mxUser.title}\nDepartment : {mxUser.department}')
confirmation = input('Is the information correct? y/n: ')

if confirmation != 'y' :
  print('Cancelling user creation')


else: 
  create_directory_service('julien@ljroy.com')

#create_directory_service('julien@ljroy.com')