action=${1}
working_path="/tmp/travis_${TRAVIS_BUILD_NUMBER}"
python_path='/opt/jumpscale7/lib:/opt/jumpscale7/lib/lib-dynload/:/opt/jumpscale7/bin:/opt/jumpscale7/lib/python.zip:/opt/jumpscale7/lib/plat-x86_64-linux-gnu'

execute(){
    sshpass -p ${ctrl_password} ssh -t -o StrictHostKeyChecking=no ${ctrl_username}@${ctrl_ipaddress} ${1}
}

execute_as_root(){
    sshpass -p ${ctrl_root_password} ssh -t -o StrictHostKeyChecking=no root@${ctrl_ipaddress} ${1}
}

join_zerotier_network(){
    echo "[+] Joining zerotier network: ${1}"
    sudo zerotier-cli join ${1}; sleep 5
    memberid=$(sudo zerotier-cli info | awk '{print $3}')
    curl -s -H "Content-Type: application/json" -H "Authorization: Bearer ${2}" -X POST -d '{"config": {"authorized": true}}' https://my.zerotier.com/api/network/${1}/member/${memberid} > /dev/null
    # fix for travis - zerotier issue 
    sudo ifconfig "$(ls /sys/class/net | grep zt)" mtu 1280 
}

if [[ ${action} == "setup" ]]; then

    join_zerotier_network ${zerotier_network} ${zerotier_token}

    execute "mkdir -p ${working_path}"
    execute "git clone -b ${TRAVIS_BRANCH} https://github.com/0-complexity/G8_testing ${working_path}/G8_testing"
    execute "chmod -R 777 ${working_path}/G8_testing"
    execute "pip install -r ${working_path}/G8_testing/requirements.txt"
    execute "pip3 install -r ${working_path}/G8_testing/functional_testing/Openvcloud/RESTful/requirements.txt"

elif [[ ${action} == "acl" ]] && echo "${jobs}" | grep -q "acl"; then

    cmd="export PYTHONPATH=${python_path} \; cd ${working_path}/G8_testing/functional_testing/Openvcloud \; nosetests-2.7 -s -v ${acl_testsuite_dir} --tc-file config.ini --tc=main.email:${test_email} --tc=main.email_password:${test_email_password} --tc=main.environment:${environment}"
    execute "${cmd}"

elif [[ ${action} == "ovc" ]] && echo "${jobs}" | grep -q "ovc"; then

    cmd="export PYTHONPATH=${python_path} \; cd ${working_path}/G8_testing/functional_testing/Openvcloud \; nosetests-2.7 -s -v ${ovc_testsuite_dir} --tc-file config.ini --tc=main.email:${test_email} --tc=main.email_password:${test_email_password} --tc=main.environment:${environment}"
    execute_as_root "${cmd}"

elif [[ ${action} == "portal" ]] && echo "${jobs}" | grep -q "portal"; then
    
    cmd="cd ${working_path}/G8_testing \; bash functional_testing/Openvcloud/ovc_master_hosted/Portal/travis_portal_script.sh ${environment} ${portal_admin} ${portal_password} ${portal_secret} ${portal_testsuite_dir} ${portal_browser} ${ctrl_password}"
    execute "${cmd}"

elif [[ ${action} == "restful" ]] && echo "${jobs}" | grep -q "restful"; then

    cmd="cd ${working_path}/G8_testing/functional_testing/Openvcloud/RESTful \; nosetests -s -v ${restful_testsuite_dir} --tc-file config.ini --tc=main.ip:${restful_ip} --tc=main.port:${restful_port} --tc=main.username:${username} --tc=main.client_id:${client_id} --tc=main.client_secret:${client_secret} --tc=main.location:${environment}"
    execute "${cmd}"

else

    echo "======================================== JOB IS SKIPPED =========================================="

fi