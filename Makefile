.PHONY: init run test build clean

init:
	pip install -r requirements.txt

run:
	PYTHONPATH=$(PWD) python src/api/app.py

test:
	PYTHONPATH=$(PWD) python -m unittest discover tests

build:
	docker build -t health-calculator-service .

clean:
	rm -rf __pycache__ src/**/__pycache__ tests/__pycache__
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
