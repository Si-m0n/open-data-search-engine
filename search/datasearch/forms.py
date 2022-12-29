from django import forms

from datasearch.models import Decision


class DecisionForm(forms.ModelForm):
    class Meta:
        model = Decision
        fields = "__all__"


class SearchForm(forms.Form):
    numero_de_dossier = forms.IntegerField(required=False)
    contenu = forms.CharField(max_length=1000, required=False)
