import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render

# Create your views here.

from .models import User, Repo, Commit


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


@csrf_exempt
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
            return JsonResponse({"error": "Invalid JSON data."}, status=400)

    else:
        return JsonResponse({"error": "This endpoint only supports POST requests."}, status=405)


@csrf_exempt
def create_repo(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            repo_name = data.get('name')
            notes_enabled = data.get('notes_enabled', False)

            if not username or not repo_name:
                return JsonResponse({"error": "Username and repo name are required"}, status=400)

            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return JsonResponse({"error": "User does not exist"}, status=404)

            if Repo.objects.filter(user=user, name=repo_name).exists():
                return JsonResponse({"error": "A repository with this name already exists for this user"}, status=400)

            repo = Repo.objects.create(
                user=user, name=repo_name, notes_enabled=notes_enabled)

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
        return JsonResponse({"error": "This endpoint only supports POST requests."}, status=405)


@csrf_exempt
def create_commit(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get('username')
            repo_name = data.get('repo_name')
            note_title = data.get('note_title', None)
            note_body = data.get('note_body', None)

            if not username or not repo_name:
                return JsonResponse({"error": "Username and repo_name are required"}, status=400)

            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return JsonResponse({"error": "User does not exist"}, status=404)

            try:
                repo = Repo.objects.get(user=user, name=repo_name)
            except Repo.DoesNotExist:
                return JsonResponse({"error": "Repo does not exist for this user"})

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
        return JsonResponse({"error": "This endpoint only supports POST requests."})
