import json
from functools import wraps

from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from django.db.models import ProtectedError
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET, require_POST, require_http_methods

from .models import Biotope, Region, Species


def admin_required(view):
    """Exige sesión (401) y usuario is_staff (403) para la API del panel."""

    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'detail': 'No autenticado.'}, status=401)
        if not request.user.is_staff:
            return JsonResponse({'detail': 'No autorizado: se requiere is_staff.'}, status=403)
        return view(request, *args, **kwargs)

    return wrapper


def _body(request):
    try:
        return json.loads(request.body.decode('utf-8') or '{}')
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None


def _user_to_dict(user):
    return {
        'id': user.id,
        'username': user.username,
        'is_staff': user.is_staff,
    }


def _region_to_dict(region):
    return {'id': region.id, 'name': region.name}


def _biotope_to_dict(biotope):
    return {
        'id': biotope.id,
        'name': biotope.name,
        'region_id': biotope.region_id,
        'region_name': biotope.region.name,
    }


def _species_to_dict(species):
    return {
        'id': species.id,
        'common_name': species.common_name,
        'scientific_name': species.scientific_name,
        'kind': species.kind,
        'temp_min': species.temp_min,
        'temp_max': species.temp_max,
        'ph_min': species.ph_min,
        'ph_max': species.ph_max,
        'gh_min': species.gh_min,
        'gh_max': species.gh_max,
        'adult_size_cm': species.adult_size_cm,
        'min_tank_liters': species.min_tank_liters,
        'min_group_size': species.min_group_size,
        'diet': species.diet,
        'temperament': species.temperament,
        'swim_zone': species.swim_zone,
        'eats_plants': species.eats_plants,
        'fin_nipper': species.fin_nipper,
        'territorial': species.territorial,
        'biotope_id': species.biotope_id,
        'biotope_name': species.biotope.name,
        'region_id': species.biotope.region_id,
        'region_name': species.biotope.region.name,
    }


def _validation_error_dict(exc):
    if hasattr(exc, 'message_dict'):
        result = {}
        for field, messages in exc.message_dict.items():
            key = '__all__' if field == '__all__' else field
            result.setdefault(key, []).extend(str(message) for message in messages)
        return result
    return {'__all__': [str(message) for message in exc.messages]}


def _merge_errors(errors, exc):
    for field, messages in _validation_error_dict(exc).items():
        target = errors.setdefault(field, [])
        for message in messages:
            if message not in target:
                target.append(message)
    return errors


def _error_response(errors, status=400):
    return JsonResponse({'errors': errors}, status=status)


def _not_found(kind):
    return JsonResponse({'detail': f'{kind} no encontrada.'}, status=404)


@require_GET
@ensure_csrf_cookie
def csrf_view(request):
    return JsonResponse({'detail': 'CSRF cookie enviada.'})


@require_POST
def login_view(request):
    data = _body(request)
    if data is None:
        return JsonResponse({'detail': 'JSON inválido.'}, status=400)

    username = (data.get('username') or '').strip()
    password = data.get('password') or ''
    user = authenticate(request, username=username, password=password)
    if user is None:
        return JsonResponse({'detail': 'Credenciales inválidas.'}, status=400)
    if not user.is_staff:
        return JsonResponse({'detail': 'Solo administradores pueden acceder al panel.'}, status=403)

    login(request, user)
    return JsonResponse(_user_to_dict(user))


@require_POST
@admin_required
def logout_view(request):
    logout(request)
    return JsonResponse({'detail': 'Sesión cerrada.'})


@require_GET
@admin_required
def me_view(request):
    return JsonResponse(_user_to_dict(request.user))


@admin_required
@require_http_methods(['GET', 'POST'])
def regions_collection(request):
    if request.method == 'GET':
        regions = Region.objects.all().order_by('name')
        return JsonResponse([_region_to_dict(region) for region in regions], safe=False)

    data = _body(request)
    if data is None:
        return JsonResponse({'detail': 'JSON inválido.'}, status=400)

    region = Region(name=(data.get('name') or '').strip())
    try:
        region.full_clean()
        region.save()
    except ValidationError as exc:
        return _error_response(_validation_error_dict(exc))
    return JsonResponse(_region_to_dict(region), status=201)


@admin_required
@require_http_methods(['GET', 'PUT', 'DELETE'])
def region_detail(request, pk):
    try:
        region = Region.objects.get(pk=pk)
    except Region.DoesNotExist:
        return _not_found('Región')

    if request.method == 'GET':
        return JsonResponse(_region_to_dict(region))

    if request.method == 'DELETE':
        try:
            region.delete()
        except ProtectedError:
            return JsonResponse(
                {'detail': 'No se puede eliminar la región porque tiene biotopos asociados.'},
                status=409,
            )
        return JsonResponse({'detail': 'Región eliminada.'})

    data = _body(request)
    if data is None:
        return JsonResponse({'detail': 'JSON inválido.'}, status=400)

    region.name = (data.get('name') or '').strip()
    try:
        region.full_clean()
        region.save()
    except ValidationError as exc:
        return _error_response(_validation_error_dict(exc))
    return JsonResponse(_region_to_dict(region))


