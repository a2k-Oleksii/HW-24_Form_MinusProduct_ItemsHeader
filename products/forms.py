from django import forms
from .models import Product


class ProductForm(forms.ModelForm):

    def save(self, commit=True, **kwargs):
        instance = super(ProductForm, self).save(commit=False)
        instance.description = instance.description + "..."
        instance.user = kwargs["user"]
        if commit:
            instance.save()
        return instance

    class Meta:
        model = Product
        fields = ["title", "description", "price"]


class UpdateProductsForm(forms.Form):
    def is_valid(self, is_superuser, is_staff, owner, id):
        if Product.objects.get(id=id).user == owner:
            return True
        elif is_staff:
            return is_staff
        else:
            return is_superuser
        return False
