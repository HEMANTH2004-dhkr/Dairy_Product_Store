from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),  # Dashboard route (avoid empty string path duplicates)
    path('', views.home, name='home'),  # Home route
    path('product/<int:pk>/', views.product_detail_view, name='product_detail'),  # Product detail
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),  # Profile edit route
    # other URLs...
]
