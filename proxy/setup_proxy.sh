sudo sed -i 's/#$nrconf{restart} = '"'"'i'"'"';/$nrconf{restart} = '"'"'a'"'"';/g' /etc/needrestart/needrestart.conf;
sudo apt update && sudo apt install python3-virtualenv -y
python3 -m virtualenv venv
source venv/bin/activate
pip install -r ~/proxy/requirements.txt
pip install sshtunnel