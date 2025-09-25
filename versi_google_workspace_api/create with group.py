from googleapiclient.discovery import build
from google.oauth2 import service_account

# === Konfigurasi ===
SERVICE_ACCOUNT_FILE = "key.json"
SCOPES = [
    "https://www.googleapis.com/auth/admin.directory.user",
    "https://www.googleapis.com/auth/admin.directory.group",
    "https://www.googleapis.com/auth/admin.directory.rolemanagement"
]

# Super Admin email untuk impersonasi
admin_email = "admin@unpak.ac.id"

# === Auth ===
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
delegated_credentials = credentials.with_subject(admin_email)

# Service utama
service = build("admin", "directory_v1", credentials=delegated_credentials)

# === 1. Buat User Baru ===
user_email = "akt48@unpak.ac.id"
user_info = {
    "name": {"givenName": "akt", "familyName": "48"},
    "password": "SecurePass123!",
    "primaryEmail": user_email,
    "orgUnitPath": "/Mahasiswa/FMIPA",
}

try:
    created_user = service.users().insert(body=user_info).execute()
    user_id = created_user["id"]  # userId numerik untuk role assignment
    print(f"✅ User {user_email} berhasil dibuat (id={user_id})")
except Exception as e:
    print(f"❌ Gagal membuat user: {e}")
    exit(1)

# === 2. Pastikan Group Ada ===
group_email = "mahasiswa-fmipa@unpak.ac.id"
try:
    group = service.groups().get(groupKey=group_email).execute()
    print(f"ℹ️ Group sudah ada: {group['email']}")
except:
    # Kalau group tidak ditemukan, buat baru
    group_body = {
        "email": group_email,
        "name": "Mahasiswa FMIPA",
        "description": "Group Mahasiswa FMIPA"
    }
    group = service.groups().insert(body=group_body).execute()
    print(f"✅ Group dibuat: {group['email']}")

# === 3. Tambahkan User ke Group ===
member_body = {"email": user_email, "role": "MEMBER"}
try:
    service.members().insert(groupKey=group_email, body=member_body).execute()
    print(f"✅ User {user_email} berhasil ditambahkan ke group {group_email}")
except Exception as e:
    print(f"❌ Gagal menambahkan ke group: {e}")