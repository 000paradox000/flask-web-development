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

request-request-with-httpie:
	http http://localhost:5000/request

request-redirect-with-httpie:
	http http://localhost:5000/redirect

request-redirect-follow-with-httpie:
	http --follow http://localhost:5000/redirect


shell:
	flask --app main.py shell
