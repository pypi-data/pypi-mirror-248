setup:

	@echo "creating directories for tasks, pipes, configs and content ..."
	@mkdir -p ./tasks
	@mkdir -p ./pipes
	@mkdir -p ./configs
	@mkdir -p ./content

	@if [ -e "./config.yaml" ]; then \
	    echo "config.yaml already exists, not overwriting ..."; \
	else \
	    cp config.yaml.in config.yaml; \
		echo "config.yaml created ..."; \
	fi

docs:
	@docop --help > ./documentation/docs/clihelp.txt
	@docop run --help > ./documentation/docs/runhelp.txt
	@echo installing documentation requirements ...
	@pip install -r ./documentation/requirements.txt > /dev/null
	@echo building documentation ...
	@mkdocs build
	@cat ./documentation/docs/example-config.yaml | grep -v "\-\-8<\-\-" > config.yaml.in

	@echo all done.
