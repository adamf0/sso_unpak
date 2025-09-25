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

# Ambil list user
results = service.users().list(
    customer="my_customer",
    # orgUnitPath="/Mahasiswa",
    orderBy="email"
).execute()
users = results.get("users", [])

# Cetak hasil
# for user in users:
#     print(f"{user['primaryEmail']} - {user['name']['fullName']} - OU: {user['orgUnitPath']}")

# Kalau mau lihat semua data JSON lengkap:
print(json.dumps(users, indent=2))
