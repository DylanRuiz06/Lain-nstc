json.extract! tarea, :id, :titulo, :hecha, :created_at, :updated_at
json.url tarea_url(tarea, format: :json)
