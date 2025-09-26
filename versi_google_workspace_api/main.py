#uvicorn main:app --reload --host 0.0.0.0 --port 8000

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from googleapiclient.discovery import build
from google.oauth2 import service_account
import re
import urllib.parse
import unicodedata
import jwt, time
from fastapi import Header

# === Konfigurasi ===
SERVICE_ACCOUNT_FILE = "key.json"
SCOPES = [
    "https://www.googleapis.com/auth/admin.directory.user",
    "https://www.googleapis.com/auth/admin.directory.group",
    "https://www.googleapis.com/auth/admin.directory.group.member"
]
ADMIN_EMAIL = "admin@unpak.ac.id"

# Load credentials & build service
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
delegated_credentials = credentials.with_subject(ADMIN_EMAIL)
service = build("admin", "directory_v1", credentials=delegated_credentials)

# === FastAPI ===
app = FastAPI(title="Google Workspace User Management API")

# === Models ===
class UserCreateRequest(BaseModel):
    givenName: str
    familyName: str
    password: str
    primaryEmail: str
    orgUnitPath: str

class UserUpdateRequest(BaseModel):
    userKey: str
    givenName: str
    familyName: str
    password: str
    orgUnitPath: str

class GroupCreateRequest(BaseModel):
    email: str
    name: str
    description: str = ""

class GroupUpdateRequest(BaseModel):
    new_email: str
    new_name: str
    new_desc: str = ""

class MemberAddRequest(BaseModel):
    member_email: str
    role: str = "MEMBER"

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str

class RefreshRequest(BaseModel):
    refresh_token: str

class RefreshResponse(BaseModel):
    access_token: str

# class VerifyJWTRequest(BaseModel):
#     token: str

class VerifyJWTResponse(BaseModel):
    valid: bool
    payload: dict = None

# === Util Functions ===
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%-]+@unpak\.ac\.id$')

def decode_validate_email(email: str, check_domain=True) -> str:
    """Decode, normalize, and validate an email."""
    decoded = urllib.parse.unquote(email)
    if '%' in decoded:
        raise HTTPException(status_code=400, detail="Email tampak double-encoded, request ditolak.")
    decoded = unicodedata.normalize('NFC', decoded)
    try:
        decoded.encode('ascii')
    except UnicodeEncodeError:
        raise HTTPException(status_code=400, detail="Email mengandung karakter non-ASCII yang tidak diperbolehkan.")
    if check_domain and not EMAIL_REGEX.fullmatch(decoded):
        raise HTTPException(status_code=400, detail="Hanya email valid @unpak.ac.id yang diperbolehkan.")
    return decoded

ORG_UNIT_REGEX = re.compile(r'^(/[a-zA-Z0-9 _\-/]+)+$')

def validate_org_unit_path(path: str) -> str:
    # Decode URL-encoded
    decoded = urllib.parse.unquote(path)
    
    # Cek double-encoded
    if '%' in decoded:
        raise HTTPException(status_code=400, detail="orgUnitPath tampak double-encoded, request ditolak.")
    
    # Normalize unicode
    decoded = unicodedata.normalize('NFC', decoded)
    
    # Pastikan ASCII
    try:
        decoded.encode('ascii')
    except UnicodeEncodeError:
        raise HTTPException(status_code=400, detail="orgUnitPath mengandung karakter non-ASCII.")
    
    # Harus diawali "/"
    if not decoded.startswith('/'):
        raise HTTPException(status_code=400, detail="orgUnitPath harus dimulai dengan '/'")
    
    # Cegah traversal (.. atau \\)
    if '..' in decoded or '\\' in decoded or '//' in decoded:
        raise HTTPException(status_code=400, detail="orgUnitPath mengandung karakter terlarang.")
    
    # Cek regex valid
    if not ORG_UNIT_REGEX.fullmatch(decoded):
        raise HTTPException(status_code=400, detail="orgUnitPath mengandung karakter tidak valid.")
    
    return decoded

