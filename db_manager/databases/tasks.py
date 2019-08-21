from shutil import rmtree
import os
from tempfile import mkdtemp

from django.utils import timezone

from celery import shared_task

from db_manager.databases.utils import pg_dump


@shared_task
def pull_database_dump(database_dump_pk):
    from db_manager.databases.models import DatabaseDump

    dump = DatabaseDump.objects.get(pk=database_dump_pk)
    dump_dir = mkdtemp()
    dump_path = os.path.join(dump_dir, 'dump.pg')
    result = pg_dump(dump.database.get_database_url(), dump_path)
    dump.log = result['log']
    dump.return_code = result['return_code']
    now = timezone.now()
    if dump.return_code == 0:
        filename = (
            f'{dump.database.project_instance.project.name}_'
            f'{dump.database.project_instance.name}_'
            f'database_dump_{now.strftime("%Y%m%d-%H%M%S")}.pg'
        )
        dump.dump_file.save(filename, open(dump_path, 'rb'), save=False)
    dump.finished_at = now
    dump.save()

    # Clean up the dump from the temporary directory 10 minutes later.
    delete_directory_if_exists.apply_async((dump_dir, ), countdown=10 * 60, max_retries=None)


@shared_task
def delete_directory_if_exists(directory_path):
    if os.path.isdir(directory_path):
        rmtree(directory_path)
