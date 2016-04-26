from django.db import models


class Status(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'status'

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=100)
    current_status = models.ForeignKey(Status, related_name="project_list", blank=True, null=True)

    def __str__(self):
        return self.name


class Transition(models.Model):
    project = models.ForeignKey(Project, related_name="transition_list")
    from_status = models.ForeignKey(Status, related_name="transition_origin")
    to_status = models.ForeignKey(Status, related_name="transition_target")

    def __str__(self):
        return "{p} {f}->{t}".format(f=self.from_status, t=self.to_status, p=self.project)
