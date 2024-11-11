# SSO UNPAK

Prototype untuk login menggunakan **Keycloak** dengan Provider **LDAP** beserta manajemen akun user menggunakan **.NET Core API**.

## ALASAN

Adanya temuan dari banyaknya dosen sekaligus menjadi PR besar untuk pihak IT karena untuk login pengguna setiap aplikasi berbeda akun. Meskipun dari teknis sudah mengakali dengan cara menggunakan **nidn**, **nip**, dan **nim**, tetap belum teratasi semua karena tingkat kompleksitas yang tidak terkendali (database berbeda server, request time out, server db down, dll). Tim jaringan sudah memberikan ide dengan menggunakan **LDAP** yang di mana tujuan tambahannya dari radius wifi bisa akses langsung tanpa request API tambahan untuk login. 

## TUJUAN  

Untuk memudahkan dalam **authentication** dan **authorization**.

## ILUSTRASI

_(Add visual diagrams or further explanation here if needed.)_

## TASK

1. **Deploy aplikasi Keycloak dan LDAP menggunakan Docker** ✅
2. **Konfigurasi LDAP**
   - 2.1 Import data LDAP ✅
   - 2.2 Tambah akun ❌
3. **Konfigurasi Keycloak**
   - 3.1 Buat realm Keycloak ✅
   - 3.2 Buat client_id Keycloak ✅
   - 3.3 Menghubungkan ke provider LDAP ✅
4. **Management akun pengguna**
   - 4.1 Create akun ✅
   - 4.2 Update akun ✅
   - 4.3 Delete akun ✅
5. **Auth login**
   - 5.1 Login sebagai administrator ✅
   - 5.2 Login menggunakan credential ✅
   - 5.3 Login menggunakan akun ✅
6. **Security**
   - 6.1 Menggunakan SSL ❌
   - 6.2 Enumeration, Log4j & injection ❌
   - 6.3 Secure image Docker ❌
7. **Login menggunakan Google account (opsional)**
