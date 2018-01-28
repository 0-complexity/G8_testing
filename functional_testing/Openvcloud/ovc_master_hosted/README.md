## OpenvCloud Functional Tests Hosted on ovc_master

All OpenvCloud functional tests designed to run on ovc_master are documented [here](/docs/functional/openvcloud/ovc_master_hosted/ovc_master_hosted.md).

Below only **internal** documentation please.

## Continues Integration

### Travis

#### Jobs

- ```ovc```: executes tests located in *functional_testing/Openvcloud/ovc_master_hosted/OVC*.
- ```acl```: executes tests located in *functional_testing/Openvcloud/ovc_master_hosted/ACL*.
- ```portal```: executes tests located in *functional_testing/Openvcloud/ovc_master_hosted/Portal*.

### configrations
- ```environment```: environment name (for example: **be-g8-3**).
- ```ctrl_ipaddress```: controller's ip address.
- ```ctrl_root_user```: controller's root user (default: root).
- ```ctrl_user```: controller's non-root user (default: gig)
- ```ctrl_password```: controller ssh password.
- ```jobs```: jobs to be executed (for example ```acl-ovc``` to execute only ovc and acl jobs).
- ```ovc_testsuite_dir```: ovc tests path.
- ```acl_testsuite_dir```: acl tests path.
- ```portal_testsuite_dir```: portal tests path.

#### in case you are using zerotier
- ```zerotier_network```: zerotier network id.
- ```zerotier_token```: zerotier account token.

#### Required for portal job 
- ```portal_admin```: [itsyou.online](itsyou.online) username.
- ```portal_password```: [itsyou.online](itsyou.online) password.
- ```portal_secret```: [itsyou.online](itsyou.online) otp secret.
- ```portal_browser```: web browser to execute portal tests (default: chrome).



### Jenkins
OpenvCloud Testsuite runs continuously on [Jenkins CI](http://ci.codescalers.com/view/Integration%20Testing/)

## Instructions on how to update the coverage documentation

#### Prerequisites

* This instruction works for UNIX-Like operating systems
* Make sure that *pip* and *virtualenv* are installed to your system

    ```shell
    $ sudo apt-get install python-pip
    $ sudo pip install virtualenv
    ```


#### Steps to update

1. Pull the testsuite repository:

  ```
  git clone git@github.com:0-complexity/G8_testing.git
  ```

2. Change directory to Openvcloud:

  ```
  $ cd G8_testing/
  ```

3. Run the build script to generate the documentation locally:

  ```
  $ bash functional_testing/Openvcloud/tools/build_docs.sh
  ```

4. Open the documentation using any browser

  ```
  $ firefox auto_generated_docs/_build/html/index.html
  ```
