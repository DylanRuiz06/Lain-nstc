# Usuario inicial para desarrollo. La contraseña puede sobreescribirse con
# la variable de entorno SEED_ADMIN_PASSWORD para no dejar credenciales reales en el repo.
admin_password = ENV.fetch("SEED_ADMIN_PASSWORD", "password123")

User.find_or_create_by!(username: "admin") do |user|
  user.password = admin_password
  user.password_confirmation = admin_password
end
