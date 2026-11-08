# Lain

Panel de administración del catálogo biológico de Lain, un planificador de
acuarios para principiantes.

**Versión desplegada:** https://lain-l8r9.onrender.com

## Funcionalidad

- Jerarquía **Regiones → Biotopos → Especies** con claves foráneas.
- CRUD de especies con temperatura, pH, GH, tamaño adulto, litros mínimos,
  grupo mínimo, dieta, temperamento, zona de natación y comportamiento.
- Dropdowns dependientes: al elegir región se cargan sus biotopos mediante
  `GET /api/regions/<id>/biotopes/`. Nunca se escribe un ID a mano.
- Login de administradores con sesiones de Django y CSRF.

## Validaciones

Las reglas de `Species` viven en `Species.clean()` y se ejecutan con
`full_clean()` antes de guardar:

- `ph_min <= ph_max`, entre 0 y 14.
- `temp_min < temp_max`, entre 0 y 40 °C.
- `gh_min <= gh_max` y `gh_min >= 0`.
- `adult_size_cm > 0`, `min_tank_liters > 0`, `min_group_size >= 1`.
- `scientific_name` único.
- El biotopo debe existir y pertenecer a la región indicada.

La API responde `400` con `{"errors": {"campo": ["mensaje"]}}`. No hay reglas
de rango duplicadas en JavaScript.

## Autenticación

Solo usuarios con `is_staff=True` usan el panel. Los endpoints de administración
responden `401` sin sesión y `403` si el usuario no es staff. El guard de Vue
solo mejora la experiencia; la seguridad real está en Django.

## Stack y requisitos

- Backend: Django 6.0.6 + SQLite, servido con Gunicorn.
- Frontend: Vue 3 + Vite + Vue Router.
- Python 3.12+ (probado con 3.14), Node.js 18+ y npm.

## Ejecutar en local

Backend:

```bash
cd backend
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_admin        # admin / admin12345 por defecto
python manage.py seed_data
python manage.py runserver         # http://localhost:8000
```

Para otra contraseña de administrador:

```bash
ADMIN_PASSWORD=mi_clave_segura python manage.py seed_admin
```

Frontend, en otra terminal:

```bash
cd frontend
npm install
npm run dev                        # http://localhost:5173
```

Vite redirige `/api` a `http://localhost:8000`, por lo que el navegador usa
rutas relativas `/api/...` y las cookies de sesión y CSRF funcionan en el mismo
origen.

## Deploy en Render

Render ejecuta un solo servicio web: Django sirve la API y el build de Vue.
WhiteNoise entrega los assets de `frontend/dist` y una vista catch-all devuelve
`index.html` para que Vue Router funcione al recargar.

- **Build Command:** `./build.sh`
- **Start Command:**

```bash
cd backend && python manage.py seed_admin && python manage.py seed_data && gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
```

`build.sh` compila Vue, instala dependencias de Python, ejecuta `collectstatic`
y aplica las migraciones.

### Variables de entorno

| Variable | Valor | Notas |
| --- | --- | --- |
| `DEBUG` | `0` | Activa `SESSION_COOKIE_SECURE` y `CSRF_COOKIE_SECURE`. |
| `SECRET_KEY` | cadena larga y aleatoria | No reutilizar el valor de desarrollo. |
| `ADMIN_PASSWORD` | contraseña segura | Nunca se sube a Git; se define en Render. |
| `ALLOWED_HOSTS` | `lain-l8r9.onrender.com` | Dominios separados por coma. |
| `CSRF_TRUSTED_ORIGINS` | `https://lain-l8r9.onrender.com` | Orígenes con esquema, separados por coma. |

**ADVERTENCIA:** el disco de SQLite en Render es efímero. Los datos se reinician
en cada redeploy. Por eso `seed_admin` y `seed_data` son idempotentes y se
ejecutan en cada arranque sin duplicar registros. Para conservar datos reales
habría que usar una base de datos gestionada y un disco persistente.

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
├── build.sh           # build de Vue + collectstatic + migrate
└── README.md
```

## Fuera de alcance

No se incluyen colores de especies, temas visuales, relaciones entre especies ni
generación de setups. El panel solo mantiene el catálogo que usará el core.
