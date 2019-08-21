from django.db import models
from django.utils import timezone

from db_manager.databases.tasks import pull_database_dump


class Database(models.Model):
    HEROKU_APP = 'HEROKU_APP'
    POSTGRES_DATABASE_URL = 'POSTGRES_DATABASE_URL'

    CONNECTION_TYPE_CHOICES = (
        (POSTGRES_DATABASE_URL, 'postgres:// DATABASE_URL'),
        (HEROKU_APP, 'Heroku app'),
    )

    project_instance = models.ForeignKey('projects.ProjectInstance', models.CASCADE, related_name='databases')
    connection_type = models.CharField(choices=CONNECTION_TYPE_CHOICES, max_length=30)
    connection_value  = models.CharField(max_length=255)

    def __str__(self):
        return "Database"

    def create_dump(self):
        dump = DatabaseDump.objects.create(
            database=self,
            initiated_at=timezone.now()
        )
        pull_database_dump.delay(dump.pk)


    def get_database_url(self):
        if self.connection_type == self.POSTGRES_DATABASE_URL:
            return self.connection_value

        raise NotImplementedError(f'Connection type {self.connection_type} not implemented')


class DatabaseDump(models.Model):
    database = models.ForeignKey('Database', models.PROTECT,
                                 related_name='dumps')
    dump_file = models.FileField(upload_to='database_dumps', blank=True)
    initiated_at = models.DateTimeField(null=True, editable=False)
    finished_at = models.DateTimeField(null=True, editable=False)
    log = models.TextField()
    return_code = models.PositiveIntegerField(null=True, default=None)

    def __str__(self):
        return "database dump"
