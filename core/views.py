from django.http import JsonResponse

from django.shortcuts import render

# Create your views here.

from .models import User
from .models import Repo


def get_users(req):
    users = User.objects.all()
    users_data = [
        {
            "id": user.id, "username": user.username,
        }
        for user in users
    ]
    return JsonResponse({"users": users_data})


def create_repo(req):
    repo = Repo
