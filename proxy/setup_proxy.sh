## This is the file used to successfully set up the proxy instance
## It installs the required dependencies to run the proxy script
## The first command is used to prevent the ubuntu image from asking questions which require UI intervention.
## To successfully install dependencies we used a virtual environment.
sudo sed -i 's/#$nrconf{restart} = '"'"'i'"'"';/$nrconf{restart} = '"'"'a'"'"';/g' /etc/needrestart/needrestart.conf;
sudo apt update && sudo apt install python3-virtualenv -y
python3 -m virtualenv venv
source venv/bin/activate
pip install -r ~/proxy/requirements.txt
pip install sshtunnel
deactivate