# flexiTests Regression Guidelines
This document describes the process of setting up the Flexiwan Test Automation suite to run in the controlled 
environment . 

Clone the ‘flexiTests’ repository from Gitlab to your Machine where you plan to run the regression. 

https://gitlab.com/flexiwangroup/flexitests

If you are cloning the tests to /root/ then it will be 
` /root/flexitests
`
### Precondition:

**System Requirements:**

    Operating System : Ubuntu Server 18.04.5 LTS.
    Processor (CPU)  : 1 or 2 CPU cores minimum. 64-bit CPU required, Intel or AMD.
    Memory (RAM)     : 4GB RAM minimum
    HDD (Storage)    : 30GB disk size minimum.

**Packages Requirements:**

There are certain preconditions which we need to take into consideration before start running 
the automated regression suite. We need to install the below packages to satisfy the precondition requirements. 

If you check out the latest changes from the ‘flexitests’ branch there will be a file ‘auto-install.sh’ file 
which you can execute by using ‘sh auto-install.sh’ command and follow the instruction, which will 
install all the required packages to satisfy the precondition requirement as shown below. 

**For Ubuntu & Debian Machines**

    root@tec:~/flexitests# pwd
    /root/flexitests

    root@tec:~/flexitests# sh autoinstall.sh
    Do you proceed with the installation?
    yes
    You Answered, yes
    Proceeding with the Installation... Following packages will be installed
    build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget libbz2-dev python3.8 unzip xvfb libxi6 libgconf-2-4 software-properties-common google-chrome-stable python3-pip python3-venv
    Hit:1 http://in.archive.ubuntu.com/ubuntu bionic InRelease
    Get:2 http://in.archive.ubuntu.com/ubuntu bionic-updates InRelease [88.7 kB]
    Ign:3 https://pkg.jenkins.io/debian-stable binary/ InRelease
    Hit:4 https://pkg.jenkins.io/debian-stable binary/ Release
    Get:5 http://dl.google.com/linux/chrome/deb stable InRelease [1,811 B]
    Get:6 http://security.ubuntu.com/ubuntu bionic-security InRelease [88.7 kB]
    Get:7 http://in.archive.ubuntu.com/ubuntu bionic-backports InRelease [74.6 kB]
    Get:9 http://dl.google.com/linux/chrome/deb stable/main amd64 Packages [1,067 B]
    Get:10 http://in.archive.ubuntu.com/ubuntu bionic-updates/main amd64 Packages [1,912 kB]
    Get:11 http://in.archive.ubuntu.com/ubuntu bionic-updates/main i386 Packages [1,228 kB]
    Get:12 http://security.ubuntu.com/ubuntu bionic-security/universe i386 Packages [979 kB]
    Get:13 http://in.archive.ubuntu.com/ubuntu bionic-updates/universe amd64 Packages [1,719 kB]
    Get:14 http://in.archive.ubuntu.com/ubuntu bionic-updates/universe i386 Packages [1,561 kB]
    Get:15 http://security.ubuntu.com/ubuntu bionic-security/universe amd64 Packages [1,113 kB]
    Fetched 8,767 kB in 5s (1,695 kB/s)
    Reading package lists... Done
    Building dependency tree
    Reading state information... Done
    14 packages can be upgraded. Run 'apt list --upgradable' to see them.
    Reading package lists... Done
    Building dependency tree
    Reading state information... Done
    build-essential is already the newest version (12.4ubuntu1).
    libffi-dev is already the newest version (3.2.1-8).
    libgdbm-dev is already the newest version (1.14.1-6).
    libreadline-dev is already the newest version (7.0-3).
    libxi6 is already the newest version (2:1.7.9-1).
    zlib1g-dev is already the newest version (1:1.2.11.dfsg-0ubuntu2).
    libgconf-2-4 is already the newest version (3.2.6-4ubuntu1).
    libbz2-dev is already the newest version (1.0.6-8.1ubuntu0.2).
    libncurses5-dev is already the newest version (6.1-1ubuntu1.18.04).
    libnss3-dev is already the newest version (2:3.35-2ubuntu2.12).
    libsqlite3-dev is already the newest version (3.22.0-1ubuntu0.4).
    libssl-dev is already the newest version (1.1.1-1ubuntu2.1~18.04.8).
    software-properties-common is already the newest version (0.96.24.32.14).
    unzip is already the newest version (6.0-21ubuntu1.1).
    wget is already the newest version (1.19.4-1ubuntu2.2).
    python3-pip is already the newest version (9.0.1-2.3~ubuntu1.18.04.4).
    python3-venv is already the newest version (3.6.7-1~18.04).
    python3.8 is already the newest version (3.8.0-3~18.04.1).
    xvfb is already the newest version (2:1.19.6-1ubuntu4.8).
    google-chrome-stable is already the newest version (89.0.4389.82-1).
    0 upgraded, 0 newly installed, 0 to remove and 14 not upgraded.
    /usr/bin/python: No module named pip

    Proceeding with Chrome driver Installation
    --2021-03-12 17:12:26--  https://chromedriver.storage.googleapis.com/2.41/chromedriver_linux64.zip
    Resolving chromedriver.storage.googleapis.com (chromedriver.storage.googleapis.com)... 172.217.163.176, 2404:6800:4007:80f::2010
    Connecting to chromedriver.storage.googleapis.com (chromedriver.storage.googleapis.com)|172.217.163.176|:443... connected.
    HTTP request sent, awaiting response... 200 OK
    Length: 3944714 (3.8M) [application/zip]
    Saving to: ‘chromedriver_linux64.zip’
    
    chromedriver_linux64.zip                            100%[===================================================================================================================>]   3.76M  3.04MB/s    in 1.2s
    
    2021-03-12 17:12:28 (3.04 MB/s) - ‘chromedriver_linux64.zip’ saved [3944714/3944714]
    
    Archive:  chromedriver_linux64.zip
      inflating: chromedriver
    Proceeding with Gecko Driver Installation
    --2021-03-12 17:12:28--  https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz
    Resolving github.com (github.com)... 140.82.114.3
    Connecting to github.com (github.com)|140.82.114.3|:443... connected.
    HTTP request sent, awaiting response... 302 Found
    Location: https://github-releases.githubusercontent.com/25354393/5c569480-ed2d-11e9-9cc4-fc5d37f5f932?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20210312%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20210312T114046Z&X-Amz-Expires=300&X-Amz-Signature=7c1861a87946e158f0d0793609f8578618326b816e74ec2d3402deacdb5239a6&X-Amz-SignedHeaders=host&actor_id=0&key_id=0&repo_id=25354393&response-content-disposition=attachment%3B%20filename%3Dgeckodriver-v0.26.0-linux64.tar.gz&response-content-type=application%2Foctet-stream [following]
    --2021-03-12 17:12:29--  https://github-releases.githubusercontent.com/25354393/5c569480-ed2d-11e9-9cc4-fc5d37f5f932?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20210312%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20210312T114046Z&X-Amz-Expires=300&X-Amz-Signature=7c1861a87946e158f0d0793609f8578618326b816e74ec2d3402deacdb5239a6&X-Amz-SignedHeaders=host&actor_id=0&key_id=0&repo_id=25354393&response-content-disposition=attachment%3B%20filename%3Dgeckodriver-v0.26.0-linux64.tar.gz&response-content-type=application%2Foctet-stream
    Resolving github-releases.githubusercontent.com (github-releases.githubusercontent.com)... 185.199.109.154, 185.199.111.154, 185.199.110.154, ...
    Connecting to github-releases.githubusercontent.com (github-releases.githubusercontent.com)|185.199.109.154|:443... connected.
    HTTP request sent, awaiting response... 200 OK
    Length: 2390549 (2.3M) [application/octet-stream]
    Saving to: ‘geckodriver-v0.26.0-linux64.tar.gz’
    
    geckodriver-v0.26.0-linux64.tar.gz                  100%[===================================================================================================================>]   2.28M  4.48MB/s    in 0.5s
    
    2021-03-12 17:12:30 (4.48 MB/s) - ‘geckodriver-v0.26.0-linux64.tar.gz’ saved [2390549/2390549]
    
    geckodriver
    Proceeding with Firefox Driver Installation
    --2021-03-12 17:12:30--  https://ftp.mozilla.org/pub/firefox/releases/66.0.3/linux-x86_64/en-US/firefox-66.0.3.tar.bz2
    Resolving ftp.mozilla.org (ftp.mozilla.org)... 52.84.6.117, 52.84.6.82, 52.84.6.17, ...
    Connecting to ftp.mozilla.org (ftp.mozilla.org)|52.84.6.117|:443... connected.
    HTTP request sent, awaiting response... 200 OK
    Length: 61994174 (59M) [application/x-tar]
    Saving to: ‘firefox-66.0.3.tar.bz2’
    
    firefox-66.0.3.tar.bz2                              100%[===================================================================================================================>]  59.12M  3.27MB/s    in 18s
    
    2021-03-12 17:12:49 (3.26 MB/s) - ‘firefox-66.0.3.tar.bz2’ saved [61994174/61994174]
    
    Successfully completed the installation


