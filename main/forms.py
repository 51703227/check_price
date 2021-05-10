from django import forms


class GetUrlForm(forms.Form):
    url = forms.CharField(max_length=500)

class GetAttribForm(forms.Form):
    def __init__(self,mausac,bonho,*args,**kwargs):
        super(GetAttribForm,self).__init__(*args,**kwargs)
        self.fields['mausac'].choices = mausac
        self.fields['bonho'].choices = bonho
    mausac = forms.ChoiceField(choices=(),label='Màu sắc')
    bonho = forms.ChoiceField(choices=(),label='Bộ nhớ')