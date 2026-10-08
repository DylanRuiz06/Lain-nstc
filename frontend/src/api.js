// Cliente HTTP mínimo para hablar con Django usando sesiones + CSRF.
// - credentials: 'include' => el navegador envía la cookie de sesión.
// - Antes de cualquier POST/PUT/DELETE pedimos GET /api/csrf/ para que
//   Django emita la cookie csrftoken, y la devolvemos en X-CSRFToken.

function getCookie(name) {
  const m = document.cookie.match(new RegExp('(^|;\\s*)' + name + '=([^;]*)'))
  return m ? decodeURIComponent(m[2]) : ''
}

export async function ensureCsrf() {
  if (!getCookie('csrftoken')) {
    await fetch('/api/csrf/', { credentials: 'include' })
  }
}

async function request(path, options = {}) {
  const method = (options.method || 'GET').toUpperCase()
  if (['POST', 'PUT', 'DELETE'].includes(method)) {
    await ensureCsrf()
  }
  const res = await fetch(path, {
    ...options,
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken'),
      ...(options.headers || {}),
    },
  })
  let data = null
  try {
    data = await res.json()
  } catch {
    data = null
  }
  if (!res.ok) {
    const msg = (data && data.detail) || `Error ${res.status}`
    throw new Error(Array.isArray(msg) ? msg.join(' ') : msg)
  }
  return data
}

export const api = {
  register: (payload) => request('/api/register/', { method: 'POST', body: JSON.stringify(payload) }),
  login: (payload) => request('/api/login/', { method: 'POST', body: JSON.stringify(payload) }),
  logout: () => request('/api/logout/', { method: 'POST' }),
  me: () => request('/api/me/'),
  listUsers: () => request('/api/users/'),
  getUser: (id) => request(`/api/users/${id}/`),
  createUser: (payload) => request('/api/users/', { method: 'POST', body: JSON.stringify(payload) }),
  updateUser: (id, payload) => request(`/api/users/${id}/`, { method: 'PUT', body: JSON.stringify(payload) }),
  deleteUser: (id) => request(`/api/users/${id}/`, { method: 'DELETE' }),
}
