from django import forms
from .models import State, City

class AddressForm(forms.Form):
    state = forms.ModelChoiceField(queryset=State.objects.all())
    city = forms.ModelChoiceField(queryset=City.objects.none())  # Initialize with an empty queryset

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].queryset = City.objects.filter(state=self.fields['state'].initial)  # Filter cities based on the initial state value

    def clean(self):
        cleaned_data = super().clean()
        state = cleaned_data.get('state')
        city = cleaned_data.get('city')

        if state and city:
            if city.state != state:
                self.add_error('city', 'Invalid city for the selected state')

        return cleaned_data