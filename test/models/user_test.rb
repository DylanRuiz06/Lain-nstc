require "test_helper"

class UserTest < ActiveSupport::TestCase
  test "normaliza username a minúsculas y sin espacios" do
    user = User.new(username: "  Admin ", password: "password123")
    assert_equal("admin", user.username)
  end

  test "username es obligatorio y único" do
    assert_not User.new(password: "password123").valid?

    User.create!(username: "unico", password: "password123")
    duplicado = User.new(username: "UNICO ", password: "password123")
    assert_not duplicado.valid?
  end
end
