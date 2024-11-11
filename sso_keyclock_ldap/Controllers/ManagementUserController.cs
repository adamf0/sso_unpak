using Microsoft.AspNetCore.Mvc;
using Novell.Directory.Ldap;

namespace sso_keyclock_ldap.Controllers
{
    [ApiController]
    [Route("/user")]
    public class ManagementUserController : ControllerBase
    {
        private readonly string ldapServer = "host.docker.internal";
        private readonly string ldapDN = "cn=admin,dc=mycompany,dc=com"; // User dengan hak admin LDAP
        private readonly string ldapPassword = "admin";
        private readonly string ldapBaseDn = "ou=users,dc=mycompany,dc=com"; // Menyesuaikan dengan struktur LDAP Anda

        // POST api/ldap/adduser
        [HttpPost("adduser")]
        public IActionResult AddLdapUser([FromBody] LdapUser newUser)
        {
            try
            {
                LdapConnection ldapConn = new LdapConnection();
                ldapConn.Connect(ldapServer, 389);
                ldapConn.Bind(ldapDN, ldapPassword);
                LdapAttributeSet attributeSet = new LdapAttributeSet();
                attributeSet.Add(new LdapAttribute("objectclass", "inetOrgPerson"));
                //attributeSet.Add(new LdapAttribute("cn", new string[] { newUser.Username, newUser.Email })); //username
                attributeSet.Add(new LdapAttribute("givenname", newUser.DisplayName));
                attributeSet.Add(new LdapAttribute("sn", newUser.Username));
                attributeSet.Add(new LdapAttribute("userpassword", newUser.Password));
                attributeSet.Add(new LdapAttribute("mail", newUser.Email));
 
                string dn = $"cn={newUser.Username},{ldapBaseDn}";
                LdapEntry newEntry = new LdapEntry(dn, attributeSet);
                ldapConn.Add(newEntry);

                return Ok("User successfully added.");
            }
            catch (Exception ex)
            {
                return StatusCode(500, $"Error creating user data: {ex.Message}");
            }
        }
        [HttpPost("updateuser")]
        public IActionResult UpdateLdapUser([FromBody] LdapUser request)
        {
            try
            {
                LdapConnection ldapConn = new LdapConnection();
                ldapConn.Connect(ldapServer, 389);
                ldapConn.Bind(ldapDN, ldapPassword);

                string dn = $"cn={request.Username},{ldapBaseDn}";

                var modifications = new List<LdapModification>();
                modifications.Add(new LdapModification(LdapModification.REPLACE, new LdapAttribute("givenName", request.DisplayName)));
                modifications.Add(new LdapModification(LdapModification.REPLACE, new LdapAttribute("sn", request.Username)));
                modifications.Add(new LdapModification(LdapModification.REPLACE, new LdapAttribute("mail", request.Email)));
                modifications.Add(new LdapModification(LdapModification.REPLACE, new LdapAttribute("userPassword", request.Password)));
                ldapConn.Modify(dn, modifications.ToArray());

                return Ok("User data successfully updated.");
            }
            catch (Exception ex)
            {
                return StatusCode(500, $"Error updating user data: {ex.Message}");
            }
        }
        [HttpPost("deleteuser")]
        public IActionResult DeleteLdapUser([FromBody] LdapUser request)
        {
            try
            {
                LdapConnection ldapConn = new LdapConnection();
                ldapConn.Connect(ldapServer, 389);
                ldapConn.Bind(ldapDN, ldapPassword);
                string dn = $"cn={request.Username},{ldapBaseDn}";
                ldapConn.Delete(dn);

                return Ok("User data successfully delete.");
            }
            catch (Exception ex)
            {
                return StatusCode(500, $"Error delete user data: {ex.Message}");
            }
        }
    }
 }

    // Model untuk data pengguna yang diterima dalam permintaan POST
    public class LdapUser
    {
        public string Username { get; set; }
        public string FirstName { get; set; }
        public string LastName { get; set; }
        public string DisplayName { get; set; }
        public string Email { get; set; }
        public string Password { get; set; }
    }
