from django import forms
from apps.catalog.models import Product, ProductVariant, Brand, Category, FragranceFamily

INPUT_CLASSES = 'w-full px-4 py-2.5 bg-[#16161E] border border-[#2D2D3D] rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-[#C5A880] transition'
SELECT_CLASSES = 'w-full px-4 py-2.5 bg-[#16161E] border border-[#2D2D3D] rounded-lg text-white focus:outline-none focus:border-[#C5A880] transition'
CHECKBOX_CLASSES = 'w-4 h-4 text-[#C5A880] bg-[#16161E] border-[#2D2D3D] rounded focus:ring-[#C5A880]'

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'title', 'brand', 'category', 'fragrance_family', 'concentration',
            'short_description', 'description',
            'top_notes', 'heart_notes', 'base_notes',
            'image_url', 'is_featured', 'is_active'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'e.g. Baccarat Rouge 540'}),
            'brand': forms.Select(attrs={'class': SELECT_CLASSES}),
            'category': forms.Select(attrs={'class': SELECT_CLASSES}),
            'fragrance_family': forms.Select(attrs={'class': SELECT_CLASSES}),
            'concentration': forms.Select(attrs={'class': SELECT_CLASSES}),
            'short_description': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Luminous, dense, amber floral sillage...'}),
            'description': forms.Textarea(attrs={'class': INPUT_CLASSES, 'rows': 4, 'placeholder': 'Full perfume history and character...'}),
            'top_notes': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'e.g. Jasmine Grandiflorum, Saffron'}),
            'heart_notes': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'e.g. Bitter Almond, Cedarwood'}),
            'base_notes': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'e.g. Ambergris, Musky Woody Accord'}),
            'image_url': forms.URLInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'https://...'}),
            'is_featured': forms.CheckboxInput(attrs={'class': CHECKBOX_CLASSES}),
            'is_active': forms.CheckboxInput(attrs={'class': CHECKBOX_CLASSES}),
        }


class VariantForm(forms.ModelForm):
    class Meta:
        model = ProductVariant
        fields = ['size_label', 'size_ml', 'sku', 'price', 'stock_quantity', 'is_default']
        widgets = {
            'size_label': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'e.g. 100ml Eau de Parfum'}),
            'size_ml': forms.NumberInput(attrs={'class': INPUT_CLASSES, 'placeholder': '100'}),
            'sku': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'e.g. MFK-BR540-100'}),
            'price': forms.NumberInput(attrs={'class': INPUT_CLASSES, 'placeholder': '1450.00'}),
            'stock_quantity': forms.NumberInput(attrs={'class': INPUT_CLASSES, 'placeholder': '15'}),
            'is_default': forms.CheckboxInput(attrs={'class': CHECKBOX_CLASSES}),
        }


class QuickRestockForm(forms.Form):
    variant_id = forms.IntegerField(widget=forms.HiddenInput())
    add_units = forms.IntegerField(
        min_value=1,
        max_value=1000,
        widget=forms.NumberInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'Qty to add'})
    )
