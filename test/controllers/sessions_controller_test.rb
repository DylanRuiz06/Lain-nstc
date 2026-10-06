require "test_helper"

class SessionsControllerTest < ActionDispatch::IntegrationTest
  setup { @user = users(:one) }

  test "new" do
    get new_session_path
    assert_response :success
  end

  test "login correcto redirige a root y crea sesión" do
    post session_path, params: { username: @user.username, password: "password" }

    assert_redirected_to root_path
    assert cookies[:session_id]
  end

  test "login incorrecto muestra error y no crea sesión" do
    post session_path, params: { username: @user.username, password: "wrong" }

    assert_redirected_to new_session_path
    assert_nil cookies[:session_id]

    follow_redirect!
    assert_select "div", /Usuario o contraseña incorrectos/
  end

  test "tras login vuelve a la URL que se intentaba visitar" do
    get tarea_url(tareas(:one))
    assert_redirected_to new_session_path

    post session_path, params: { username: @user.username, password: "password" }
    assert_redirected_to tarea_url(tareas(:one))
  end

  test "logout cierra la sesión" do
    sign_in_as(@user)

    delete session_path

    assert_redirected_to new_session_path
    assert_empty cookies[:session_id]
  end
end
