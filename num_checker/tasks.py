import csv
import logging

from django.core.files.base import File

from config.celery import app

from .filemanager import FileManager
from .models import FileExtract, Registry


@app.task
def register_files():
    filemanager = FileManager()
    try:
        if filemanager.remove_files_from_media():
            FileExtract.objects.all().delete()
            files_data = filemanager.create_files()

            for file_name, code in files_data:
                with open(file_name, 'rb') as file:
                    FileExtract.objects.create(
                        code=int(code),
                        file=File(file)
                    )
                filemanager.remove_file(file_name)
        update_files.delay()
    
    except Exception as err:
        logging.info(f'error - {str(err)}')


@app.task
def registry_get_updates(file_pk: int):
    record_list = list()
    file_obj = FileExtract.objects.get(pk=file_pk)

    with open(file_obj.file.path, 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            try:
                row = row[0].split(';')
                record = {
                    'file_id': file_obj.pk,
                    'code': int(row[0]),
                    'range_from': int(row[1]),
                    'range_to': int(row[2]),
                    'capacity': int(row[3]),
                    'operator': row[4],
                    'region': row[5],
                    'inn': int(row[6]),
                }
                record_list.append(Registry(**record))

            except Exception as err:
                logging.info(f'error - {str(err)}')

    if len(record_list):
        Registry.objects.bulk_create(record_list)


@app.task
def update_files():
    for file in FileExtract.objects.all():
        registry_get_updates.delay(file.pk)
