#!/bin/bash
docker run -v./:/app --rm -i ubuntu:jammy << 'EOF'
set -euo pipefail
apt-get update
apt-get install --yes python3 qt6-base-dev
pip install --user pipenv

cd /app
~/.local/bin/pipenv install
~/.local/bin/pipenv run pyside6-deploy main.py
EOF2
EOF

#!/bin/bash
# docker run -v./:/app --rm -i ubuntu:jammy << 'EOF'
# set -euo pipefail
# apt-get update
# apt-get install --yes curl qt6-base-dev cmake build-essential ccache
# curl https://mise.run | sh
# echo 'eval "$(~/.local/bin/mise activate bash)"' >> ~/.bashrc

# bash << 'EOF2'
# mise use --global python@3.11
# pip install --user pipenv

# cd /app
# pipenv install
# pipenv run pyside6-deploy main.py
# EOF2
# EOF

