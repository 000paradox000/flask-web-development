install-requirements:
	pip install -r requirements.txt

run-flask:
	flask --app main.py run --debug -h 0.0.0.0 -p 5000

run-main:
	python main.py

request-headers-with-curl:
	curl http://localhost:5000/headers

request-headers-with-httpie:
	http http://localhost:5000/headers
