FROM python:3
ENV PYTHONUNBUFFERED 1
ADD . .
RUN pip install -r requirements.txt
RUN python manage.py migrate
RUN python manage.py load_gene_location
EXPOSE 5000
CMD ["python", "manage.py", "runserver"]
