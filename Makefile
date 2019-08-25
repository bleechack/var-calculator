RUNTEST=python -m unittest discover -p "*_test.py"

test: .PHONY
	$(RUNTEST) lib
	$(RUNTEST) bin

clean:
	rm -rf *.pyc .DS_Store

tidy:
	find . -name '*.py' -maxdepth 1 -exec pythontidy {} {} \;

lint:
	pylint lib/*.py bin/*.py

.PHONY:
