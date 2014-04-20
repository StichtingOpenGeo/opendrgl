import backbone

from routes.models import Route


class RouteAPIView(backbone.views.BackboneAPIView):
    model = Route
    display_fields = ('route_id', 'destination')

    def queryset(self, request):
        qry = super(RouteAPIView, self).queryset(request)
        qry.filter(project=request.session.get('project_id', None))
        return qry

backbone.site.register(RouteAPIView)