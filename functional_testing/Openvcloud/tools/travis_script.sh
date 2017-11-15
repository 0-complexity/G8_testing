action=$1

if [[ ${action} == "before" ]]; then

    echo "[+] Joining zerotier network : ${zerotier_network}"
    sudo zerotier-cli join ${zerotier_network} > /dev/null

    echo "[+] Authorizing zerotier member"
    memberid=$(sudo zerotier-cli info | awk '{print $3}')
    curl -H "Content-Type: application/json" -H "Authorization: Bearer ${zerotier_token}" -X POST -d '{"config": {"authorized": true}}' https://my.zerotier.com/api/network/${zerotier_network}/member/${memberid} > /dev/null

    echo "[+] Cloning G8_testing repo : ${ctrl_ipaddress}"
    cmd="cd /tmp; rm -rf G8_testing; git clone -b ${TRAVIS_BRANCH} https://github.com/0-complexity/G8_testing"
    sshpass -p ${ctrl_password} ssh -t ${ctrl_user}@${ctrl_ipaddress} "${cmd}"

elif [[ ${action} == "test" ]]; then

    echo "[+] Executing testsuite from path : ${testsuite_dir}"
    cmd="cd /tmp/G8_testing/functional_testing/Openvcloud; nosetests -s -v ${testsuite_dir} --tc-file config.ini --tc=main.environment:${environment}"
    sshpass -p ${ctrl_password} ssh -t ${ctrl_user}@${ctrl_ipaddress} "${cmd}"

elif [[ ${action} == "after" ]]; then

    echo "[+] Removing G8_testing repo"
    sshpass -p ${ctrl_password} ssh -t ${ctrl_user}@${ctrl_ipaddress} "rm -rf /tmp/G8_testing"

fi