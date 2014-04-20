from django.views.generic import TemplateView
from stops.views import EnsureProjectMixin


class RouteAppView(EnsureProjectMixin, TemplateView):
    template_name = 'routes/routes_app.html'