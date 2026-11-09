from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import User

class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': '••••••••',
            'class': 'w-full px-4 py-3 bg-[#16161E] border border-[#2D2D3D] rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-[#C5A880] transition'
        }),
        validators=[validate_password]
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': '••••••••',
            'class': 'w-full px-4 py-3 bg-[#16161E] border border-[#2D2D3D] rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-[#C5A880] transition'
        })
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Alexandru',
                'class': 'w-full px-4 py-3 bg-[#16161E] border border-[#2D2D3D] rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-[#C5A880] transition'
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Georgescu',
                'class': 'w-full px-4 py-3 bg-[#16161E] border border-[#2D2D3D] rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-[#C5A880] transition'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'alex@example.com',
                'class': 'w-full px-4 py-3 bg-[#16161E] border border-[#2D2D3D] rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-[#C5A880] transition'
            }),
            'phone_number': forms.TextInput(attrs={
                'placeholder': '+40 700 000 000',
                'class': 'w-full px-4 py-3 bg-[#16161E] border border-[#2D2D3D] rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-[#C5A880] transition'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match.')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'your.email@example.com',
            'class': 'w-full px-4 py-3 bg-[#16161E] border border-[#2D2D3D] rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-[#C5A880] transition'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': '••••••••',
            'class': 'w-full px-4 py-3 bg-[#16161E] border border-[#2D2D3D] rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-[#C5A880] transition'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            self.user = authenticate(username=email, password=password)
            if self.user is None:
                raise forms.ValidationError('Invalid email or password.')
            if not self.user.is_active:
                raise forms.ValidationError('This account is inactive.')

        return cleaned_data


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'phone_number',
            'address_line1', 'address_line2', 'city', 'county', 'postal_code'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'w-full px-4 py-2.5 bg-[#16161E] border border-[#2D2D3D] rounded-lg text-white focus:outline-none focus:border-[#C5A880]'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full px-4 py-2.5 bg-[#16161E] border border-[#2D2D3D] rounded-lg text-white focus:outline-none focus:border-[#C5A880]'}),
            'phone_number': forms.TextInput(attrs={'class': 'w-full px-4 py-2.5 bg-[#16161E] border border-[#2D2D3D] rounded-lg text-white focus:outline-none focus:border-[#C5A880]'}),
            'address_line1': forms.TextInput(attrs={'class': 'w-full px-4 py-2.5 bg-[#16161E] border border-[#2D2D3D] rounded-lg text-white focus:outline-none focus:border-[#C5A880]'}),
            'address_line2': forms.TextInput(attrs={'class': 'w-full px-4 py-2.5 bg-[#16161E] border border-[#2D2D3D] rounded-lg text-white focus:outline-none focus:border-[#C5A880]'}),
            'city': forms.TextInput(attrs={'class': 'w-full px-4 py-2.5 bg-[#16161E] border border-[#2D2D3D] rounded-lg text-white focus:outline-none focus:border-[#C5A880]'}),
            'county': forms.TextInput(attrs={'class': 'w-full px-4 py-2.5 bg-[#16161E] border border-[#2D2D3D] rounded-lg text-white focus:outline-none focus:border-[#C5A880]'}),
            'postal_code': forms.TextInput(attrs={'class': 'w-full px-4 py-2.5 bg-[#16161E] border border-[#2D2D3D] rounded-lg text-white focus:outline-none focus:border-[#C5A880]'}),
        }
