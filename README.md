# Lain

Aplicación web para gestionar usuarios, con un frontend moderno y una API backend preparada para crecer hacia la planificación de acuarios. 🐠

## 🎬 Video

Mira el video del proyecto en YouTube:

▶️ [Ver video de Lain](https://youtu.be/03yrmhcbDz8)

## 🛠️ Tecnologías

### Frontend

- 🟢 [Vue 3](https://vuejs.org/)
- ⚡ [Vite](https://vite.dev/)
- 🧭 [Vue Router](https://router.vuejs.org/)
- 📦 Node.js y npm

### Backend

- 🐍 [Python](https://www.python.org/)
- 🎸 [Django 6](https://www.djangoproject.com/)
- 🔐 Django Sessions, CSRF y CORS
- 🗃️ SQLite

## 📋 Requisitos

- Node.js 18 o superior
- npm
- Python 3.12 o superior

## 🚀 Cómo levantar el proyecto

Clona el repositorio y entra en la carpeta del proyecto:

```bash
git clone <URL_DEL_REPOSITORIO>
cd lain
```

### 1. Levantar el backend

Abre una terminal y ejecuta:

```bash
cd backend
python -m venv venv
```

Activa el entorno virtual:

**Linux/macOS**

```bash
source venv/bin/activate
```

**Windows PowerShell**

```powershell
venv\Scripts\Activate.ps1
```

Instala las dependencias y ejecuta las migraciones:

```bash
pip install -r requirements.txt
python manage.py migrate
```

Inicia el servidor Django:

```bash
python manage.py runserver
```

El backend estará disponible en `http://127.0.0.1:8000`.

### 2. Levantar el frontend

En otra terminal, desde la raíz del proyecto:

```bash
cd frontend
npm install
npm run dev
```

Abre la aplicación en [http://localhost:5173](http://localhost:5173).

El servidor de Vite redirige las peticiones `/api` hacia Django mediante el proxy configurado en `vite.config.js`.

## 📦 Comandos disponibles

### Frontend

```bash
npm run dev      # Servidor de desarrollo
npm run build    # Compilación para producción
npm run preview  # Vista previa de la compilación
```

### Backend

```bash
python manage.py runserver  # Servidor de desarrollo
python manage.py migrate     # Aplicar migraciones
python manage.py createsuperuser  # Crear usuario administrador
```

## 📁 Estructura principal

```text
lain/
├── backend/          # API y lógica de Django
│   ├── config/       # Configuración del proyecto
│   ├── users/        # Gestión de usuarios
│   └── manage.py
├── frontend/         # Aplicación Vue
│   ├── src/
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## 🔮 Próximamente: planificador de acuarios

La evolución prevista de Lain es convertirse en un planificador inteligente para acuarios. 🐟 🐸 🌿

El objetivo es ayudar a crear setups equilibrados y compatibles mediante:

- 🐠 Preparación de setups para peces.
- 🐸 Planificación de espacios para anfibios.
- 🌱 Selección y organización de plantas.
- ⚖️ Recomendaciones basadas en compatibilidad, tamaño y necesidades de cada especie.
- ➕ Posibilidad de agregar nuevas especies al catálogo.
- 📊 Organización de los habitantes, plantas, equipamiento y condiciones del acuario.

## 📄 Licencia

Este proyecto se encuentra en desarrollo.
