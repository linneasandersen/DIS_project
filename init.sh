cd src
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=run.py
