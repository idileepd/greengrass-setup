# GreenGrass AWS

## Prerequisites
Setup Tokens
```bash
export AWS_ACCESS_KEY_ID=<AWS_ACCESS_KEY_ID>
export AWS_SECRET_ACCESS_KEY=<AWS_SECRET_ACCESS_KEY>
export AWS_SESSION_TOKEN=<AWS_SESSION_TOKEN>
```

Update the system:
```bash 
sudo apt update
sudo apt upgrade
```

Install all (if you are not specific): 
```bash
sudo apt install -y default-jre default-jdk maven python3 python3-pip
```

Install (minimal individually)
```bash 
sudo apt install python3-pip
sudo apt install default-jdk
pip --version
```

Install GDK (Build and deploy components)
```bash 
pip3 install git+https://github.com/aws-greengrass/aws-greengrass-gdk-cli.git@v1.6.2
```
Incase of error installing GDK by extenal package dependency
```bash
cd /home/<user>/.local
# EX:: cd /home/murali/.local
# .venu is env name
python -m venv .venv
source .venv/bin/activate
# EX: source /home/murali/.local/.venv/bin/activate
# MAC: source /Users/dileepnagendra/.local/.venv/bin/activate

pip3 install git+https://github.com/aws-greengrass/aws-greengrass-gdk-cli.git@v1.6.2
gdk --version
deactivate
```

## Setup GreenGrass Core Device
Download installer (This step will be give by aws when adding gg coredevice in aws)
```bash
curl -s https://d2s8p88vqu9w66.cloudfront.net/releases/greengrass-nucleus-latest.zip > greengrass-nucleus-latest.zip && unzip greengrass-nucleus-latest.zip -d GreengrassInstaller
```



## Raspberry config
[Set kernel parameters on a Raspberry Pi](https://docs.aws.amazon.com/greengrass/v2/developerguide/getting-started-set-up-environment.html)
```bash
#1. Open the /boot/cmdline.txt file. This file specifies Linux kernel parameters to apply when the Raspberry Pi boots.
#For example, on a Linux-based system, you can run the following command to use GNU nano to open the file.
sudo nano /boot/cmdline.txt

#2. Verify that the /boot/cmdline.txt file contains the following kernel parameters. The systemd.unified_cgroup_hierarchy=0 parameter specifies to use cgroups v1 instead of cgroups v2.

cgroup_enable=memory cgroup_memory=1 systemd.unified_cgroup_hierarchy=0

#3. If the /boot/cmdline.txt file doesn't contain these parameters, or it contains these parameters with different values, update the file to contain these parameters and values.
# If you updated the /boot/cmdline.txt file, reboot the Raspberry Pi to apply the changes.
sudo reboot
```


Install GreenGrass
```
What below command dees:
1. Provisions the Greengrass core device as an AWS IoT thing with a device certificate and default permissions. Learn more 
2. Creates a system user and group, ggc_user and ggc_group, that the software uses to run components on the device.
3. Connects the device to AWS IoT.
4. Installs and runs the latest AWS IoT Greengrass Core software as a system service.

```
```bash
sudo -E java -Droot="/greengrass/v2" -Dlog.store=FILE -jar ./GreengrassInstaller/lib/Greengrass.jar --aws-region us-east-1 --thing-name GreengrassQuickStartCore-1911de586c8 --thing-group-name GreengrassQuickStartGroup --component-default-user ggc_user:ggc_group --provision true --setup-system-service true --deploy-dev-tools true`
```
(Redable: Just Above cmd cleaned)
```bash
sudo -E java -Droot="/greengrass/v2" -Dlog.store=FILE \
-jar ./GreengrassInstaller/lib/Greengrass.jar \
--aws-region us-east-1 \
--thing-name GreengrassQuickStartCore-1911de586c8 \
--thing-group-name GreengrassQuickStartGroup \
--component-default-user ggc_user:ggc_group \
--provision true \
--setup-system-service true \
--deploy-dev-tools true
```

Optional
```bash
sudo useradd --system --create-home ggc_user
sudo groupadd --system ggc_group
sudo groupadd --system ggc_group
sudo passwd ggc_user
```


## Create a Component 

```bash
# Get all sample repos available
gdk component list --repository
# Get all the templates available
gdk component list --template

# Shows all options to init component
gdk component init --help

gdk component init -n python-example -l python -t HelloWorld
# Update the author and version in python-example/gdk-config.json

cd python-example
# Generate build 
gdk component build

# NOTE:::: create venv for the python project
cd /home/<user>/.local
#EX:  cd /home/murali/.local
python -m venv .greengrass-env

source .greengrass-env/bin/activate
# source /home/murali/.local/.greengrass-env/bin/activate

# To Check all the installed components
sudo /greengrass/v2/bin/greengrass-cli component list

```



### Helper commands

```bash
# to log
sudo tail -f /greengrass/v2/logs/greengrass.log
sudo cat /greengrass/v2/logs/com.example.PythonMqttHello.log
sudo /greengrass/v2/bin/greengrass-cli component list
```