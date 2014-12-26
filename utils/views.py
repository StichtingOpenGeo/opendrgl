from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django.http import Http404
from django.views.generic import DetailView
from djangular.views.crud import NgCRUDView
from preserialize.serialize import serialize

__author__ = 'Joel Haasnoot'


class BaseNgView(NgCRUDView, DetailView):
    query_slug = None

    def dispatch(self, request, *args, **kwargs):
        if self.query_slug is None:
            raise ImproperlyConfigured("No query slug")
        if self.query_slug not in self.request.GET:
            raise Http404
        try:
            data = self.get_data(self.request.GET[self.query_slug])
            return self.build_json_response(data)
        except ObjectDoesNotExist:
            raise Http404

class TreeNgView(BaseNgView):
    """
    Add support for serializing with one or more relations
    """
    relations = {}

    def serialize_queryset(self, queryset):
        """
        Return serialized queryset or single object as python dictionary
        """
        return serialize(queryset, fields=self.get_fields(), related=self.related)