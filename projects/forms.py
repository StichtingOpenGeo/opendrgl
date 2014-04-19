from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.forms import ModelForm
from projects.models import Project
from utils.forms import BootstrapModelForm


class ProjectForm(ModelForm):
    class Meta:
        model = Project

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = True
        self.helper.form_method = "POST"
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'

        self.helper.add_input(Submit('submit', 'Opslaan'))
