from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView
from raw.models import RawCouncilAgenda


class RawCouncilAgendaListView(ListView):
    model = RawCouncilAgenda
    template_name = 'raw/agenda_list.html'
    paginate_by = 25


class RawCouncilAgendaDetailView(DetailView):
    model = RawCouncilAgenda
    template_name = 'raw/agenda_detail.html'

    def get_context_data(self, **kwargs):
        context = super(RawCouncilAgendaDetailView, self).get_context_data(**kwargs)
        context['parser'] = self.object.get_parser()
        return context
