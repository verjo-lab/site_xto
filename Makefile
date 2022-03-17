migrate:
	python manage.py migrate

migrations:
	python manage.py makemigrations

run:
	python manage.py runserver

load:
	python manage.py load_gene_location
	python manage.py load_smps
	python manage.py load_schistocyte_data
	python manage.py load_clusters_data