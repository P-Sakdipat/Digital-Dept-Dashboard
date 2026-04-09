from django.urls import path
from .views import SalesSummaryView, SalesDataView, SalesDetailView

urlpatterns = [
    path('summary/', SalesSummaryView.as_view(), name='sales_summary'),
    path('sales/', SalesDataView.as_view(), name='sales_list_create'),
    path('sales/<int:vbeln>/<int:posnr>/', SalesDetailView.as_view(), name='sales_detail'),
]