@admin_required
@require_http_methods(['GET', 'POST'])
def biotopes_collection(request):
    if request.method == 'GET':
        biotopes = Biotope.objects.select_related('region').order_by('region__name', 'name')
        return JsonResponse([_biotope_to_dict(biotope) for biotope in biotopes], safe=False)

    data = _body(request)
    if data is None:
        return JsonResponse({'detail': 'JSON inválido.'}, status=400)

    biotope = Biotope(name=(data.get('name') or '').strip())
    errors = _assign_biotope_region(biotope, data)
    try:
        biotope.full_clean()
        if not errors:
            biotope.save()
    except ValidationError as exc:
        _merge_errors(errors, exc)
    if errors:
        return _error_response(errors)
    return JsonResponse(_biotope_to_dict(biotope), status=201)


@admin_required
@require_http_methods(['GET', 'PUT', 'DELETE'])
def biotope_detail(request, pk):
    try:
        biotope = Biotope.objects.select_related('region').get(pk=pk)
    except Biotope.DoesNotExist:
        return _not_found('Biotopo')

    if request.method == 'GET':
        return JsonResponse(_biotope_to_dict(biotope))

    if request.method == 'DELETE':
        try:
            biotope.delete()
        except ProtectedError:
            return JsonResponse(
                {'detail': 'No se puede eliminar el biotopo porque tiene especies asociadas.'},
                status=409,
            )
        return JsonResponse({'detail': 'Biotopo eliminado.'})

    data = _body(request)
    if data is None:
        return JsonResponse({'detail': 'JSON inválido.'}, status=400)

    biotope.name = (data.get('name') or '').strip()
    errors = _assign_biotope_region(biotope, data)
    try:
        biotope.full_clean()
        if not errors:
            biotope.save()
    except ValidationError as exc:
        _merge_errors(errors, exc)
    if errors:
        return _error_response(errors)
    return JsonResponse(_biotope_to_dict(biotope))


def _assign_biotope_region(biotope, data):
    errors = {}
    region_id = data.get('region_id')
    if region_id in (None, ''):
        errors['region'] = ['Debes seleccionar una región.']
        return errors

    try:
        region = Region.objects.get(pk=region_id)
    except (Region.DoesNotExist, TypeError, ValueError):
        errors['region'] = ['La región seleccionada no existe.']
        return errors

    biotope.region = region
    return errors


@admin_required
@require_GET
def region_biotopes(request, pk):
    try:
        region = Region.objects.get(pk=pk)
    except Region.DoesNotExist:
        return _not_found('Región')

    biotopes = region.biotopes.order_by('name')
    return JsonResponse([_biotope_to_dict(biotope) for biotope in biotopes], safe=False)


SPECIES_FIELDS = [
    'common_name',
    'scientific_name',
    'kind',
    'temp_min',
    'temp_max',
    'ph_min',
    'ph_max',
    'gh_min',
    'gh_max',
    'adult_size_cm',
    'min_tank_liters',
    'min_group_size',
    'diet',
    'temperament',
    'swim_zone',
    'eats_plants',
    'fin_nipper',
    'territorial',
]


def _assign_species_biotope(species, data, is_new):
    errors = {}
    biotope_sent = 'biotope_id' in data or 'biotope' in data
    biotope_id = data.get('biotope_id', data.get('biotope'))

    if biotope_sent or is_new:
        if biotope_id in (None, ''):
            errors['biotope'] = ['El biotopo es obligatorio.']
            return errors
        try:
            biotope = Biotope.objects.select_related('region').get(pk=biotope_id)
        except (Biotope.DoesNotExist, TypeError, ValueError):
            errors['biotope'] = ['El biotopo seleccionado no existe.']
            return errors
        species.biotope = biotope

    region_id = data.get('region_id')
    if region_id not in (None, ''):
        try:
            region_id = int(region_id)
        except (TypeError, ValueError):
            errors['biotope'] = ['La región seleccionada no es válida.']
            return errors
        if species.biotope_id and species.biotope.region_id != region_id:
            errors['biotope'] = ['El biotopo no pertenece a la región seleccionada.']

    return errors


@admin_required
@require_http_methods(['GET', 'POST'])
def species_collection(request):
    if request.method == 'GET':
        species_list = Species.objects.select_related('biotope__region').all()
        return JsonResponse([_species_to_dict(item) for item in species_list], safe=False)

    data = _body(request)
    if data is None:
        return JsonResponse({'detail': 'JSON inválido.'}, status=400)

    species = Species()
    for field in SPECIES_FIELDS:
        if field in data:
            setattr(species, field, data[field])

    errors = _assign_species_biotope(species, data, is_new=True)
    try:
        species.full_clean()
        if not errors:
            species.save()
    except ValidationError as exc:
        _merge_errors(errors, exc)
    if errors:
        return _error_response(errors)
    return JsonResponse(_species_to_dict(species), status=201)


@admin_required
@require_http_methods(['GET', 'PUT', 'DELETE'])
def species_detail(request, pk):
    try:
        species = Species.objects.select_related('biotope__region').get(pk=pk)
    except Species.DoesNotExist:
        return _not_found('Especie')

    if request.method == 'GET':
        return JsonResponse(_species_to_dict(species))

    if request.method == 'DELETE':
        species.delete()
        return JsonResponse({'detail': 'Especie eliminada.'})

    data = _body(request)
    if data is None:
        return JsonResponse({'detail': 'JSON inválido.'}, status=400)

    for field in SPECIES_FIELDS:
        if field in data:
            setattr(species, field, data[field])

    errors = _assign_species_biotope(species, data, is_new=False)
    try:
        species.full_clean()
        if not errors:
            species.save()
    except ValidationError as exc:
        _merge_errors(errors, exc)
    if errors:
        return _error_response(errors)
    return JsonResponse(_species_to_dict(species))
