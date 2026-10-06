class TareasController < ApplicationController
  before_action :set_tarea, only: %i[ show edit update destroy ]

  # GET /tareas or /tareas.json
  def index
    @tareas = Tarea.all
  end

  # GET /tareas/1 or /tareas/1.json
  def show
  end

  # GET /tareas/new
  def new
    @tarea = Tarea.new
  end

  # GET /tareas/1/edit
  def edit
  end

  # POST /tareas or /tareas.json
  def create
    @tarea = Tarea.new(tarea_params)

    respond_to do |format|
      if @tarea.save
        format.html { redirect_to @tarea, notice: "Tarea was successfully created." }
        format.json { render :show, status: :created, location: @tarea }
      else
        format.html { render :new, status: :unprocessable_content }
        format.json { render json: @tarea.errors, status: :unprocessable_content }
      end
    end
  end

  # PATCH/PUT /tareas/1 or /tareas/1.json
  def update
    respond_to do |format|
      if @tarea.update(tarea_params)
        format.html { redirect_to @tarea, notice: "Tarea was successfully updated.", status: :see_other }
        format.json { render :show, status: :ok, location: @tarea }
      else
        format.html { render :edit, status: :unprocessable_content }
        format.json { render json: @tarea.errors, status: :unprocessable_content }
      end
    end
  end

  # DELETE /tareas/1 or /tareas/1.json
  def destroy
    @tarea.destroy!

    respond_to do |format|
      format.html { redirect_to tareas_path, notice: "Tarea was successfully destroyed.", status: :see_other }
      format.json { head :no_content }
    end
  end

  private
    # Use callbacks to share common setup or constraints between actions.
    def set_tarea
      @tarea = Tarea.find(params.expect(:id))
    end

    # Only allow a list of trusted parameters through.
    def tarea_params
      params.expect(tarea: [ :titulo, :hecha ])
    end
end
