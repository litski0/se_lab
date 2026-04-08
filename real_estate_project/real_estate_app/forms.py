from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Property, Booking

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number', 'pincode', 'is_owner', 'is_seeker')
        
    def clean(self):
        cleaned_data = super().clean()
        is_owner = cleaned_data.get('is_owner')
        is_seeker = cleaned_data.get('is_seeker')
        if not is_owner and not is_seeker:
            raise forms.ValidationError("You must register as either an Owner or a Seeker.")
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'

class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['address', 'price', 'photo']
        widgets = {
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter property address...'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter price per month...'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }
        
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['start_date', 'duration_months']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
        }
