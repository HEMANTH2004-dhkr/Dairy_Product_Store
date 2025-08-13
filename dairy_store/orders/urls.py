from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('history/', views.order_history, name='order_history'),
    path('<int:order_id>/', views.order_detail, name='order_detail'),  # Added this
    path('<int:order_id>/cancel/', views.cancel_order, name='cancel_order'),
    path('order-confirmation_view/<int:order_id>/', views.order_confirmation_view, name='order_confirmation_view'),
    path('return/<int:order_id>/', views.return_order, name='return_order'),
    path('cancel/<int:order_id>/', views.cancel_order, name='cancel_order'),
]