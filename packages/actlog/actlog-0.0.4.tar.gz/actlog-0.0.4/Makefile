ECHO=@

install: frontend-build python-install

venv:
	@echo Creating python virtual environment
	$(ECHO) mkdir venv
	$(ECHO) python3 -m venv venv

python-install: venv
	@echo Installing python files
	$(ECHO) ./venv/bin/pip install '.[dev]'

requirements-that-work:
	@echo Making requirements-that-work.txt
	$(ECHO) ./venv/bin/pip-compile \
		--strip-extras --quiet \
		--output-file requirements-that-work.txt

frontend-build:
	@echo Building frontend
	$(ECHO) $(MAKE) -C frontend build

python-build: check-backend-block python-install
	@echo Building dist
	$(ECHO) rm -rf dist
	$(ECHO) ./venv/bin/python -m build

package: install requirements-that-work frontend-build python-build

check-block: check-backend-block check-frontend-block

check-backend-block:
	 @echo Checking for backend BLOCK-s
	$(ECHO) \
		grep -nr BLOCK src ; \
		if [ $$? = 0 ] ; then \
			echo Saw some BLOCK-s. Failing >&2 ; \
			exit 1 ; \
		fi

check-frontend-block:
	$(ECHO) $(MAKE) -C frontend check-block

clean: clean-backend clean-frontend

clean-backend:
	@echo Cleaning backend
	$(ECHO) rm -rf venv dist

clean-frontend:
	$(ECHO) $(MAKE) -C frontend clean
