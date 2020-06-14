from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('password_reset/', views.MyPasswordResetView, name='password_reset'),
    path('accounts/login/', views.MyLoginView.as_view(), name='login'),
    path('accounts/password_change/done/', views.Passdone, name='passdone'),
    path('accounts/password_change/passdone', views.MyPasswordChangeView.as_view(template_name = 'registration/password_change_form.html',success_url=reverse_lazy('passdone')), name='password_change'),
    path('accounts/logout/',auth_views.LogoutView.as_view(template_name='index', next_page='index'), name = 'logout'),
    path('accounts/password_reset/', views.MyPasswordResetView, name='password_reset'),
    path('accounts/', include('django.contrib.auth.urls')),
]