from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import CustomLoginForm

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html', authentication_form=CustomLoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('property/add/', views.add_property, name='add_property'),
    path('property/catalog/', views.property_catalog, name='property_catalog'),
    path('property/<int:property_id>/book/', views.book_property, name='book_property'),
    path('property/<int:property_id>/admin-detail/', views.admin_property_detail, name='admin_property_detail'),
    path('property/<int:property_id>/owner-detail/', views.owner_property_detail, name='owner_property_detail'),
    path('property/<int:property_id>/seeker-detail/', views.seeker_property_detail, name='seeker_property_detail'),
    path('payment/<int:booking_id>/', views.mock_payment, name='mock_payment'),
    path('property/<int:property_id>/approve/', views.approve_property, name='approve_property'),
    path('property/<int:property_id>/reject/', views.reject_property, name='reject_property'),
    path('', views.home, name='home'),
]
