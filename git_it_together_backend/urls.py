"""
URL configuration for git_it_together_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from core.views import get_users, create_user, create_repo

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', get_users, name='get_users'),
    path('users/create/', create_user, name='create_user'),
    path('repos/create/', create_repo, name='create_repo'),
]
