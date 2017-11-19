action=$1

if [ "$TRAVIS_EVENT_TYPE" == "cron" ] || [ "$TRAVIS_EVENT_TYPE" == "api" ]; then

    if [[ ${action} == "before" ]]; then

        ssh-keygen -f $HOME/.ssh/id_rsa -t rsa -N ''

        echo "[+] Joining zerotier network : ${zerotier_network}"
        sudo zerotier-cli join ${zerotier_network}; sleep 10

        echo "[+] Authorizing zerotier member"
        memberid=$(sudo zerotier-cli info | awk '{print $3}')
        curl -s -H "Content-Type: application/json" -H "Authorization: Bearer ${zerotier_token}" -X POST -d '{"config": {"authorized": true}}' https://my.zerotier.com/api/network/${zerotier_network}/member/${memberid} > /dev/null
       
        sleep 60

        echo "[+] Cloning G8_testing repo"
        cmd="cd /tmp; rm -rf G8_testing; git clone -b ${TRAVIS_BRANCH} https://github.com/0-complexity/G8_testing"
        sshpass -p "${ctrl_password}" ssh -t -o StrictHostKeyChecking=no ${ctrl_user}@${ctrl_ipaddress} "${cmd}"

        echo "[+] Install requirements"
        cmd="cd /tmp/G8_testing; pip install -r requirements.txt"
        sshpass -p "${ctrl_password}" ssh -t -o StrictHostKeyChecking=no ${ctrl_user}@${ctrl_ipaddress} "${cmd}"

    elif [[ ${action} == "test" ]]; then

        python_path="export PYTHONPATH=/opt/jumpscale7/lib:/opt/jumpscale7/lib/lib-dynload/:/opt/jumpscale7/bin:/opt/jumpscale7/lib/python.zip:/opt/jumpscale7/lib/plat-x86_64-linux-gnu"
        echo "[+] Executing testsuite from path : ${testsuite_dir}"
        cmd="export PYTHONPATH=${python_path}; cd /tmp/G8_testing/functional_testing/Openvcloud; nosetests -s -v ${testsuite_dir} --tc-file config.ini --tc=main.environment:${environment}"
        sshpass -p ${ctrl_password} ssh -t -o StrictHostKeyChecking=no ${ctrl_user}@${ctrl_ipaddress} "${cmd}"

    elif [[ ${action} == "after" ]]; then

        echo "[+] Removing G8_testing repo"
        sshpass -p ${ctrl_password} ssh -t -o StrictHostKeyChecking=no ${ctrl_user}@${ctrl_ipaddress} "rm -rf /tmp/G8_testing"

    fi

fi