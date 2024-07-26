from django.urls import path
from . import views

urlpatterns = [
    path('request/create/', views.create_request, name='create_request'),
    path('client/', views.client_page, name='client_page'),
    path('master/', views.master_page, name='master_page'),
    path('register/master/', views.register_master, name='register-master'),
    path('register/client/', views.register_client, name='register-client'),

    path('accept/<int:request_id>/', views.accept_request, name='accept_request'),
    path('reject/<int:request_id>/', views.reject_request, name='reject_request'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
