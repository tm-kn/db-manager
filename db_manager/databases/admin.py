from django.contrib import admin

from db_manager.databases.models import Database, DatabaseDump


@admin.register(Database)
class DatabaseAdmin(admin.ModelAdmin):
    pass


@admin.register(DatabaseDump)
class DatabaseDumpAdmin(admin.ModelAdmin):
    pass
