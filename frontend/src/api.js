// Cliente HTTP mínimo para la API de Django (sesiones + CSRF).
// La seguridad real (401/403, is_staff, validaciones) está en Django.

export class ApiError extends Error {
  constructor(message, status, data) {
    super(message)
    this.status = status
    this.data = data
  }
}

function getCookie(name) {
  const match = document.cookie.match(new RegExp('(^|;\\s*)' + name + '=([^;]*)'))
  return match ? decodeURIComponent(match[2]) : ''
}

async function ensureCsrf() {
  if (!getCookie('csrftoken')) {
    await fetch('/api/csrf/', { credentials: 'include' })
  }
}

function messageFromData(data, status) {
  if (!data) return `Error ${status}`
  if (data.errors) {
    return Object.values(data.errors).flat().join(' ')
  }
  return data.detail || `Error ${status}`
}

async function request(path, options = {}, { redirectOn401 = true } = {}) {
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

  if (res.status === 401 && redirectOn401 && window.location.pathname !== '/login') {
    window.location.assign('/login')
  }

  if (!res.ok) {
    throw new ApiError(messageFromData(data, res.status), res.status, data)
  }
  return data
}

export const api = {
  csrf: () => request('/api/csrf/'),
  login: (payload) => request('/api/login/', { method: 'POST', body: JSON.stringify(payload) }),
  logout: () => request('/api/logout/', { method: 'POST' }),
  me: () => request('/api/me/', {}, { redirectOn401: false }),

  listRegions: () => request('/api/regions/'),
  getRegion: (id) => request(`/api/regions/${id}/`),
  createRegion: (payload) => request('/api/regions/', { method: 'POST', body: JSON.stringify(payload) }),
  updateRegion: (id, payload) => request(`/api/regions/${id}/`, { method: 'PUT', body: JSON.stringify(payload) }),
  deleteRegion: (id) => request(`/api/regions/${id}/`, { method: 'DELETE' }),

  listBiotopes: () => request('/api/biotopes/'),
  getBiotope: (id) => request(`/api/biotopes/${id}/`),
  createBiotope: (payload) => request('/api/biotopes/', { method: 'POST', body: JSON.stringify(payload) }),
  updateBiotope: (id, payload) => request(`/api/biotopes/${id}/`, { method: 'PUT', body: JSON.stringify(payload) }),
  deleteBiotope: (id) => request(`/api/biotopes/${id}/`, { method: 'DELETE' }),
  biotopesByRegion: (id) => request(`/api/regions/${id}/biotopes/`),

  listSpecies: () => request('/api/species/'),
  getSpecies: (id) => request(`/api/species/${id}/`),
  createSpecies: (payload) => request('/api/species/', { method: 'POST', body: JSON.stringify(payload) }),
  updateSpecies: (id, payload) => request(`/api/species/${id}/`, { method: 'PUT', body: JSON.stringify(payload) }),
  deleteSpecies: (id) => request(`/api/species/${id}/`, { method: 'DELETE' }),
}
