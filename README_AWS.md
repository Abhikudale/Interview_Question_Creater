# How to Deploy Streamlit app on EC2 instance

## 1. Login with your AWS console and launch an EC2 instance

## 2. Run the following commands

### Note: Do the port mapping to this port:- 8501

```bash
sudo apt update
```

```bash
sudo apt-get update
```

```bash
sudo apt upgrade -y
```

```bash
sudo apt install git curl unzip tar make sudo vim wget -y
```

git clone "Your-repository"

```bash
cd
```


```bash
sudo apt install python3-pip
```

Make sure venv is installed by running:

sudo apt install python3-venv
To create a new virtual environment in a directory named .venv, run:

python3 -m venv .venv
To activate this virtual environment (which modifies the PATH environment variable), run this:

source .venv/bin/activate


```bash
pip3 install -r requirements.txt
```

touch .env
vi.env
paste key
then press shift + ! then enter :wq

enter (cat .env) to see contents of the file

For a python file
python3 app.py

```bash
#Temporary running
python3 -m streamlit run app.py
```

```bash
#Permanent running
nohup python3 -m streamlit run app.py
```

Note: Streamlit runs on this port: 8501

