install-requirements:
	pip install -r requirements.txt

run-flask:
	flask --app main.py run --debug -h 0.0.0.0 -p 5000

run-main:
	python main.py
