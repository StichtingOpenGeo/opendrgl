from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import ModelForm
from stops.models import Stop
from django.utils.translation import ugettext_lazy as _

class StopForm(ModelForm):

    class Meta:
        model = Stop
        exclude = ('project',)

    def __init__(self, *args, **kwargs):
        super(StopForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', _('Opslaan')))