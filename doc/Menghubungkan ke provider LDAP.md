1. pastikan udah login sebelumnya
2. klik menu **Keycloak** dan klik nama realmnya
3. klik menu **User federation** dan tombol **Add LDAP provider**
4. isi dengan konfigurasi berikut ini.
```
Connection URL: ldap://host.docker.internal:389
Bind type: simple
Bind DN: cn=admin,dc=mycompany,dc=com
Bind credentials: admin
```
5. tes koneksi dan auth nya
6. isi dengan konfigurasi berikut ini.
```
Edit mode: READ_ONLY
Users DN: ou=users,dc=mycompany,dc=com
Username LDAP attribute: cn
RDN LDAP attribute: cn
UUID LDAP attribute: entryUUID
User object classes: inetOrgPerson
Search scope: Subtree
Periodic full: on
Full sync period: 604800
Periodic changed users: on
Changed users sync period: 86400
```
