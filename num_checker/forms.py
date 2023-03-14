from django import forms


class NumberForm(forms.Form):
    number = forms.CharField(
        max_length=11,
        min_length=11
    )
