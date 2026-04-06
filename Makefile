.PHONY: install test benchmark benchmark-cmu clean

PYTHON ?= python3
CODE_DIR := code

install:
	cd $(CODE_DIR) && $(PYTHON) -m pip install -e ".[dev]"

test:
	cd $(CODE_DIR) && $(PYTHON) -m pytest tests -q

benchmark:
	cd $(CODE_DIR) && $(PYTHON) scripts/gate_c_benchmarks.py

benchmark-cmu:
	cd $(CODE_DIR) && $(PYTHON) scripts/benchmark_cmu.py

clean:
	rm -rf $(CODE_DIR)/build $(CODE_DIR)/dist $(CODE_DIR)/*.egg-info
