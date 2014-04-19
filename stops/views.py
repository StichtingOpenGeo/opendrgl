from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from stops.forms import StopForm
from stops.models import Stop
from django.views.generic import ListView, CreateView, View, UpdateView


class EnsureProjectMixin(View):

    def get(self, request, *args, **kwargs):
        if not request.session.get('project_id', False):
            return HttpResponseRedirect(reverse('project_list'))
        return super(EnsureProjectMixin, self).get(request, args, kwargs)

    def get_project(self):
        return self.request.session.get('project_id', None)

class StopIndexView(EnsureProjectMixin, ListView):
    model = Stop

    def get_queryset(self):
        qry = super(StopIndexView, self).get_queryset()
        return qry.filter(project=self.get_project())

class StopCreateView(EnsureProjectMixin, CreateView):
    model = Stop
    form_class = StopForm

    def form_valid(self, form):
        form.instance.project_id = self.get_project()
        return super(StopCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('stop_edit', self.object.pk)

class StopUpdateView(EnsureProjectMixin, UpdateView):
    model = Stop
    form_class = StopForm

    def form_valid(self, form):
        form.instance.project_id = self.get_project()
        return super(StopCreateView, self).form_valid(form)