### How to Install Chrome Driver:

    wget https://chromedriver.storage.googleapis.com/2.41/chromedriver_linux64.zip
    unzip chromedriver_linux64.zip
    sudo mv chromedriver /usr/bin/chromedriver
    sudo chown root:root /usr/bin/chromedriver
    sudo chmod +x /usr/bin/chromedriver
    sudo rm -fr chromedriver_linux64.zip

### How to Install Gecko Driver:

    wget https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz
    tar xvzf geckodriver-v0.26.0-linux64.tar.gz
    sudo chmod 777 geckodriver
    sudo mv geckodriver /usr/bin/

### How to install firefox Driver:
     wget https://ftp.mozilla.org/pub/firefox/releases/66.0.3/linux-x86_64/en-US/firefox-66.0.3.tar.bz2
     tar -xjf firefox-66.0.3.tar.bz2
     sudo rm -rf /opt/firefox
     sudo mv firefox/ /opt
     sudo mv /usr/bin/firefox /usr/bin/firefox_old
     sudo ln -s /opt/firefox/firefox /usr/bin/firefox

### How to create Virtual Environment:
We need to create a virtual environment to run the test inside it. 

Go to ‘/root/’ or ‘/home/ubuntu’ and create the virtual environment

    sudo python3.8 -m venv <venv_name>
    source /root/<venv_name>/bin/activate
    cd /root/flexitests/
    python3.8 -m pip install -r requirements.txt 

