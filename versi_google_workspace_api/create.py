from googleapiclient.discovery import build
from google.oauth2 import service_account

# Load the service account credentials
SERVICE_ACCOUNT_FILE = "key.json"
SCOPES = ["https://www.googleapis.com/auth/admin.directory.user"]

# Authenticate and build the API client
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Set up admin API client
admin_email = "admin@unpak.ac.id"
delegated_credentials = credentials.with_subject(admin_email)
service = build("admin", "directory_v1", credentials=delegated_credentials)

user_info = {
    "name": {
        "givenName": "akt",
        "familyName": "48"
    },
    "password": "SecurePass123!",
    "primaryEmail": "akt48@unpak.ac.id",
    "orgUnitPath": "/Mahasiswa/FMIPA",
}

# Create the user
service.users().insert(body=user_info).execute()
print("User Created Successfully!")
