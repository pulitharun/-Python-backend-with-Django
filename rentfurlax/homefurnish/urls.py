#urls.py

from django import views
from .views import *
from django.urls import path



# URL patterns for API endpoints
urlpatterns = [
    path('register', CustomerView.as_view()),
    path('login', LoginView.as_view()),
    path('username/<str:username>',GetidfromusernameView.as_view()),
    path('category', CategoriesView.as_view()),
    path('categories', GetCategoryView.as_view()),
    path('products', AddProductView.as_view()),
    path('invoice',CreateInvoiceView.as_view()),
    path('invoices/<str:status>',GetInvoiceBasedOnStatus.as_view()),
    # path('invoices/<int:product_id>',GetInvoiceBasedOnStatus.as_view()),
    path('product/<int:product_id>',GetProductsByID.as_view()),
    path('<str:category>',GetProductsByCategoryView.as_view()),
    
]