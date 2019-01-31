from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import json, os


# Email of the Service Account


# Path to the Service Account's Private Key file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
client_secret_file=os.path.join(BASE_DIR, "GSUIT DOMEN", "credentials.json")
#print(client_secret_file)
json_data=open(client_secret_file).read()
data=json.loads(json_data)
SERVICE_ACCOUNT_EMAIL =data["client_email"]
SERVICE_ACCOUNT_PKCS12_FILE_PATH = data["private_key"]
USER_EMAIL=data["user_email"]

def create_directory_service():
    """Build and returns an Admin SDK Directory service object authorized with the service accounts
    that act on behalf of the given user.

    Args:
      user_email: The email of the user. Needs permissions to access the Admin APIs.
    Returns:
      Admin SDK directory service object.
    """

    credentials = ServiceAccountCredentials._from_p12_keyfile_contents(
        SERVICE_ACCOUNT_EMAIL,
        SERVICE_ACCOUNT_PKCS12_FILE_PATH,
        'notasecret',
        scopes=['https://www.googleapis.com/auth/admin.directory.user',\
                "https://www.googleapis.com/auth/admin.directory.group",\
                "https://www.googleapis.com/auth/admin.directory.group.member",\
                "https://www.googleapis.com/auth/admin.directory.user.alias",\
                "https://www.googleapis.com/auth/admin.directory.userschema",\
                "https://www.googleapis.com/auth/admin.directory.domain"])

    credentials = credentials.create_delegated(USER_EMAIL)

    return build('admin', 'directory_v1', credentials=credentials)
if __name__=="__main__":
    create_directory_service("test@example.com")