def handle_google_api(func, *args, **kwargs):
    try:
        return func(*args, **kwargs).execute()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ================== GROUP ENDPOINTS ==================
@app.post("/group/create")
async def create_group(req: GroupCreateRequest):
    email = decode_validate_email(req.email, check_domain=False)
    body = {"email": email, "name": req.name, "description": req.description}
    group = handle_google_api(service.groups().insert, body=body)
    return {"message": "Group berhasil dibuat", "group": group}

@app.get("/group/{group_email}")
async def get_group(group_email: str):
    email = decode_validate_email(group_email, check_domain=False)
    return handle_google_api(service.groups().get, groupKey=email)

@app.get("/groups")
async def list_groups(domain: str = "unpak.ac.id"):
    domain_decoded = urllib.parse.unquote(domain)
    if '%' in domain_decoded:
        raise HTTPException(status_code=400, detail="Domain tampak double-encoded, request ditolak.")
    return handle_google_api(service.groups().list, domain=domain_decoded)

@app.put("/groups/{group_email}")
async def update_group(group_email: str, req: GroupUpdateRequest):
    email = decode_validate_email(group_email, check_domain=False)
    body = {k: v for k, v in {"email": req.new_email, "name": req.new_name, "description": req.new_desc}.items() if v}
    if not body:
        raise HTTPException(status_code=400, detail="Tidak ada field yang diberikan untuk update.")
    group = handle_google_api(service.groups().update, groupKey=email, body=body)
    return {"message": "Group berhasil diupdate", "group": group}

@app.delete("/groups/{group_email}")
async def delete_group(group_email: str):
    email = decode_validate_email(group_email, check_domain=False)
    handle_google_api(service.groups().delete, groupKey=email)
    return {"message": f"Group {email} berhasil dihapus!"}

# ================== MEMBER ENDPOINTS ==================
@app.post("/groups/{group_email}/members")
async def add_member(group_email: str, req: MemberAddRequest):
    email = decode_validate_email(group_email, check_domain=False)
    member_email = decode_validate_email(req.member_email)
    body = {"email": member_email, "role": req.role}
    member = handle_google_api(service.members().insert, groupKey=email, body=body)
    return {"message": f"Member {member_email} berhasil ditambahkan", "member": member}

@app.get("/groups/{group_email}/members")
async def list_members(group_email: str):
    email = decode_validate_email(group_email, check_domain=False)
    return handle_google_api(service.members().list, groupKey=email)

@app.delete("/groups/{group_email}/members/{member_email}")
async def delete_member(group_email: str, member_email: str):
    email = decode_validate_email(group_email, check_domain=False)
    member_email = decode_validate_email(member_email)
    handle_google_api(service.members().delete, groupKey=email, memberKey=member_email)
    return {"message": f"Member {member_email} berhasil dihapus dari {email}"}

# ================== USER ENDPOINTS ==================
@app.get("/users")
async def list_users(orgUnitPath: str = None):
    params = {"customer": "my_customer", "orderBy": "email"}
    if orgUnitPath:
        params["orgUnitPath"] = orgUnitPath
    results = handle_google_api(service.users().list, **params)
    return {"users": results.get("users", [])}

@app.get("/user/{userKey}")
async def get_user(userKey: str):
    email = decode_validate_email(userKey)
    return handle_google_api(service.users().get, userKey=email)

@app.post("/user/create")
async def create_user(req: UserCreateRequest):
    email = decode_validate_email(req.primaryEmail)
    org_path = validate_org_unit_path(req.orgUnitPath)

    body = {
        "name": {"givenName": req.givenName, "familyName": req.familyName},
        "password": req.password,
        "primaryEmail": email,
        "orgUnitPath": org_path,
    }
    user = handle_google_api(service.users().insert, body=body)
    return {"message": f"User {email} berhasil disimpan", "user": user}

