action=$1

if [ "$TRAVIS_EVENT_TYPE" == "cron" ] || [ "$TRAVIS_EVENT_TYPE" == "api" ]; then

    testsuite_repo_path="/tmp/travis.buid.${TRAVIS_JOB_NUMBER}"
    python_path="export PYTHONPATH=/opt/jumpscale7/lib:/opt/jumpscale7/lib/lib-dynload/:/opt/jumpscale7/bin:/opt/jumpscale7/lib/python.zip:/opt/jumpscale7/lib/plat-x86_64-linux-gnu"

    if [[ ${action} == "before" ]]; then

        echo "[+] Installing travis machine requirements"
        sudo apt install git sshpass -y
        curl -s https://install.zerotier.com/ | sudo bash

        echo "[+] Joining zerotier network : ${zerotier_network}"
        sudo zerotier-cli join ${zerotier_network}; sleep 10

        echo "[+] Authorizing zerotier member"
        memberid=$(sudo zerotier-cli info | awk '{print $3}')
        curl -s -H "Content-Type: application/json" -H "Authorization: Bearer ${zerotier_token}" -X POST -d '{"config": {"authorized": true}}' https://my.zerotier.com/api/network/${zerotier_network}/member/${memberid} > /dev/null
       
        sleep 60

        echo "[+] Cloning G8_testing repo"
        cmd="mkdir ${testsuite_repo_path}; cd ${testsuite_repo_path}; rm -rf G8_testing; git clone -b ${TRAVIS_BRANCH} https://github.com/0-complexity/G8_testing"
        sshpass -p "${ctrl_password}" ssh -t -o StrictHostKeyChecking=no ${ctrl_user}@${ctrl_ipaddress} "${cmd}"

        echo "[+] Install requirements"
        cmd="cd ${testsuite_repo_path}/G8_testing; pip install -r requirements.txt"
        sshpass -p "${ctrl_password}" ssh -t -o StrictHostKeyChecking=no ${ctrl_user}@${ctrl_ipaddress} "${cmd}"

    elif [[ ${action} == "test" ]]; then

        echo "[+] Executing testsuite : ${testsuite_title}"
        cmd="export PYTHONPATH=${python_path}; cd ${testsuite_repo_path}/${testsuite_home_dir}; nosetests -s -v ${testsuite_run_dir} --tc-file config.ini --tc=main.environment:${environment}"
        sshpass -p ${ctrl_password} ssh -t -o StrictHostKeyChecking=no ${ctrl_user}@${ctrl_ipaddress} "${cmd}"

    elif [[ ${action} == "after" ]]; then

        echo "[+] Removing testsuite directory"
        sshpass -p ${ctrl_password} ssh -t -o StrictHostKeyChecking=no ${ctrl_user}@${ctrl_ipaddress} "rm -rf ${testsuite_repo_path}"

    fi

fi