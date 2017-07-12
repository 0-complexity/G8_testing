## 0-Orchestrator Testsuite

#### Clone this repo 
```bash
git clone https://github.com/0-complexity/G8_testing
```
#### Install requirements
```bash
cd G8_testing/functional_testing/Grid_API_Testing/
pip3 install -r requirements.txt
```
#### Set your configrations
```ini
[main]
api_base_url = #the url of the Zero-OS Cluste
zerotier_token = #zerotier account token
client_id = #itsyouonline account client id
client_secret = #itsyouonline account client secret
organization = #itsyouonline organization

```
> [See how to setup a Zero-OS Cluste](https://github.com/zero-os/0-orchestrator/tree/master/docs/setup)


#### Run tests
```bash
cd G8_testing/functional_testing/Grid_API_Testing/
export PYTHONPATH=./
nosetests -s -v api_testing/testcases --tc-file api_testing/config.ini
```