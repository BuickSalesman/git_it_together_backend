import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
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


@api_view(["POST"])
@permission_classes([AllowAny])
def create_user(request):
    data = request.data
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return Response({"error": "Username and password are required"}, status=400)

    if User.objects.filter(username=username).exists():
        return Response({"error": "A user with that username already exists"}, status=400)

    user = User.objects.create_user(username=username, password=password)

    return Response({"message": "User created succesfully"}, status=200)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    user = request.user
    user_data = {
        "username": user.username,
        "date_joined": user.date_joined.isoformat()
    }
    return Response({"user": user_data}, status=200)


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
def delete_current_user(request):
    user = request.user
    user.delete()

    return Response({
        "message": "User deleted successfully",
        "username": user.username
    }, status=200)

# endregion USER
# region REPOS


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_repo(request):
    user = request.user
    data = request.data

    name = data.get("name")
    notes_enabled = data.get("notes_enabled", False)

    if not name:
        return Response({"error": "Repository must have a name."}, status=400)

    if Repo.objects.filter(user=user, name=name).exists():
        return Response({"error": "A repo of thius name already exists for this user."}, status=400)

    repo = Repo.objects.create(
        user=user,
        name=name,
        notes_enabled=notes_enabled
    )

    return Response({
        "message": "Repository created successfully",
        "repo_id": repo.id,
        "user": user.username,
        "name": repo.name,
        "notes_enabled": repo.notes_enabled,
        "created_at": repo.created_at.isoformat()
    }, status=201)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_repo(request):
    user = request.user
    data = request.data
    repo_name = data.get("name")

    if not repo_name:
        return Response({"error": "Repository name is required"}, status=400)

    try:
        repo = Repo.objects.get(user=user, name=repo_name)
    except Repo.DoesNotExist:
        return Response({
            "error": "Repository not found or doesn't belong to current user."
        }, status=404)

    repo.delete()
    return Response({"message": "Repo deleted successfully"}, status=200)


# endregion REPOS
# region COMMITS

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_commit(request):
    user = request.user
    data = request.data

    repo_name = data.get("name")
    note_title = data.get("note_title", None)
    note_body = data.get("note_body", None)

    if not repo_name:
        return Response({"error": "Repo name is required"}, status=400)

    try:
        repo = Repo.objects.get(user=user, name=repo_name)
    except Repo.DoesNotExist:
        return Response({"error": "Repo does not exist for this user."}, status=404)

    commit = Commit.objects.create(
        repo=repo,
        note_title=note_title,
        note_body=note_body
    )

    return Response({
        "message": "Commit created successfully",
        "commit_id": commit.id,
        "repo": repo.name,
        "user": user.username,
        "note_title": commit.note_title,
        "note_body": commit.note_body,
        "created_at": commit.created_at.isoformat()
    }, status=201)

# endregion COMMITS
