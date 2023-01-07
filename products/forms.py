from django import forms
from .models import Product
from django.contrib.auth.models import User


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


class ValidateForm(forms.Form):

    def is_valid(self, user, id):
        if Product.objects.get(id=id).user == user:
            return True
        elif user.is_staff:
            return user.is_staff
        else:
            return user.is_superuser
        return False
