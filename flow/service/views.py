from django.shortcuts import render
from django import http
from . import models
from graphviz import Graph


def add_status(request, project, status):
    method = dict(
        GET=add_status_get,
        POST=add_status_post,
    ).get(request.method)
    if method:
        st, _ = models.Status.objects.get_or_create(name=status)
        prj, _ = models.Project.objects.get_or_create(name=project)
        return method(request, prj, st)
    raise http.Http404(
        "Operation %s not implemented for url %s"
        % (request.method, request.path)
    )


def add_status_get(request, project, status):
    getformat = request.GET.get('format')
    if getformat is None:
        return http.JsonResponse(
            dict(
                result='Not implemented yet',
            )
        )
    if getformat == 'svg':
        response = http.HttpResponse(content_type='image/svg+xml')
        dot = Graph(comment='Status %s in project %s' % (status, project), format='svg')
        if project.current_status.name == status.name:
            dot.attr('node', style='filled', color='yellow')
        dot.node('A', str(project))
        response.write(dot.pipe())
        return response

    return http.JsonResponse(
        dict(
            result='Unknown format',
        )
    )


def add_status_post(request, project, status):
    old_status = project.current_status
    project.current_status = status
    project.save()

    if old_status:
        models.Transition.objects.get_or_create(
            project=project,
            from_status=old_status,
            to_status=status,
        )

    return http.JsonResponse(
        dict(
            result='ok',
        )
    )
