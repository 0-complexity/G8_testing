password=$1

echo "[*] Install zerotier ..."
curl -s https://install.zerotier.com/ | sudo bash

echo "[*] Starting zerotier service ..."
zerotier-one -d

echo "[*] Installing pip, pip3 & xvfb ..."
apt-get install -y python-pip python3-pip xvfb iputils-ping

echo "[*] Add gig user ..."
echo "gig:x:1000:1000:gig,,,:/home/gig:/bin/bash" >> /etc/passwd && echo gig:${password} | chpasswd
adduser gig sudo 

echo "[*] Set password to user root ..."
echo -e "${password}\n${password}" | passwd

echo "[*] Allow password access ..."
sed -i 's/#PermitRootLogin yes/PermitRootLogin yes/g' /etc/ssh/sshd_config

echo "[*] Restart ssh service ..."
service ssh restart
