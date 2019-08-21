from django.db import models
from django.urls import reverse_lazy


class ProjectInstance(models.Model):
    project = models.ForeignKey('Project', models.CASCADE,
                                related_name='instances')
    name = models.SlugField()

    class Meta:
        unique_together = ('project', 'name', )

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('projects:detail', kwargs={'slug': self.name})
