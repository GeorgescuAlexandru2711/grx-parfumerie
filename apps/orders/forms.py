from django import forms

class CheckoutForm(forms.Form):
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'First Name',
            'class': 'w-full px-4 py-3 bg-[#16161E] border border-[#2D2D3D] rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-[#C5A880] transition'
        })
    )
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Last Name',
            'class': 'w-full px-4 py-3 bg-[#16161E] border border-[#2D2D3D] rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-[#C5A880] transition'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'order@example.com',
            'class': 'w-full px-4 py-3 bg-[#16161E] border border-[#2D2D3D] rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-[#C5A880] transition'
        })
    )
    phone_number = forms.CharField(
        max_length=25,
        widget=forms.TextInput(attrs={
            'placeholder': '+40 700 000 000',
            'class': 'w-full px-4 py-3 bg-[#16161E] border border-[#2D2D3D] rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-[#C5A880] transition'
        })
    )
    address_line1 = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'placeholder': 'Street and House / Apartment Number',
            'class': 'w-full px-4 py-3 bg-[#16161E] border border-[#2D2D3D] rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-[#C5A880] transition'
        })
    )
    address_line2 = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Apartment, Suite, Unit, etc. (Optional)',
            'class': 'w-full px-4 py-3 bg-[#16161E] border border-[#2D2D3D] rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-[#C5A880] transition'
        })
    )
    city = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Bucharest, Cluj-Napoca, Timișoara, etc.',
            'class': 'w-full px-4 py-3 bg-[#16161E] border border-[#2D2D3D] rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-[#C5A880] transition'
        })
    )
    county = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Sector or County (Județ)',
            'class': 'w-full px-4 py-3 bg-[#16161E] border border-[#2D2D3D] rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-[#C5A880] transition'
        })
    )
    postal_code = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'placeholder': '010001',
            'class': 'w-full px-4 py-3 bg-[#16161E] border border-[#2D2D3D] rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-[#C5A880] transition'
        })
    )
    order_notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'Special delivery instructions or perfume gift wrapping requests...',
            'class': 'w-full px-4 py-3 bg-[#16161E] border border-[#2D2D3D] rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-[#C5A880] transition'
        })
    )
