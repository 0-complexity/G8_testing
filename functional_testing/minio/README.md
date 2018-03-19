## Minio Testsuite

#### Install requirements
```bash
cd G8_testing/functional_testing/minio
pip3 install -r requirements.txt
```

#### Set configuration
```ini
[minio]
url = # url of the minio server (ex: 127.0.0.1:9000)
access_key = # access key
secret_key = # secret key
```

#### Run tests
```bash
cd G8_testing/functional_testing/minio
nosetests -s -v testsuite --tc-file config.ini
```