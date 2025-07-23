# File: listings/forms.py

from django import forms
from django.contrib.auth.models import User
from .models import CarListing, Message, Review, Profile, TRANSMISSION_CHOICES, FUEL_TYPE_CHOICES

# ... (CarListingForm, UserUpdateForm, ProfileUpdateForm, MessageForm remain the same) ...
class CarListingForm(forms.ModelForm):
    additional_images = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-red-50 file:text-red-700 hover:file:bg-red-100'
        }),
        label="Additional Photos (Select multiple files)"
    )
    class Meta:
        model = CarListing
        fields = [
            'make', 'model', 'year', 'price', 'kms_driven',
            'image', 'mileage', 'transmission', 'fuel_type',
            'noc_available',
            'description', 'location_city'
        ]
        # ... widgets ...
        widgets = {
            'make': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500'}),
            'model': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500'}),
            'year': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500'}),
            'price': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500'}),
            'kms_driven': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500'}),
            'image': forms.FileInput(attrs={'class': 'w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-red-50 file:text-red-700 hover:file:bg-red-100'}),
            'mileage': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500'}),
            'transmission': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500'}),
            'fuel_type': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500'}),
            'noc_available': forms.CheckboxInput(attrs={'class': 'h-5 w-5 text-red-600 border-gray-300 rounded focus:ring-red-500'}),
            'description': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500', 'rows': 4}),
            'location_city': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500'}),
        }

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500'}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500'}),
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-red-50 file:text-red-700 hover:file:bg-red-100'}),
        }

# --- UPDATED CarFilterForm ---
class CarFilterForm(forms.Form):
    # Define common choices and widget attributes
    ANY_CHOICE = [('', 'Any')]
    WIDGET_ATTRS = {'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500'}

    # Existing fields
    transmission = forms.ChoiceField(choices=ANY_CHOICE + list(TRANSMISSION_CHOICES), required=False, widget=forms.Select(attrs=WIDGET_ATTRS))
    fuel_type = forms.ChoiceField(choices=ANY_CHOICE + list(FUEL_TYPE_CHOICES), required=False, widget=forms.Select(attrs=WIDGET_ATTRS))
    min_price = forms.IntegerField(required=False, min_value=0, widget=forms.NumberInput(attrs={**WIDGET_ATTRS, 'placeholder': 'Min Price'}))
    max_price = forms.IntegerField(required=False, min_value=0, widget=forms.NumberInput(attrs={**WIDGET_ATTRS, 'placeholder': 'Max Price'}))

    # --- NEW DYNAMIC FIELDS ---
    # We define them here, but their choices will be set in the view.
    make = forms.ChoiceField(required=False, widget=forms.Select(attrs=WIDGET_ATTRS))
    location_city = forms.ChoiceField(required=False, widget=forms.Select(attrs=WIDGET_ATTRS))
    year = forms.IntegerField(required=False, min_value=1900, widget=forms.NumberInput(attrs={**WIDGET_ATTRS, 'placeholder': 'e.g., 2021'}))

    # This special method allows us to pass dynamic choices from the view
    def __init__(self, *args, **kwargs):
        # Pop the custom choices from kwargs before calling super()
        make_choices = kwargs.pop('make_choices', [])
        city_choices = kwargs.pop('city_choices', [])
        
        super(CarFilterForm, self).__init__(*args, **kwargs)

        # Set the choices for the dynamic fields
        self.fields['make'].choices = self.ANY_CHOICE + make_choices
        self.fields['location_city'].choices = self.ANY_CHOICE + city_choices

# ... (ReviewForm and MessageForm remain the same) ...
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500',
                'rows': 4,
                'placeholder': 'Ask a question about the car...'
            })
        }
        labels = {'content': '',}

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={
                'type': 'number',
                'min': 1,
                'max': 5,
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500',
                'placeholder': 'Rating (1-5)'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500',
                'rows': 4,
                'placeholder': 'Share your experience with this seller...'
            })
        }
