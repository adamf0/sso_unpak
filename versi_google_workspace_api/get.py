from googleapiclient.discovery import build
from google.oauth2 import service_account
import json

SERVICE_ACCOUNT_FILE = "key.json"
SCOPES = ["https://www.googleapis.com/auth/admin.directory.user.readonly"]

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

delegated_credentials = credentials.with_subject("admin@unpak.ac.id")
service = build("admin", "directory_v1", credentials=delegated_credentials)

user_key = "akt48@unpak.ac.id"

user = service.users().get(userKey=user_key).execute()
print(json.dumps(user, indent=2))
