# Setup

```bash
pyenv install 3.10
PYENV_VERSION=3.10 && pyenv global 3.10 && pyenv local 3.10 && python --version
rm -rf venv && python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install psycopg2-binary
```
