from django.urls import path

from db_manager.projects.views import ProjectDetailView, ProjectListView

app_name = 'projects'

urlpatterns = [
    path('<slug:slug>/', ProjectDetailView.as_view(), name='detail'),
    path('', ProjectListView.as_view(), name='list'),
]
