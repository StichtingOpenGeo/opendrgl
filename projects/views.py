from django.core.urlresolvers import reverse_lazy, reverse
from django.http.response import HttpResponseRedirect
from django.views.generic import ListView, CreateView, RedirectView
from projects.forms import ProjectForm
from projects.models import Project
from utils.forms import BootstrapModelForm


class ProjectListView(ListView):
    model = Project

class ProjectPickView(RedirectView):
    url = reverse_lazy('stop_index')

    def get(self, request, *args, **kwargs):
        if 'pk' not in kwargs:
            return HttpResponseRedirect(reverse('project_pick'))
        # TODO Actually check permissions, bla bla
        request.session['project_id'] = kwargs['pk']
        return super(ProjectPickView, self).get(request, args, kwargs)

class CreateProjectView(CreateView):
    model = Project
    form_class = ProjectForm
    success_url = reverse_lazy('stop_index')