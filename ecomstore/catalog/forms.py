from django import forms
from ecomstore.catalog.models import Product, Category

class ProductAdminForm(forms.ModelForm):
    """ ModelForm class to validate product instance data before saving from admin interface """
    class Meta:
        model = Product

    def clean_price(self):
        if self.cleaned_data['price'] <= 0:
            raise forms.ValidationError('Price supplied must be greater than zero.')
        return self.cleaned_data['price']
