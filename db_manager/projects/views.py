from django.views.generic.detail import DetailView
from django.views.generic.list  import ListView

from db_manager.projects.models import Project


class ProjectMixin:
    model = Project


class ProjectListView(ProjectMixin, ListView):
    pass


class ProjectDetailView(ProjectMixin, DetailView):
    slug_field = 'name'

    def get_instances(self):
        return self.object.instances.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['instances'] = self.get_instances()
        return context
