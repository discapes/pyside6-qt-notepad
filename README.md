```bash
pipenv install
sudo dnf install python3.11-devel
pipenv shell
pyside6-rcc icons.qrc -o rc_icons.py

python main.py # OR
pyside6-deploy main.py # OR
watchexec -r -e py -- python main.py
```
