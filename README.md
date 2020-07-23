# Usage
```
usage: srr_check [-h] [-v] [-c] [-f] path

Compare a release against srrDB

positional arguments:
  path             path to release

optional arguments:
  -h, --help       show this help message and exit
  -v, --verbose    verbose output
  -c, --crc-check  Compare crc checksums
  -f, --fix        Try to download mismatched nfo,sfv,jpg from srrDB
  ```
  
# Installation (Ubuntu 20.04)
```
apt update
apt install python3 python3-setuptools git
git clone https://github.com/lillmumriken/srr_check.git
cd srr_check
python3 setup.py develop
```
