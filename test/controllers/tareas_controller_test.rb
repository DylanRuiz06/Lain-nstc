require "test_helper"

class TareasControllerTest < ActionDispatch::IntegrationTest
  setup do
    @tarea = tareas(:one)
    sign_in_as(users(:one))
  end

  test "should get index" do
    get tareas_url
    assert_response :success
  end

  test "should get new" do
    get new_tarea_url
    assert_response :success
  end

  test "should create tarea" do
    assert_difference("Tarea.count") do
      post tareas_url, params: { tarea: { hecha: @tarea.hecha, titulo: @tarea.titulo } }
    end

    assert_redirected_to tarea_url(Tarea.last)
  end

  test "should show tarea" do
    get tarea_url(@tarea)
    assert_response :success
  end

  test "should get edit" do
    get edit_tarea_url(@tarea)
    assert_response :success
  end

  test "should update tarea" do
    patch tarea_url(@tarea), params: { tarea: { hecha: @tarea.hecha, titulo: @tarea.titulo } }
    assert_redirected_to tarea_url(@tarea)
  end

  test "should destroy tarea" do
    assert_difference("Tarea.count", -1) do
      delete tarea_url(@tarea)
    end

    assert_redirected_to tareas_url
  end

  test "sin sesión redirige al login" do
    sign_out

    get tareas_url
    assert_redirected_to new_session_path
  end

  test "root requiere sesión y con sesión muestra tareas" do
    sign_out

    get root_url
    assert_redirected_to new_session_path

    sign_in_as(users(:one))
    get root_url
    assert_response :success
  end
end
