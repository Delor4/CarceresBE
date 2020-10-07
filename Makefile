.PHONY: all install run

all:

install:
	pip install -r requirements.txt

run:
	python app.py

init_db:
	python create_db.py
