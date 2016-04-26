from django.shortcuts import render
from . import models


def add_status(request, project, status):
    st, _ = models.Status.objects.get_or_create(name=status)
    prj, _ = models.Project.objects.get_or_create(name=project)

    old_status = prj.current_status
    prj.current_status = st
    prj.save()

    if old_status:
        models.Transition.objects.get_or_create(
            project = prj,
            from_status = old_status,
            to_status = st,
        )
