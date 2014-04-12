from django.shortcuts import render
from stops.models import Stop
from django.views.generic import ListView, CreateView


class StopIndexView(ListView):
    model=Stop

    def get_queryset(self):
        qry = super(StopIndexView, self).get_queryset()
        #return qry.filter(project=self.request.current_project)
        return qry

class StopCreateView(CreateView):
    model=Stop
