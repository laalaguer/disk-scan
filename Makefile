install:
	python3 --version
	python3 -m venv .env && . .env/bin/activate && pip3 install -r requirements.txt