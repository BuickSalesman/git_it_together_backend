"""
URL configuration for git_it_together_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path(", views.home, name="home")
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path(", Home.as_view(), name="home")
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path("blog/", include("blog.urls"))
"""
from django.contrib import admin
from django.urls import path
from core.views import create_user, create_repo, create_commit
from core.views import update_current_user
from core.views import delete_current_user, delete_repo
from core.views import get_all_users, get_current_user, get_repos, get_commits
# get_repos, get_commits

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("admin/", admin.site.urls),

    path("users/all/", get_all_users, name="get_all_users"),
    path("users/create/", create_user, name="create_user"),
    path("users/me/", get_current_user, name="get_current_user"),
    path("users/me/update/", update_current_user, name="update_current_user"),
    path("users/me/delete/", delete_current_user, name="delete_current_user"),

    path("repos/create/", create_repo, name="create_repo"),
    path("repos/", get_repos, name="get_repos"),
    path("repos/delete/", delete_repo, name="delete_repo"),

    path("commits/create/", create_commit, name="create_commit"),
    path("commits/", get_commits, name="get_commits"),


    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
