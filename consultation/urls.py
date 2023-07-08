from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('add-client', views.AddCustomerView.as_view(), name="add-client"),
    path('add-facture', views.AddInvoiceView.as_view(), name="add-facture"),
]



