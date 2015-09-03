#!/bin/bash
set -e

CACHE=0
if [ $# -ne 4 ] ; then
	if [ $# -eq 5 ] && [ $5 = 'CACHE' ] ; then
		CACHE=1
	else
		echo "USAGE: $0 hostname domain dchostname username ['CACHE']" >&2
		echo "Example: $0 iwg-gen0 d3catur.net dc0 rbmason" >&2
		exit 1
	fi
fi

HOST=$1
DOMAIN=$2
DCHOSTNAME=$3
USER=$4

set -x

hostname $HOST
echo "127.0.0.1    $HOST.$DOMAIN      $HOST      localhost" > /etc/hosts
echo "$HOST" > /etc/hostname

apt-get install ntp realmd adcli sssd libsss-sudo crudini -y
mkdir -p /var/lib/samba/private
systemctl enable sssd

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

realm discover $DOMAIN
realm join --user=$USER $DOMAIN
crudini --set /etc/sssd/sssd.conf sssd default_domain_suffix $DOMAIN
systemctl start sssd

echo 'session required pam_mkhomedir.so' >> /etc/pam.d/common-session
echo "%domain\ admins@$DOMAIN ALL=(root) ALL" >> /etc/sudoers

[ $CACHE -eq 1 ] && apt-get install nss-updatedb libnss-db libpam-ccreds nscd -y

set +x

echo SUCCESS

