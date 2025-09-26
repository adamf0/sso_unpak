from googleapiclient.discovery import build
from google.oauth2 import service_account
import jwt, time

# === Konfigurasi ===
SERVICE_ACCOUNT_FILE = "key.json"
SCOPES = ["https://www.googleapis.com/auth/admin.directory.user.readonly"]
ADMIN_EMAIL = "admin@unpak.ac.id"

JWT_SECRET = "supersecretkey"
JWT_ALGORITHM = "HS256"

# Simpan refresh tokens (contoh: in-memory dict)
refresh_tokens = {}

# === Google Service ===
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
delegated_credentials = credentials.with_subject(ADMIN_EMAIL)
service = build("admin", "directory_v1", credentials=delegated_credentials)

# Baca key dari file
# with open("private.pem", "r") as f:
#     PRIVATE_KEY = f.read()
# with open("public.pem", "r") as f:
#     PUBLIC_KEY = f.read()

# JWT_ALGORITHM = "RS256"

# def generate_access_token(email):
#     payload = {
#         "sub": email,
#         "iss": "unpak.ac.id",
#         "iat": int(time.time()),
#         "exp": int(time.time()) + 3600
#     }
#     return jwt.encode(payload, PRIVATE_KEY, algorithm=JWT_ALGORITHM)

# def verify_jwt(token):
#     try:
#         decoded = jwt.decode(token, PUBLIC_KEY, algorithms=[JWT_ALGORITHM])
#         return decoded
#     except jwt.ExpiredSignatureError:
#         return "Token expired"
#     except jwt.InvalidTokenError:
#         return "Invalid token"

def generate_access_token(email):
    payload = {
        "sub": email,
        "iss": "unpak.ac.id",
        "iat": int(time.time()),
        "exp": int(time.time()) + 3600  # berlaku 1 jam
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def generate_refresh_token(email):
    payload = {
        "sub": email,
        "type": "refresh",
        "iat": int(time.time()),
        "exp": int(time.time()) + 86400  # berlaku 1 hari
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    refresh_tokens[email] = token
    return token

def verify_jwt(token):
    try:
        decoded = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded
    except jwt.ExpiredSignatureError:
        return "Token expired"
    except jwt.InvalidTokenError:
        return "Invalid token"

def login(email, password):
    # 1. cek user ada di Google Workspace
    try:
        service.users().get(userKey=email).execute()
    except Exception:
        return None, None, "User tidak ditemukan"

    # 2. cek password (⚠️ ini dummy, karena password Google Workspace tidak bisa dicek via API)
    if password != "SecurePass123!":  # contoh hardcode
        return None, None, "Password salah"

    # 3. generate tokens
    access_token = generate_access_token(email)
    refresh_token = generate_refresh_token(email)

    return access_token, refresh_token, None

def refresh(token):
    try:
        decoded = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        if decoded.get("type") != "refresh":
            return None, "Invalid token type"

        email = decoded.get("sub")

        # Pastikan refresh token masih valid
        if refresh_tokens.get(email) != token:
            return None, "Refresh token revoked"

        # Buat access token baru
        new_access_token = generate_access_token(email)
        return new_access_token, None

    except jwt.ExpiredSignatureError:
        return None, "Refresh token expired"
    except jwt.InvalidTokenError:
        return None, "Invalid token"

# === Contoh penggunaan ===
if __name__ == "__main__":
    email = "akt48@unpak.ac.id"
    password = "SecurePass123!"

    access_token, refresh_token, err = login(email, password)
    if err:
        print("Login gagal:", err)
    else:
        print("Login sukses!")
        print("Access Token:", access_token)
        print("Refresh Token:", refresh_token)

        # Simulasi refresh
        new_access, err = refresh(refresh_token)
        if err:
            print("Refresh gagal:", err)
        else:
            print("Access Token baru:", new_access)
