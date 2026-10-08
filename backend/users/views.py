"""Vistas de la API: auth por sesiones de Django + CRUD de usuarios.

Nunca se devuelve ni se acepta una contraseña en texto plano para
almacenarla: se usa User.objects.create_user / set_password (hashing).
La API nunca devuelve el campo password.
"""

import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.views.decorators.csrf import ensure_csrf_cookie


def _body(request):
    try:
        return json.loads(request.body.decode('utf-8') or '{}')
    except (json.JSONDecodeError, UnicodeDecodeError):
        return {}


def _user_to_dict(u):
    return {'id': u.id, 'username': u.username, 'email': u.email or ''}


def _login_required_json(view):
    """Como @login_required pero devuelve 403 JSON (no redirect) para la API."""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'detail': 'No autenticado.'}, status=403)
        return view(request, *args, **kwargs)
    return wrapper


@require_GET
@ensure_csrf_cookie
def csrf_view(request):
    # Solo sirve para que Django emita la cookie csrftoken.
    return JsonResponse({'detail': 'CSRF cookie enviada.'})


@require_POST
def register_view(request):
    data = _body(request)
    username = (data.get('username') or '').strip()
    email = (data.get('email') or '').strip()
    password = data.get('password') or ''
    password2 = data.get('password2') or ''

    if not username or not password:
        return JsonResponse({'detail': 'username y password son obligatorios.'}, status=400)
    if password != password2:
        return JsonResponse({'detail': 'Las contraseñas no coinciden.'}, status=400)
    if len(password) < 8:
        return JsonResponse({'detail': 'La contraseña debe tener al menos 8 caracteres.'}, status=400)
    if User.objects.filter(username=username).exists():
        return JsonResponse({'detail': 'Ese username ya existe.'}, status=400)

    # create_user aplica el hashing de Django (nunca texto plano).
    user = User.objects.create_user(username=username, email=email, password=password)
    return JsonResponse(_user_to_dict(user), status=201)


@require_POST
def login_view(request):
    data = _body(request)
    username = (data.get('username') or '').strip()
    password = data.get('password') or ''
    user = authenticate(request, username=username, password=password)
    if user is None:
        return JsonResponse({'detail': 'Credenciales inválidas.'}, status=400)
    login(request, user)  # crea la sesión de Django
    return JsonResponse(_user_to_dict(user))


@require_POST
@_login_required_json
def logout_view(request):
    logout(request)
    return JsonResponse({'detail': 'Sesión cerrada.'})


@require_GET
def me_view(request):
    """Comprobar sesión: 200 + usuario si hay sesión, 403 si no."""
    if not request.user.is_authenticated:
        return JsonResponse({'detail': 'No autenticado.'}, status=403)
    return JsonResponse(_user_to_dict(request.user))


@_login_required_json
@require_http_methods(['GET', 'POST'])
def users_collection(request):
    if request.method == 'GET':
        users = User.objects.all().order_by('id')
        return JsonResponse([_user_to_dict(u) for u in users], safe=False)

    # POST: crear usuario (con password hasheada)
    data = _body(request)
    username = (data.get('username') or '').strip()
    email = (data.get('email') or '').strip()
    password = data.get('password') or ''
    if not username or not password:
        return JsonResponse({'detail': 'username y password son obligatorios.'}, status=400)
    if len(password) < 8:
        return JsonResponse({'detail': 'La contraseña debe tener al menos 8 caracteres.'}, status=400)
    if User.objects.filter(username=username).exists():
        return JsonResponse({'detail': 'Ese username ya existe.'}, status=400)
    user = User.objects.create_user(username=username, email=email, password=password)
    return JsonResponse(_user_to_dict(user), status=201)


@_login_required_json
@require_http_methods(['GET', 'PUT', 'DELETE'])
def user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return JsonResponse({'detail': 'No encontrado.'}, status=404)

    if request.method == 'GET':
        return JsonResponse(_user_to_dict(user))

    if request.method == 'PUT':
        data = _body(request)
        username = (data.get('username') or '').strip()
        email = (data.get('email') or '').strip()
        password = data.get('password') or ''
        if not username:
            return JsonResponse({'detail': 'username es obligatorio.'}, status=400)
        if User.objects.exclude(pk=user.pk).filter(username=username).exists():
            return JsonResponse({'detail': 'Ese username ya existe.'}, status=400)
        user.username = username
        user.email = email
        if password:  # solo se cambia si se envía; se hashea con set_password
            if len(password) < 8:
                return JsonResponse({'detail': 'La contraseña debe tener al menos 8 caracteres.'}, status=400)
            user.set_password(password)
        user.save()
        return JsonResponse(_user_to_dict(user))

    # DELETE: no se puede eliminar a sí mismo para no quedarse sin sesión a medias
    if user.pk == request.user.pk:
        return JsonResponse({'detail': 'No puedes eliminarte a ti mismo.'}, status=400)
    user.delete()
    return JsonResponse({'detail': 'Eliminado.'})
