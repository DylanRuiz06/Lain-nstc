# Lain

Lain es un planificador de acuarios para principiantes. Su núcleo es un motor de
compatibilidad entre especies que necesita un catálogo con datos biológicos
correctos. Este repositorio contiene el **panel de administración** que alimenta
ese catálogo.

## Qué administra el panel

- **Regiones** → **Biotopos** → **Especies** (jerarquía con claves foráneas).
- Especies con sus parámetros biológicos: temperatura, pH, GH, tamaño adulto,
  litros mínimos, grupo mínimo, dieta, temperamento, zona de natación y
  comportamiento.
- Todos los formularios usan dropdowns para las relaciones: la región de un
  biotopo y la región + biotopo de una especie. Nunca se escribe un ID a mano.

## Validaciones en back-end

Las reglas de los datos sensibles de `Species` viven en `Species.clean()` y se
ejecutan con `full_clean()` antes de guardar desde la API:

- `ph_min <= ph_max`, ambos entre 0 y 14.
- `temp_min < temp_max`, ambos entre 0 y 40 °C.
- `gh_min <= gh_max` y `gh_min >= 0`.
- `adult_size_cm > 0`, `min_tank_liters > 0`, `min_group_size >= 1`.
- `scientific_name` único, con mensaje claro.
- El biotopo debe existir; si se envía `region_id`, debe pertenecer a esa región.

Cuando falla, la API responde `400` con
`{"errors": {"campo": ["mensaje"], "__all__": ["mensaje"]}}` y Vue muestra los
mensajes junto a cada campo. No hay reglas de rango duplicadas en JavaScript.

## Dropdown dependiente

En el formulario de especie, al elegir una región se consulta
`GET /api/regions/<id>/biotopes/` y se recarga el select de biotopos. Al editar,
primero se carga la especie, se deduce su región desde el biotopo, se cargan los
biotopos de esa región y recién entonces se selecciona el biotopo guardado.

## Autenticación

Sesiones de Django + CSRF + CORS. Solo usuarios con `is_staff=True` pueden usar
el panel. Los endpoints de administración responden `401` sin sesión y `403` si
el usuario no es staff (decorador `admin_required`). El guard de Vue solo mejora
la experiencia; la seguridad real está en Django.

## Requisitos

- Python 3.12 o superior (probado con Python 3.14 y Django 6.0.6).
- Node.js 18 o superior y npm.

## Ejecutar en local

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_admin        # admin / admin12345 por defecto (solo desarrollo)
python manage.py seed_data         # regiones, biotopos y especies de ejemplo
python manage.py runserver         # http://localhost:8000
```

Para usar otra contraseña de administrador:

```bash
ADMIN_PASSWORD=mi_clave_segura python manage.py seed_admin
```

### Frontend

En otra terminal:

```bash
cd frontend
npm install
npm run dev                        # http://localhost:5173
```

Vite redirige `/api` a `http://localhost:8000` (ver `vite.config.js`), así que el
navegador trabaja contra rutas relativas `/api/...` y las cookies de sesión y
CSRF funcionan sin problemas. CORS y `CSRF_TRUSTED_ORIGINS` también están
configurados para `http://localhost:5173`.

## Deploy en Render

Render ejecuta **un solo servicio web**: Django sirve la API y el build de Vue
(WhiteNoise entrega los assets de `frontend/dist` y una vista catch-all devuelve
`index.html` para que Vue Router funcione al recargar).

Crea un **Web Service** apuntando a este repositorio con:

- **Build Command**: `./build.sh`
- **Start Command**:
  ```bash
  cd backend && python manage.py seed_admin && python manage.py seed_data && gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
  ```

`build.sh` instala las dependencias de Node, compila Vue, instala las
dependencias de Python, ejecuta `collectstatic` y aplica las migraciones.

El cliente de Vue llama rutas relativas `/api/...`, así que el login, el token
CSRF y las cookies de sesión funcionan en el mismo origen del servicio (no hace
falta CORS en producción).

### Variables de entorno

| Variable | Valor de ejemplo | Notas |
| --- | --- | --- |
| `DEBUG` | `0` | Obligatorio en producción. Con `0` se activan `SESSION_COOKIE_SECURE` y `CSRF_COOKIE_SECURE`. |
| `SECRET_KEY` | cadena larga y aleatoria | No reutilizar el valor de desarrollo. |
| `ADMIN_PASSWORD` | contraseña segura | Contraseña del usuario `admin`. **Nunca se sube a Git**; se define en el panel de Render (Environment). |
| `ALLOWED_HOSTS` | `lain.onrender.com` | Dominio(s) del servicio, separados por coma. |
| `CSRF_TRUSTED_ORIGINS` | `https://lain.onrender.com` | Origen(es) con esquema, separados por coma. |

> **ADVERTENCIA:** el disco de SQLite en Render es efímero. **Los datos se
> reinician en cada redeploy.** Por eso `seed_admin` y `seed_data` son
> idempotentes y se ejecutan en cada arranque: recrean el admin y los datos de
> ejemplo sin duplicarlos. Para conservar datos reales habría que migrar a una
> base de datos gestionada y un disco persistente.

## Estructura

```text
lain/
├── backend/
│   ├── config/        # settings y urls del proyecto Django
│   ├── catalog/       # modelos, vistas, urls y comandos seed
│   └── manage.py
├── frontend/
│   ├── src/
│   │   ├── views/     # login, listas y formularios
│   │   ├── api.js     # fetch con credentials + CSRF
│   │   └── router/    # rutas y guard
│   └── vite.config.js
├── build.sh           # build de Vue + collectstatic + migrate (Render)
└── README.md
```

## Fuera de alcance

No se incluyen colores de especies, temas visuales, relaciones entre especies ni
generación de setups. El panel solo mantiene el catálogo que usará el core.
