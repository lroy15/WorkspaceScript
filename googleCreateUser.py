from mxApiCall import mxGetUser


from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

mxUser = mxGetUser()
# Email of the Service Account
SERVICE_ACCOUNT_EMAIL = 'julien@intricate-dryad-349319.iam.gserviceaccount.com'

# Path to the Service Account's Private Key file
SERVICE_ACCOUNT_FILE_PATH = 'v1/credentialsfile.json'

def create_directory_service(user_email):
    """Build and returns an Admin SDK Directory service object authorized with the service accounts
    that act on behalf of the given user.

    Args:
      user_email: The email of the user. Needs permissions to access the Admin APIs.
    Returns:
      Admin SDK directory service object.
    """

    credentials = ServiceAccountCredentials.from_json_keyfile_name(

        SERVICE_ACCOUNT_FILE_PATH,
        'https://www.googleapis.com/auth/admin.directory.user') #scope

    credentials = credentials.create_delegated(user_email)

    service = build('admin', 'directory_v1', credentials=credentials)

    body = { "name": 
            {"familyName":mxUser.name.split(' ')[1] , "givenName": mxUser.name.split(' ')[0]}, 
            "password": "test1234", 
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
confirmation = input('Is the information correct? Y/N: ')

if confirmation != 'Y' :
  print('Cancelling user creation')


else: 
  create_directory_service('julien@ljroy.com')

#create_directory_service('julien@ljroy.com')