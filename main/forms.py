from django import forms
from django.utils.safestring import mark_safe


class GetUrlForm(forms.Form):
    url = forms.CharField(max_length=500,label="Vui lòng nhập URL")

class GetAttribForm(forms.Form):
    def __init__(self,mausac,bonho,*args,**kwargs):
        super(GetAttribForm,self).__init__(*args,**kwargs)
        self.fields['mausac'].choices = mausac
        self.fields['bonho'].choices = bonho
    mausac = forms.ChoiceField(choices=(),label='Màu sắc',required=False)
    bonho = forms.ChoiceField(choices=(),label=mark_safe('Bộ nhớ'),required=False)