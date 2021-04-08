sudo apt-get update; sudo apt-get install --no-install-recommends -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
rm -rf /home/baneeishaque/.pyenv
curl https://pyenv.run | bash
exec $SHELL
pyenv install 3.7.10
pyenv global 3.7.10
pip install -r requirements.txt 
git submodule init
git submodule update
