action=$1

if [ "$TRAVIS_EVENT_TYPE" == "cron" ] || [ "$TRAVIS_EVENT_TYPE" == "api" ]; then

    testsuite_repo_path="/tmp/travis.build.${TRAVIS_JOB_NUMBER}"

    if [[ ${action} == "before" ]]; then

        echo "[+] Joining zerotier network : ${zerotier_network}"
        sudo zerotier-cli join ${zerotier_network}; sleep 20

        echo "[+] Authorizing zerotier member"
        memberid=$(sudo zerotier-cli info | awk '{print $3}')
        curl -s -H "Content-Type: application/json" -H "Authorization: Bearer ${zerotier_token}" -X POST -d '{"config": {"authorized": true}}' https://my.zerotier.com/api/network/${zerotier_network}/member/${memberid} > /dev/null
       
        sleep 50

        echo "[+] Cloning G8_testing repo"
        cmd="mkdir ${testsuite_repo_path}; cd ${testsuite_repo_path}; rm -rf G8_testing; git clone -b ${TRAVIS_BRANCH} https://github.com/0-complexity/G8_testing; chown -R ${ctrl_user}:${ctrl_user} ."
        sshpass -p "${ctrl_root_password}" ssh -t -o StrictHostKeyChecking=no ${ctrl_root_user}@${ctrl_ipaddress} "${cmd}"

        echo "[+] Install requirements"
        cmd="cd ${testsuite_repo_path}/G8_testing; pip install -r requirements.txt"
        sshpass -p "${ctrl_root_password}" ssh -t -o StrictHostKeyChecking=no ${ctrl_root_user}@${ctrl_ipaddress} "${cmd}"

    elif [[ ${action} == "test" ]]; then

        testsuite=${2}
        testsuite_path=${3}
        python_path="/opt/jumpscale7/lib:/opt/jumpscale7/lib/lib-dynload/:/opt/jumpscale7/bin:/opt/jumpscale7/lib/python.zip:/opt/jumpscale7/lib/plat-x86_64-linux-gnu"
    
        if echo "${jobs}" | grep -q "${testsuite}"; then

            echo "[+] Executing testsuite: ${testsuite}, from path: ${testsuite_path}"

            if [[ "${testsuite}" == "acl" || "${testsuite}" == "ovc" ]]; then

                cmd="export PYTHONPATH=${python_path}; cd ${testsuite_repo_path}/G8_testing/functional_testing/Openvcloud; nosetests-2.7 -s -v ${testsuite_path} --tc-file config.ini --tc=main.email:${test_email} --tc=main.email_password:${test_email_password} --tc=main.environment:${environment}"
                sshpass -p ${ctrl_root_password} ssh -t -o StrictHostKeyChecking=no ${ctrl_root_user}@${ctrl_ipaddress} "${cmd}"

            elif [[ "${testsuite}" == "restful" ]]; then

                echo "[+] Install requirements"
                cmd="cd ${testsuite_repo_path}/G8_testing/functional_testing/Openvcloud/RESTful; pip3 install -r requirements.txt"
                sshpass -p "${ctrl_root_password}" ssh -t -o StrictHostKeyChecking=no ${ctrl_root_user}@${ctrl_ipaddress} "${cmd}"

                cmd="cd ${testsuite_repo_path}/G8_testing/functional_testing/Openvcloud/RESTful; nosetests -s -v ${testsuite_path} --tc-file config.ini --tc=main.ip:${restful_ip} --tc=main.port:${restful_port} --tc=main.username:${username} --tc=main.client_id:${client_id} --tc=main.client_secret:${client_secret} --tc=main.location:${environment}"
                sshpass -p ${ctrl_user_password} ssh -t -o StrictHostKeyChecking=no ${ctrl_user}@${ctrl_ipaddress} "${cmd}"

            elif [[ "${testsuite}" == "portal" ]]; then

                cmd="cd ${testsuite_repo_path}/G8_testing; bash functional_testing/Openvcloud/ovc_master_hosted/Portal/travis_portal_script.sh ${environment} ${portal_admin} ${portal_password} ${portal_secret} ${testsuite_path} ${portal_browser} ${ctrl_user_password}"
                sshpass -p "${ctrl_user_password}" ssh -t -o StrictHostKeyChecking=no ${ctrl_user}@${ctrl_ipaddress} "${cmd}"

            fi

        else
            echo "======================================== JOB IS SKIPPED =========================================="
        fi

    elif [[ ${action} == "after" ]]; then

        echo "[+] Removing testsuite directory"
        sshpass -p ${ctrl_root_password} ssh -t -o StrictHostKeyChecking=no ${ctrl_root_user}@${ctrl_ipaddress} "rm -rf ${testsuite_repo_path}"

    fi

fi