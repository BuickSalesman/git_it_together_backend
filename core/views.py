import json
from django.http import JsonResponse

from django.shortcuts import render

# Create your views here.

from .models import User
from .models import Repo


# retrieves users via get request to the database.
def get_users(request):
    users = User.objects.all()
    users_data = [
        {
            "id": user.id, "username": user.username,
        }
        for user in users
    ]
    return JsonResponse({"users": users_data})


def create_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            if not username or not password:
                return JsonResponse({"error": "Username and password are required."}, status=400)

            if User.objects.filter(username=username).exists():
                return JsonResponse({"error": "A user with that username already exists"}, status=400)

            user = User.objects.create_user(
                username=username, password=password)

            return JsonResponse({"message": "User created successfully", "user_id": user.id}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data."}, status=400
                                )

    else:
        return JsonResponse({"error": "This endpoint only supports POST requests."}, status=405)
