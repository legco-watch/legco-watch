from datetime import datetime
from django.forms import ModelForm
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.views.generic import FormView, TemplateView
# Create your views here.
from urllib import unquote_plus
from common.models import ErrorReport


class LandingView(TemplateView):
    template_name = 'landing.html'

    def get_context_data(self, **kwargs):
        context = super(LandingView, self).get_context_data(**kwargs)
        context['errors'] = ErrorReport.objects.open_errors()
        return context


class ErrorReportForm(ModelForm):
    class Meta:
        model = ErrorReport
        fields = ['reported', 'url', 'comment']


class ErrorReportFormView(FormView):
    template_name = 'common/error_report.html'
    form_class = ErrorReportForm

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        # Pre-fill the form with the reporting url
        url = request.GET.get('url', None)
        if url is None:
            # if it's not there, show an error
            return HttpResponseBadRequest('Must provide url')
        form.fields['url'].initial = unquote_plus(url)
        form.fields['reported'].initial = datetime.now()
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        # If the form is valid, save the form, then go back to the reported url
        form.save()
        url = form.cleaned_data['url']
        return HttpResponseRedirect(url)
