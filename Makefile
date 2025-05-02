install:
	pip3 install -r requirements.txt

run:
	python3 manage.py runserver 0.0.0.0:6424

migrate:
	python3 manage.py makemigrations
	python3 manage.py migrate

shell:
	python3 manage.py shell

start_farms:
	python3 manage.py init_farming

bigbang:
	python3 manage.py bigbang

attack_mission:
	python3 manage.py attack_mission
