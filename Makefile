# Vince is not a make wizard.

help:
	@echo "Targets: help, clean, wipedb"


clean:
	# Tox creates virtualenvs for every test scenario
	-[ -e .tox ] && rm -r .tox

	# Python 3 places compiled files in a subdir
	-find . -name __pycache__ -print0 | xargs -0 rm -r

	# Python 2 places compiled files next to the source
	-find . -name *.py[co] -print0 | xargs -0 rm -f

	# pip caches wheels in addition to source downloads. This can create pain if
	# you upgrade a binary library like libmysqlclient.
	-[ -d ~/.cache/pip ] && rm -r ~/.cache/pip
	-[ -d ~/Library/Caches/pip ] && rm -r ~/Library/Caches/pip


# TEMPORARY while noodling on database schema. Quick reset to empty.
wipedb: clean
	rm -f db.sqlite3
	rm -f worlds/migrations/0*
	python manage.py makemigrations
	python manage.py migrate
	python manage.py createsuperuser --username=vince --email="vince@veselosky.me"
	# Will prompt for password