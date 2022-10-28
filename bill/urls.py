from django.urls import path
from .views import *

urlpatterns = [
    path('bill/<pk>',ProductBillDetail.as_view(),name='bill'),
    path('dashboard/',Dashboard.as_view(),name='dashboard'),
    path('create_bill/',CreateBill.as_view(),name='create_bill'),
    path('pdf-report/<int:id>',pdf_report_create,name='pdf-report'),
    path('product-update/<pk>', ProductBillUpdate.as_view(), name='update-product'),
    path('login/',login,name='login'),
    path('ajax',DataTablesAjaxPagination.as_view(), name='bill-list-ajax'),
]