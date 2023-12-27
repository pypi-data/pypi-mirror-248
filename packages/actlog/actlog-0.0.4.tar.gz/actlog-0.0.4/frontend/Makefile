ECHO=@

build: icons check-block
	@echo Building frontend
	$(ECHO) npm install && npm run build

icons:
	@echo Generating icons
	$(ECHO) npm run icons

check-block:
	@echo Checking for frontend BLOCK-s
	$(ECHO) \
		grep -nr BLOCK src ; \
		if [ $$? = 0 ] ; then \
			echo Saw some BLOCK-s. Failing >&2 ; \
			exit 1 ; \
		fi

clean:
	@echo Cleaning frontend
	$(ECHO) rm -rf frontend node_modules