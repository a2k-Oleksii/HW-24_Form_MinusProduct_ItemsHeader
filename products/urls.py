from django.urls import path
from .views import add_product, products_details, edit_product, update_product, add_category, update_category, delete_product

urlpatterns = [
    path('/add', add_product, name='add_product'),
    path('/edit/<int:id>', edit_product, name="edit_product"),
    path('/update/<int:id>', update_product, name="update_product"),
    path('/delete/<int:id>', delete_product, name="delete_product"),
    path('/category/add', add_category, name='add_category'),
    path('/category/update/<int:id>', update_category, name='update_category'),
    path('/<int:id>', products_details, name='products_details'),
]
