#!/bin/bash
set -e

if [ $# -ne 4 ] ; then
	echo "USAGE: $0 hostname domain dchostname username" >&2
	echo "Example: $0 iwg-gen0 d3catur.net dc0 rbmason" >&2
	exit 1
fi

HOST=$1
DOMAIN=$2
DOMAIN_UPPER=${DOMAIN^^}
WINS=`echo $DOMAIN_UPPER | cut -d. -f1`
DCHOSTNAME=$3
USER=$4

set -x

hostname $HOST
echo "127.0.0.1    $HOST.$DOMAIN      $HOST      localhost" > /etc/hosts
echo "$HOST" > /etc/hostname

apt-get install krb5-user libpam-krb5 winbind libpam-winbind ntp -y

cat > /etc/ntp.conf << EOF
driftfile /var/lib/ntp/ntp.drift
statistics loopstats peerstats clockstats
filegen loopstats file loopstats type day enable
filegen peerstats file peerstats type day enable
filegen clockstats file clockstats type day enable

# Put your ntp server here
# It might not be the domain controller - they don't have to
# be the same computer (might be e.g. ntp.usna.bluenet)
server $DCHOSTNAME.$DOMAIN

restrict -4 default kod notrap nomodify nopeer noquery
restrict -6 default kod notrap nomodify nopeer noquery
restrict 127.0.0.1
restrict ::1
EOF

service ntp stop
ntpd -gq
service ntp start

cat > /etc/krb5.conf << EOF
[logging]
        default = FILE:/var/log/krb5libs.log
        kdc = FILE:/var/log/krb5kdc.log
        admin_server = FILE:/var/log/kadmind.log

[libdefaults]
        default_realm = $DOMAIN_UPPER

[realms]
        $DOMAIN_UPPER = {
                kdc = $DCHOSTNAME.$DOMAIN
                admin_server = $DCHOSTNAME.$DOMAIN
        }

[domain_realm]
        .$DOMAIN = $DOMAIN_UPPER
        $DOMAIN = $DOMAIN_UPPER
EOF

kinit $USER@$DOMAIN_UPPER

cat > /etc/samba/smb.conf << EOF
[global]
        security = ads
        realm = $DOMAIN_UPPER
        workgroup = $WINS
        # winbind needs this but we wont' use this
        idmap config * : backend = tdb
        idmap config * : range = 90000-99999
        # don't collide with system accounts
        idmap config $WINS : backend = ad
        idmap config $WINS : range = 100000-200000
        winbind enum users = yes
        winbind enum groups = yes
        client use spnego = yes
        client ntlmv2 auth = yes
        client ldap sasl wrapping = sign
        encrypt passwords = yes
        winbind use default domain = yes
        # needed to ensure users have a login shell
        template shell = /bin/bash
        # Don't allow anonymous connections
        restrict anonymous = 2
EOF

service winbind stop
service winbind start
net ads join -U $USER -W $DOMAIN_UPPER

echo 'session required pam_mkhomedir.so' >> /etc/pam.d/login

cat > /etc/nsswitch.conf << EOF
passwd:     compat winbind
group:      compat winbind
shadow:     compat

hosts:      files mdns4_minimal [NOTFOUND=return] dns mdns4
networks:   files

protocols:  db files
services:   db files
ethers:     db files
rpc:        db files

netgroup:   nis
EOF

echo '%domain\ admins ALL=(root) ALL' >> /etc/sudoers
service winbind restart

set +x

echo SUCCESS
