import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.shortcuts import render

# Create your views here.

from .models import User, Repo, Commit

# region USER


@csrf_exempt
def jwt_generation(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")

            if not username or not password:
                return JsonResponse({"error": "Username and password are required."}, status=400)

            user = authenticate(username=username, password=password)
            if user is not None:
                refresh = RefreshToken.for_user(user)
                return JsonResponse({
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }, status=200)
            else:
                return JsonResponse({"error": "Invalid username or password"}, status=401)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data."}, status=400)

    else:
        return JsonResponse({"error": "This enpoint only supports POST requests"}, status=405)


@csrf_exempt
def create_user(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")

            if not username or not password:
                return JsonResponse({"error": "Username and password are required."}, status=400)

            if User.objects.filter(username=username).exists():
                return JsonResponse({"error": "A user with that username already exists"}, status=400)

            user = User.objects.create_user(
                username=username, password=password)

            return JsonResponse({"message": "User created successfully", "user_id": user.id}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data."}, status=400)

    else:
        return JsonResponse({"error": "This endpoint only supports POST requests."}, status=405)


@api_view(["GET"])
@permission_classes({IsAuthenticated})
def get_current_user(request):
    user = request.user
    user_data = {
        "username": user.username,
        "date_joined": user.date_joined.isoformat()
    }
    return Response({"user": user_data}, status=200)


@api_view(["PATCH"])
@permission_classes({IsAuthenticated})
def update_current_user(request):
    user = request.user
    data = request.data

    new_username = data.get("new_username", None)
    new_password = data.get("new_password", None)

    if new_username and new_username != user.username:
        if User.objects.filter(username=new_username).exists():
            return Response({"error": "This username is already taken"}, status=400)
        user.username = new_username

    if new_password:
        user.set_password(new_password)

    user.save()

    return Response({
        "message": "User updated successfully",
        "user_id": user.id,
        "username": user.username
    }, status=200)


@api_view(["DELETE"])
@permission_classes({IsAuthenticated})
def delete_current_user(request):
    user = request.user
    user.delete()

    return Response({
        "message": "User deleted successfully",
        "username": user.username
    }, status=200)

# endregion USER
# region REPOS


@csrf_exempt
def create_repo(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username")
            name = data.get("name")
            notes_enabled = data.get("notes_enabled", False)

            if not username or not name:
                return JsonResponse({"error": "Username and repo name are required"}, status=400)

            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return JsonResponse({"error": "User does not exist"}, status=404)

            if Repo.objects.filter(user=user, name=name).exists():
                return JsonResponse({"error": "A repository with this name already exists for this user"}, status=400)

            repo = Repo.objects.create(
                user=user, name=name, notes_enabled=notes_enabled)

            return JsonResponse({
                "message": "Repository created successfully",
                "repo_id": repo.id,
                "user": user.username,
                "name": repo.name,
                "notes_enabled": repo.notes_enabled,
                "created_at": repo.created_at.isoformat()
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)

    else:
        return JsonResponse({"error": "This endpoint only supports POST requests"}, status=405)


@csrf_exempt
def delete_repo(request):
    if request.method == "DELETE":
        try:
            data = json.loads(request.body)
            username = data.get("username")
            name = data.get("name")

            if not username or not name:
                return JsonResponse({"error": "Username and repo name are required"}, status=400)

            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return JsonResponse({"error": "User does not exist"}, status=404)

            try:
                repo = Repo.objects.get(user=user, name=name)
            except Repo.DoesNotExist:
                return JsonResponse({"error": "Repository not found for this user"}, status=404)

            repo.delete()

            return JsonResponse({"message": "Repository deleted successfully"}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)

    else:
        return JsonResponse({"error": "This endpoint only supports DELETE requests"}, status=405)

# endregion REPOS

# region COMMITS


@csrf_exempt
def create_commit(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username")
            name = data.get("name")
            note_title = data.get("note_title", None)
            note_body = data.get("note_body", None)

            if not username or not name:
                return JsonResponse({"error": "Username and name are required"}, status=400)

            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return JsonResponse({"error": "User does not exist"}, status=404)

            try:
                repo = Repo.objects.get(user=user, name=name)
            except Repo.DoesNotExist:
                return JsonResponse({"error": "Repo does not exist for this user"}, status=404)

            commit = Commit.objects.create(
                repo=repo,
                note_title=note_title,
                note_body=note_body
            )

            return JsonResponse({
                "message": "Commit created successfully",
                "commit_id": commit.id,
                "repo": repo.name,
                "user": user.username,
                "note_title": commit.note_title,
                "note_body": commit.note_body,
                "created_at": commit.created_at.isoformat()
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data."}, status=400)

    else:
        return JsonResponse({"error": "This endpoint only supports POST requests."}, status=405)


# endregion COMMITS
