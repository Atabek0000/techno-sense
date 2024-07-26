from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from academy import views as orders_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('academy.urls')),
    path('', include('content.urls')),
    path('client/', orders_views.client_page, name='client_page'),
    path('master/', orders_views.master_page, name='master_page'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
