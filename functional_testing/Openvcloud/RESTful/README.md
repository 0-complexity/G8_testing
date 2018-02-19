## OpenvCloud RESTful api  Tests



### Continues Integration

### Travis
You can trigger the build from [Travis website](https://travis-ci.org/0-complexity/G8_testing) or [CI-Dashboard](https://travis-dash.gig.tech/).

#### Prerequisites
Travis CI build uses the environment's controller to execute the tests from it, so if your environment controller doesn't have public ip you have to:
- Install zerotier [ZeroTier](zerotier.com/network) on the controller.
- Create zerotier network and make the controller join it.

#### Travis Parameters
  - ```ctrl_ipaddress```: controller's ip address (zerotier ip in case your using zerotier).
  - ```ctrl_user```: controller's non-root user (default: gig)
  - ```ctrl_user_password```: controller user ssh password.
  - ```restful_ip```: the ip of the api server
  - ```restful_port```: the port of the api server
  - ```username```: [itsyou.online](https://itsyou.online) username
  - ```client_id```: [itsyou.online](https://itsyou.online) client id
  - ```client_secret```: [itsyou.online](https://itsyou.online) client secret  

  - ```jobs```: jobs to be executed (for example ```ovc-restful``` to execute only ovc and restful jobs).
  - ```restful_testsuite_dir```: restful tests path.

  - ##### In case you are using zerotier
    - ```zerotier_network```: zerotier network id.
    - ```zerotier_token```: zerotier account token.

