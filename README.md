# SSO UNPAK
prototype untuk login menggunakan Keyclock dengan Provider LDAP beserta managen akun user menggunakan .NET Core API

# ALASAN
adanya temuan dari benyaknya dosen sekaligus menjadi PR besar untuk pihak IT karena untuk login pengguna setiap aplikasi berbeda akun. meskupun dari teknis sudah mengakali dengan cara menggunakan nidn, nip dan nim tetap belum terelasisai semua karena tingkat kompleksitas yg tidak terkendali (database berbeda server, request time out, server db down, dll). tim jaringan sudah memberikan ide dengan menggunakan LDAP yg dimana tujuan tambahannya dari radius wifi bisa akses langsung tanpa request api tambahan untuk login. 

# TUJUAN  
untuk memudahkan dalam authentication dan authorization

# ILUSTRASI

# TASK
1. deploy aplikasi keyclock dan ldap menggunakan docker ✅
2. konfigurasi ldap
    2.1 import data ❌
    2.2 tambah akun ❌
3. konfigurasi keycloack
    3.1 buat realm ❌
    3.2 buat client_id ❌
    3.3 menghubungkan ke provide ldap
4. management akun pengguna ❌
    4.1 create akun ❌
    4.2 update akun ❌
    4.3 delete akun ❌
5. auth login
    5.1 sebagai administrator ❌
    5.2 menggunakan credential ❌
    5.3 menggunakan akun ❌
6. security
    6.1 menggunakan ssl ❌
    6.2 enumeration, log4j & injection ❌
    6.3 secure image docker ❌
7. login menggunakan google account (opsional) 