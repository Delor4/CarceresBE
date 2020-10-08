
CMDS = help install run init_db

.PHONY: $(CMDS)

help:
	@echo Possible targets: $(CMDS)

install:
	pip install -r requirements.txt

run:
	python app.py

init_db:
	python create_db.py

