"""
URL configuration for fstore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from rest_framework_simplejwt.views import TokenRefreshView
from django.views.decorators.csrf import csrf_exempt
from django.contrib import admin
from django.urls import path

from auth.views import TokenObtainView, TokenCheckPairView

urlpatterns = [

    # Auth
    path('api/auth/token/obtain', TokenObtainView.as_view()),
    path('api/auth/token/check', csrf_exempt(TokenCheckPairView.as_view())),
    path('api/auth/token/refresh', TokenRefreshView.as_view()),

    # Django admin
    path('admin/', admin.site.urls),
]