As per the above command we are setting up the virtual environment to run our automated test and 
installing the required packages via requirements.txt file 

    PyNaCl>=1.4.0
    astroid>=2.5
    atomicwrites>=1.4.0
    attrs>=20.3.0
    bcrypt>=3.2.0
    certifi>=2020.12.5
    cffi>=1.14.5
    chardet>=4.0.0
    colorama>=0.4.4
    cryptography>=3.4.6
    idna>=2.10
    iniconfig>=1.1.1
    isort>=5.7.0
    lazy-object-proxy>=1.5.2
    mccabe>=0.6.1
    packaging>=20.9
    paramiko>=2.7.2
    pip>=21.0.1
    pluggy>=0.13.1
    py>=1.10.0
    pycparser>=2.20
    pylint>=2.7.1
    pyparsing>=2.4.7
    pytest>=6.2.2
    requests>=2.25.1
    selenium>=3.141.0
    setuptools>=53.0.0
    six>=1.15.0
    toml>=0.10.2
    urllib3>=1.26.3
    wrapt>=1.12.1
    PyJWT>=2.0.1

## How to create 3-site topology using flexitest 

### Precondition to create 3-site topology in KVM

Before creating topology we need to create KVM hypervisor, We can create KVM hypervisor in below mentioned ways
    1. Create a Hypervisor in Virtual Box/ESXi in private infrastructure
    2. Create a Hypervisor in Cloud infrastructure using GCP 

As of now we have automated the topology creation in GCP environment for 3-site. 

Following is the command to create 3-site topology in KVM hypervisor in Nested Environment. 

    sudo python flexitest.py build kvm -s <kvm hypervisor ip> -u <ssh_username> -k <ssh_key_file> -ev <release_version> -r <repository> -m <management_ip> -tk <token of organization> -ak <access key of the organization>

## How to Start the automated regression:

Once all the installation is done on the TEC machine, now the machine is ready to trigger the automated 
regression suites on the targeted test bed. 
We need to create the testbed if not already there and capture the device details in to the JSON formatted 
file under 'users' directory

    root@tec:~/flexitests# pwd
    /root/flexitests
    root@tec:~/flexitests# ls
        autoinstall.sh  common  conftest.py  LICENSE  pageObjects  __pycache__  pytest.ini  README.md  requirements.txt  results  start.py  tests  users  utils
    root@tec:~/flexitests# python3 start.py --setup=users/regression/3-site.json 

Once the test is started, the LOGS were logged under 'results' folder which is automatically created under 'flexitests'
folder. We can tail the logs to check the progress of test case execution. 
