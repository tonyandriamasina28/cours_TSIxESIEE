.PHONY: venv run-queue run-zerocopy clean

venv:
	python3 -m venv venv --without-pip
	curl -sS https://bootstrap.pypa.io/get-pip.py | venv/bin/python
	./venv/bin/pip install -r requirements.txt

run-queue: venv
	./venv/bin/python task/queue_benchmark.py

run-zerocopy: venv
	./venv/bin/python task/zerocopy_manager.py

clean:
	rm -rf venv/
	find . -type d -name "__pycache__" -exec rm -rf {} +
