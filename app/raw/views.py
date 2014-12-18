import inspect
from django.db.models import get_model
from django.forms import ModelForm
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, FormView, TemplateView
from django.views.generic.detail import BaseDetailView
from django.views.generic.edit import FormMixin
from raw import models
from raw.forms import OverrideForm
from raw.models import RawCouncilAgenda, RawMember, RawCommittee, Override
from raw.names import NameMatcher, MemberName


class RawCouncilAgendaListView(ListView):
    model = RawCouncilAgenda
    template_name = 'raw/agenda_list.html'
    paginate_by = 25


class RawCouncilAgendaDetailView(DetailView):
    model = RawCouncilAgenda
    slug_field = 'uid'
    template_name = 'raw/agenda_detail.html'

    def get_context_data(self, **kwargs):
        context = super(RawCouncilAgendaDetailView, self).get_context_data(**kwargs)
        parser = self.object.get_parser()
        context['parser'] = parser
        matcher = RawMember.get_matcher()
        questions = []
        if parser.questions is not None:
            for q in parser.questions:
                name = MemberName(q.asker)
                match = matcher.match(name)
                obj = (q, match)
                questions.append(obj)
        context['questions'] = questions
        return context


class RawCouncilAgendaSourceView(BaseDetailView):
    model = RawCouncilAgenda
    slug_field = 'uid'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return HttpResponse(self.object.get_source())


class RawMemberListView(ListView):
    model = RawMember
    template_name = 'raw/member_list.html'
    paginate_by = 25


class RawMemberDetailView(DetailView):
    model = RawMember
    template_name = 'raw/member_detail.html'

    def get_context_data(self, **kwargs):
        context = super(RawMemberDetailView, self).get_context_data(**kwargs)
        fields = ['gender', 'year_of_birth', 'place_of_birth', 'homepage']
        context['fields'] = []
        for f in fields:
            res = {'label': f, 'value': getattr(self.object, f, '')}
            context['fields'].append(res)

        questions = self.object.raw_questions.filter(language=models.LANG_EN)
        questions_with_dates = sorted([(xx, xx.date) for xx in questions], key=lambda x: x[1])
        context['questions'] = [xx for xx, dd in questions_with_dates]
        return context


class RawCommitteeListView(ListView):
    model = RawCommittee
    template_name = 'raw/committee_list.html'
    paginate_by = 25


class RawCommitteeDetailView(DetailView):
    model = RawCommittee
    template_name = 'raw/committee_detail.html'


class ParsedModelListView(TemplateView):
    template_name = 'raw/parsedmodel_list.html'

    def get_context_data(self, **kwargs):
        context = super(ParsedModelListView, self).get_context_data(**kwargs)
        # Dynamically generate the list of models we're interested in
        parsed_models = [xx[1] for xx in inspect.getmembers(models.parsed, inspect.isclass)
                         if issubclass(xx[1], models.BaseParsedModel) and not xx[1] == models.BaseParsedModel]
        context['models'] = sorted(
            [{'name': xx._meta.verbose_name.capitalize(), 'path': xx._meta.model_name} for xx in parsed_models],
            key=lambda x: x['path']
        )
        return context


class ParsedModelInstanceList(ListView):
    template_name = 'raw/parsedmodel_instance_list.html'
    paginate_by = 25

    def get_model(self):
        model_name = self.kwargs['model']
        mdl = get_model('raw', model_name)
        return mdl

    def get_queryset(self):
        # Get the model and all the items
        mdl = self.get_model()
        return mdl.objects.all()

    def get_context_data(self, **kwargs):
        context = super(ParsedModelInstanceList, self).get_context_data(**kwargs)
        context['model'] = self.get_model()
        context['model_name'] = context['model']._meta.verbose_name.capitalize()
        context['path'] = self.kwargs['model']
        return context


class ParsedModelDetailView(TemplateView):
    template_name = 'raw/parsedmodel_detail.html'

    def __init__(self, *args, **kwargs):
        super(ParsedModelDetailView, self).__init__(*args, **kwargs)
        self._model_instance = None

    def get_initial(self):
        pass

    def get_form_kwargs(self):
        kwargs = {
            'initial': self.get_initial(),
            'prefix': 'override',
        }

        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def get(self, request, *args, **kwargs):
        # Check if an override exists.  If it does, load it and use its data to populate the form
        # Get the form
        override = self.get_override()
        model_instance = self.get_model_instance()
        if override is None:
            form = OverrideForm.from_model(model_instance, {'prefix' :'override'})
            return self.render_to_response(self.get_context_data(form=form))
        else:
            pass
            # return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        pass

    def get_model_class(self):
        # Gets the model class that we're currently viewing
        model_name = self.kwargs['model']
        mdl = get_model('raw', model_name)
        return mdl

    def get_model_instance(self):
        # Gets the instance of the model class that we're viewing
        if self._model_instance is None:
            self._model_instance = self.get_model_class().objects.get(uid=self.kwargs['uid'])
        return self._model_instance

    def get_override(self):
        # Tries to get the Override instance for the model
        instance = self.get_model_instance()
        return Override.objects.get_from_reference(instance)

    def get_fields_from_model(self, model):
        res = []
        for field in model._meta.fields:
            res.append((field.name, getattr(model, field.name)))
        return res

    def get_context_data(self, **kwargs):
        context = super(ParsedModelDetailView, self).get_context_data(**kwargs)
        context['model'] = self.get_model_instance()
        context['fields'] = self.get_fields_from_model(context['model'])
        return context
