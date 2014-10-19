from django.shortcuts import render
from djangular.views.crud import NgCRUDView
from data.models import TripPattern

class TripPatternView(NgCRUDView):
    model = TripPattern