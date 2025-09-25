from googleapiclient.discovery import build
from google.oauth2 import service_account

SERVICE_ACCOUNT_FILE = "key.json"
SCOPES = ["https://www.googleapis.com/auth/admin.directory.user"]

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

delegated_credentials = credentials.with_subject("admin@unpak.ac.id")
service = build("admin", "directory_v1", credentials=delegated_credentials)

# Email user yang mau dihapus
user_key = "akt48@unpak.ac.id"

# Hapus user
service.users().delete(userKey=user_key).execute()
print(f"User {user_key} berhasil dihapus!")
