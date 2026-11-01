.PHONY: setup run clean

setup:
	dd if=/dev/zero of=dataset.bin bs=1M count=500

run:
	python3 task/agent_manager.py

clean:
	rm -f dataset.bin
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.core" -delete
