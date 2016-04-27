from django.shortcuts import render
from django import http
from . import models
from graphviz import Digraph


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
        render = RenderSvg(project, 'Status %s in project %s' % (status, project))
        response = http.HttpResponse(content_type=render.mime)
        render.add_status(status)
        for st in status.transition_origin.all():
            render.add_status(st.to_status)
            render.add_transition(status, st.to_status)
        response.write(render.render())
        return response

    return http.JsonResponse(
        dict(
            result='Unknown format',
        )
    )

class RenderSvg(object):
    def __init__(self, project, comment):
        self.project = project
        self.dot = Digraph(comment=comment, format='svg')

    def add_status(self, status, mark=False):
        if self.project.current_status.name == status.name:
            self.dot.node(status.name, status.name, style='filled', color='yellow')
        else:
            self.dot.node(status.name, status.name)

    def add_transition(self, from_status, to_status):
        self.dot.edge(from_status.name, to_status.name)

    def render(self):
        return self.dot.pipe()

    @property
    def mime(self):
        return 'image/svg+xml'

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
