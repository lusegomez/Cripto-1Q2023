PYTHON := $(shell which python3.10 python3 python py | head -n 1)

run:
	$(PYTHON) -c "import pandas" || pip install pandas
	$(PYTHON) -c "import PIL" || pip install pillow
	$(PYTHON) ./main.py $(ARGS)
