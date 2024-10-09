from django.urls import path, include
from . import views

app_name = 'authentication'

urlpatterns = [             
    path('register', views.register, name="register"),
    path('login/', views.login_user, name="login"),
    path('', views.login_user, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('health/home/', views.health_home, name='health-home'),

]
