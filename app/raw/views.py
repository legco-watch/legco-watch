from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView
from raw.models import RawCouncilAgenda


class RawCouncilAgendaListView(ListView):
    model = RawCouncilAgenda
    template_name = 'raw/agenda_list.html'
    paginate_by = 25