@app.post("/user/update")
async def update_user(req: UserUpdateRequest):
    email = decode_validate_email(req.userKey)
    org_path = validate_org_unit_path(req.orgUnitPath)

    body = {
        "name": {"givenName": req.givenName, "familyName": req.familyName},
        "password": req.password,
        "orgUnitPath": req.orgUnitPath,
    }
    user = handle_google_api(service.users().update, userKey=email, body=body)
    return {"message": f"User {email} berhasil diupdate", "user": user}

@app.delete("/user/{userKey}")
async def delete_user(userKey: str):
    email = decode_validate_email(userKey)
    handle_google_api(service.users().delete, userKey=email)
    return {"message": f"User {email} berhasil dihapus!"}


JWT_SECRET = "supersecretkey"
JWT_ALGORITHM = "HS256"
refresh_tokens = {}

def generate_access_token(email: str):
    payload = {
        "sub": email,
        "iss": "unpak.ac.id",
        "iat": int(time.time()),
        "exp": int(time.time()) + 3600  # berlaku 1 jam
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def generate_refresh_token(email: str):
    payload = {
        "sub": email,
        "type": "refresh",
        "iat": int(time.time()),
        "exp": int(time.time()) + 86400  # berlaku 1 hari
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    refresh_tokens[email] = token
    return token

def verify_jwt(token: str):
    try:
        decoded = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded
    except jwt.ExpiredSignatureError:
        return "Token expired"
    except jwt.InvalidTokenError:
        return "Invalid token"

def login_user(email: str, password: str):
    # 1. cek user ada di Google Workspace
    try:
        service.users().get(userKey=email).execute()
    except Exception:
        return None, None, "User tidak ditemukan"

    # 2. cek password (⚠️ dummy, karena Google password tidak bisa dicek via API)
    if password != "SecurePass123!":
        return None, None, "Password salah"

    # 3. generate tokens
    access_token = generate_access_token(email)
    refresh_token = generate_refresh_token(email)

    return access_token, refresh_token, None

def refresh_access_token(token: str):
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

@app.post("/login", response_model=LoginResponse)
async def login(req: LoginRequest):
    email = decode_validate_email(req.email)

    access, refresh, err = login_user(email, req.password)
    if err:
        raise HTTPException(status_code=401, detail={err})
    return {"access_token": access, "refresh_token": refresh}

@app.post("/refresh", response_model=RefreshResponse)
async def refresh(req: RefreshRequest):
    token = req.refresh_token

    try:
        decoded = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM],  # pastikan algoritma sesuai
            options={"verify_exp": True} # cek expiration
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail={"Refresh token expired"}
        )
    except jwt.InvalidAlgorithmError:
        raise HTTPException(
            status_code=401,
            detail={"Token algoritma tidak valid"}
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail={"Token tidak valid"}
        )

    # --- Cek type token harus "refresh" --- #
    if decoded.get("type") != "refresh":
        raise HTTPException(
            status_code=401,
            detail={"Token bukan refresh token"}
        )

    email = decode_validate_email(decoded.get("sub"))

    # --- Pastikan refresh token masih tersimpan / belum dicabut --- #
    if refresh_tokens.get(email) != token:
        raise HTTPException(
            status_code=401,
            detail={"Refresh token dicabut"}
        )

    new_access, err = refresh_access_token(req.refresh_token)
    if err:
        raise HTTPException(status_code=401, detail={err})
    return {"access_token": new_access}

@app.get("/verify_jwt", response_model=VerifyJWTResponse)
async def verify_jwt_endpoint(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail={"error": "Invalid Input", "message": "Header Authorization harus Bearer <token>"}
        )
    
    token = authorization.split(" ", 1)[1]

    try:
        decoded = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM],  
            options={"verify_exp": True} 
        )
        return {"valid": True, "payload": decoded}
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail={"Token expired"}
        )
    except jwt.InvalidAlgorithmError:
        raise HTTPException(
            status_code=401,
            detail={"Token algoritma tidak valid"}
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail={"Token tidak valid"}
        )