from django import forms

class GetUrlForm(forms.Form):
    url = forms.CharField(max_length=500)
