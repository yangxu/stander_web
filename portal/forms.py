from django import forms
from portal.models import Template, FlatPageAddon
from django.contrib.flatpages.models import FlatPage

class TemplateForm(forms.ModelForm):
    file_name = forms.CharField(label='Name', max_length=200, required=True)
    content = forms.CharField(label='HTML', widget=forms.Textarea, required=False)
    
    file_name.widget.attrs.update({'class': 'form-control form-control-lg'})
    content.widget.attrs.update({'class': 'form-control form-control-lg', 'style':'display:none;'})

    class Meta:
        model = Template
        fields = ('file_name', 'content')

class FlatPageForm(forms.ModelForm):
    title = forms.CharField(label='Name', max_length=200, required=True)
    content = forms.CharField(label='HTML', widget=forms.Textarea, required=False)
    
    title.widget.attrs.update({'class': 'form-control form-control-lg'})
    content.widget.attrs.update({'class': 'form-control form-control-lg', 'style':'display:none;'})

    class Meta:
        model = FlatPage
        fields = ('title', 'content')

class FlatPageAddonForm(forms.ModelForm):
    header = forms.CharField(label='HTML', widget=forms.Textarea, required=False)
    
    header.widget.attrs.update({'class': 'form-control form-control-lg', 'style':'display:none;'})

    class Meta:
        model = FlatPageAddon
        fields = ('header',)
