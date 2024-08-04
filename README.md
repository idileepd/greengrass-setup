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

```