from django.db.models import Q
from chb.models import ChbQuay
from utils.views import TreeNgView


class StopSearchView(TreeNgView):
    model = ChbQuay
    query_slug = 'name'
    related = {'stop': {'fields': ['name', 'city', 'public_code', 'type']}}

    def get_data(self, param):
        return self.model.objects.filter(Q(name__icontains=param) | Q(city__icontains=param))[:10]