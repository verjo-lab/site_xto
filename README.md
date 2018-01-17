# Schisto LincRNA Database

## How to develop for the Schisto LincRNA Database

```bash
mkvirtualenv site_xto -p python3
pip install -r requirements.txt
cd site_xto
python manage.py migrate
python manage.py createsuperuser
python manage.py load_gene_location
```