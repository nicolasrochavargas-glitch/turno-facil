"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from turnos.views import inicio, solicitar_turno, consultar_turno, panel_turnos, cambiar_estado, llamar_siguiente, pantalla_publica

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
    'login/',
    auth_views.LoginView.as_view(template_name='turnos/login.html'),
    name='login'
),
path(
    'logout/',
    auth_views.LogoutView.as_view(),
    name='logout'
),
    path('', inicio, name='inicio'),
    path('solicitar/', solicitar_turno, name='solicitar_turno'),
    path('consultar/', consultar_turno, name='consultar_turno'),
    path('panel/', panel_turnos, name='panel_turnos'),
    path('panel/cambiar/<int:turno_id>/<str:estado>/', cambiar_estado, name='cambiar_estado'),
    path('panel/siguiente/', llamar_siguiente, name='llamar_siguiente'),
    path('pantalla/', pantalla_publica, name='pantalla_publica'),
]