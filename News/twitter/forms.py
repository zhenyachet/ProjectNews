from django import forms


class UpdateForm(forms.Form):
    Number_of_stream = forms.IntegerField(min_value=15,
                                          max_value=100,
                                          initial=20,
                                          required=True,
                                          label='Time limit for streaming (sec.)')


class InputPinForm(forms.Form):
    PIN = forms.CharField(required=True,
                          max_length=7,
                          min_length=7,
                          label='Input PIN for using twitter API'
                                )
