migrate:
	python manage.py migrate

migrations:
	python manage.py makemigrations

run:
	python manage.py migrate
	python manage.py load_gene_location
	python manage.py load_smps
	python manage.py load_schistocyte_data
	python manage.py load_clusters_data
	python manage.py link_clusters_data
	python manage.py runserver 0.0.0.0:8000

load:
	python manage.py load_gene_location
	python manage.py load_smps
	python manage.py load_schistocyte_data
	python manage.py load_clusters_data
	python manage.py link_clusters_data