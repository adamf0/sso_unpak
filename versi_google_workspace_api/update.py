from googleapiclient.discovery import build
from google.oauth2 import service_account

SERVICE_ACCOUNT_FILE = "key.json"
SCOPES = ["https://www.googleapis.com/auth/admin.directory.user"]

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

admin_email = "admin@unpak.ac.id"
delegated_credentials = credentials.with_subject(admin_email)
service = build("admin", "directory_v1", credentials=delegated_credentials)

# Email user yang mau dipindah
user_key = "akt48@unpak.ac.id"

# Data yang diupdate (OU baru)
body = {
    "orgUnitPath": "/Mahasiswa/FKIP"
}

# Update user
service.users().update(userKey=user_key, body=body).execute()
print("User berhasil dipindahkan ke OU baru!")
