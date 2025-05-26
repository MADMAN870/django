from django import forms
from .models import Reservation

class ReservationForm(forms.ModelForm):
    TRAVEL_CLASS_CHOICES = [
        ('economic', 'Economic'),
        ('flexible', 'Flexible')
    ]
    
    travel_class = forms.ChoiceField(
        choices=TRAVEL_CLASS_CHOICES,
        widget=forms.RadioSelect,
        initial='economic'
    )
    
    children_ages = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Enter ages separated by commas'})
    )
    
    extra_baggage = forms.BooleanField(required=False)
    
    class Meta:
        model = Reservation
        fields = ['travel_class', 'number_of_persons', 'children_ages', 'selected_options', 'extra_baggage']
        widgets = {
            'selected_options': forms.CheckboxSelectMultiple()
        }
    
    def clean_children_ages(self):
        ages = self.cleaned_data.get('children_ages')
        if ages:
            try:
                ages_list = [int(age.strip()) for age in ages.split(',')]
                return ages_list
            except ValueError:
                raise forms.ValidationError('Please enter valid ages separated by commas')
        return []