from django.contrib import admin

from db_manager.projects.models import Project, ProjectInstance


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass


@admin.register(ProjectInstance)
class ProjectInstanceAdmin(admin.ModelAdmin):
    pass
