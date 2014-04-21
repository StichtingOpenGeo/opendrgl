import backbone
from django.forms import ModelForm

from routes.models import Route


class RouteAPIView(backbone.views.BackboneAPIView):
    model = Route
    display_fields = ('route_id', 'destination')

    def queryset(self, request):
        qry = super(RouteAPIView, self).queryset(request)
        qry.filter(project=request.session.get('project_id', None))
        return qry

    def get_form_instance(self, request, data=None, instance=None):
        form = super(RouteAPIView, self).get_form_instance(request, data=data, instance=instance)
        # Get the form and inject our extra data
        form.data['project'] = request.session.get('project_id', None)
        return form


backbone.site.register(RouteAPIView)