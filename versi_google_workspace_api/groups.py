from googleapiclient.discovery import build
from google.oauth2 import service_account
import json

# === Konfigurasi ===
SERVICE_ACCOUNT_FILE = "key.json"
SCOPES = [
    "https://www.googleapis.com/auth/admin.directory.group",
    "https://www.googleapis.com/auth/admin.directory.group.member"
]
admin_email = "admin@unpak.ac.id"

# === Auth ===
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
delegated_credentials = credentials.with_subject(admin_email)
service = build("admin", "directory_v1", credentials=delegated_credentials)

# ================== GROUP CRUD ==================
def create_group(email, name, desc=""):
    body = {"email": email, "name": name, "description": desc}
    return service.groups().insert(body=body).execute()

def get_group(group_email):
    return service.groups().get(groupKey=group_email).execute()

def list_groups(domain="unpak.ac.id"):
    return service.groups().list(domain=domain).execute()

def update_group(group_email, new_email=None, new_name=None, new_desc=None):
    body = {}
    if new_email:
        body["email"] = new_email
    if new_name:
        body["name"] = new_name
    if new_desc:
        body["description"] = new_desc

    if not body:
        raise ValueError("Tidak ada field yang diberikan untuk update.")

    return service.groups().update(groupKey=group_email, body=body).execute()


def delete_group(group_email):    
    return service.groups().delete(groupKey=group_email).execute()

# ================== MEMBER CRUD ==================
def add_member(group_email, member_email, role="MEMBER"):
    body = {"email": member_email, "role": role}
    return service.members().insert(groupKey=group_email, body=body).execute()

def delete_member(group_email, member_email):
    service.members().delete(groupKey=group_email, memberKey=member_email).execute()
    return f"{member_email} dihapus dari {group_email}"

def list_members(group_email):
    return service.members().list(groupKey=group_email).execute()

# ================== DEMO ==================
if __name__ == "__main__":
    group_email = "mahasiswa-fmipa@unpak.ac.id"

    # 1. Create group
    # try:
    #     g = create_group(group_email, "Mahasiswa FMIPA", "Group Mahasiswa FMIPA")
    #     print(f"✅ Group dibuat: {g['email']}")
    # except Exception as e:
    #     print(f"ℹ️ Mungkin group sudah ada: {e}")

    # 2. Add member
    # try:
    #     m = add_member(group_email, "akt48@unpak.ac.id")
    #     print(f"✅ Member ditambahkan: {m['email']}")
    # except Exception as e:
    #     print(f"❌ Gagal tambah member: {e}")

    # 3. List members
    # members = list_members(group_email)
    # print(json.dumps(members["members"], indent=2))

    # 4. Delete member
    # try:
    #     print(delete_member(group_email, "akt48@unpak.ac.id"))
    # except Exception as e:
    #     print(f"❌ Gagal hapus member: {e}")

    # 5. update group
    # try:
    #     update_group(
    #         "mahasiswa-fmipa@unpak.ac.id",
    #         new_email="fmipa-baru@unpak.ac.id",
    #         new_name="Mahasiswa FMIPA Angkatan Baru",
    #         new_desc="Group mahasiswa FMIPA 2025"
    #     )
    #     print(f"✅ Group berhasil update group")
    # except Exception as e:
    #     print(f"❌ Gagal update group: {e}")

    # 6. Delete group (opsional)
    # try:
    #     delete_group(group_email)
    #     print(f"✅ Group berhasil hapus group")
    # except Exception as e:
    #     print(f"❌ Gagal hapus group: {e}")
