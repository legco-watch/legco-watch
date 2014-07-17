from django.forms import ModelForm
from django.views.generic import FormView
# Create your views here.
from common.models import ErrorReport


class ErrorReportForm(ModelForm):
    class Meta:
        model = ErrorReport
        fields = ['reported', 'url', 'common']


class ErrorReportFormView(FormView):
    template_name = 'error_report.html'
    form_class = ErrorReportForm

    def get(self, request, *args, **kwargs):
        # Pre-fill the form with the reporting url
        # if it's not there, show an error
        return super(ErrorReportFormView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # Save, then redirect back to the url on which the error was found
        return super(ErrorReportFormView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        """
        Redirect back to the reported url
        """
        pass
