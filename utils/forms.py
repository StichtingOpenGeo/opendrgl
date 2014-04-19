from django.forms import ModelForm

__author__ = 'joel'


class BootstrapModelForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(BootstrapModelForm, self).__init__(*args, **kwargs)
        self.helper = BootstrapModelForm(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'