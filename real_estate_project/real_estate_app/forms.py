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

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput(attrs={'class': 'form-control'}))
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class PropertyForm(forms.ModelForm):
    property_photos = MultipleFileField(label="Property Photos", required=False)

    class Meta:
        model = Property
        fields = ['address', 'latitude', 'longitude', 'price']
        widgets = {
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter property address...', 'id': 'id_address'}),
            'latitude': forms.HiddenInput(attrs={'id': 'id_latitude'}),
            'longitude': forms.HiddenInput(attrs={'id': 'id_longitude'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter price per month...', 'min': '1', 'oninput': "this.value = Math.abs(this.value) > 0 ? Math.abs(this.value) : ''"}),
        }

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is None or price < 1:
            raise forms.ValidationError("Price must be a positive amount.")
        return price
        
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['start_date', 'duration_months']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'duration_months': forms.NumberInput(attrs={'min': '1', 'oninput': "this.value = Math.abs(this.value) > 0 ? Math.abs(this.value) : ''"})
        }

    def clean_duration_months(self):
        duration = self.cleaned_data.get('duration_months')
        if duration is None or duration < 1:
            raise forms.ValidationError("Duration must be at least 1 month.")
        return duration
