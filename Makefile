#######################
# Linting and Testing
#######################

lint:
	make lint-python
	make lint-ui

lint-python:
	make lint-black
	flake8

lint-black:
	black civic_jabber_app --check
	black test_civic_jabber_app --check
	black dags --check

lint-ui:
	cd ui && npx prettier --check .

tidy:
	make tidy-python
	make tidy-ui

tidy-python:
	black civic_jabber_app
	black test_civic_jabber_app
	black dags

tidy-ui:
	cd ui && npx prettier --write .

test:
	pytest test_civic_jabber_app --cov=civic_jabber_app -vv -m "not slow"
	python dags/states.py # Checks to make sure the DAG is valid

################
# Install
################

pip-compile:
	pip-compile requirements/base.in
	pip-compile requirements/dev.in
	pip-compile requirements/test.in

pip-install:
	pip install -r requirements/base.txt
	pip install -r requirements/dev.txt
	pip install -r requirements/test.txt
	pip install -e .

npm-install:
	cd ui && npm install


################
# Run
################

run-ui-local:
	cd ui && npm run start
