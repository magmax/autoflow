from django.shortcuts import render
from django import http
from . import models
from graphviz import Digraph


def status(request, project, status):
    method = dict(
        GET=status_get,
        POST=status_post,
    ).get(request.method)
    if method:
        st, _ = models.Status.objects.get_or_create(name=status)
        prj, _ = models.Project.objects.get_or_create(name=project)
        return method(request, prj, st)
    raise http.Http404(
        "Operation %s not implemented for url %s"
        % (request.method, request.path)
    )


def project(request, project):
    method = dict(
        GET=project_get,
    ).get(request.method)
    if method:
        prj, _ = models.Project.objects.get_or_create(name=project)
        return method(request, prj)
    raise http.Http404(
        "Operation %s not implemented for url %s"
        % (request.method, request.path)
    )


def status_get(request, project, status):
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
        transitions = set()
        if request.GET.get('show_outputs') == 'true':
            for st in status.transition_origin.all():
                render.add_status(st.to_status)
                transitions.add((status, st.to_status))
        if request.GET.get('show_inputs') == 'true':
            for st in status.transition_target.all():
                render.add_status(st.to_status)
                transitions.add((status, st.to_status))
        for st_from, st_to in transitions:
            render.add_transition(st_from, st_to)
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


def status_post(request, project, status):
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


def project_get(request, project):
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

        for transition in project.transition_list.all():
            st_in = transition.from_status
            st_out = transition.to_status
            render.add_status(st_in)
            render.add_status(st_out)
            render.add_transition(st_in, st_out)
        response.write(render.render())
        return response

    return http.JsonResponse(
        dict(
            result='Unknown format',
        )
    )
