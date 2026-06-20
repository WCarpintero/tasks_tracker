from fastapi import APIRouter, HTTPException
from database.supabase import supabase
from typing import List

from schemas.task_schema import TaskCreate, Task, ChatMessage
from services.ai_service import analyze_task_priority, chat_with_assistant

router = APIRouter()

@router.post("/tasks", response_model=Task, summary="Crear una nueva tarea")
def create_task(task: TaskCreate):
    response = supabase.table("tasks").insert(task.model_dump()).execute()
    if not response.data:
        raise HTTPException(status_code=400, detail="Error al crear la tarea")
    return response.data[0]

@router.get("/tasks", response_model=List[Task], summary="Obtener lista de tareas")
def get_tasks():
    response = supabase.table("tasks").select("*").execute()
    return response.data

@router.get("/tasks/{id}", response_model=Task, summary="Obtener tarea por ID")
def get_task(id: int):
    response = supabase.table("tasks").select("*").eq("id", id).single().execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return response.data

@router.put("/tasks/{id}", response_model=Task, summary="Actualizar una tarea")
def update_task(id: int, task: TaskCreate):
    response = supabase.table("tasks").update(task.model_dump()).eq("id", id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Error al actualizar")
    return response.data[0]

@router.delete("/tasks/{id}", summary="Eliminar una tarea")
def delete_task(id: int):
    response = supabase.table("tasks").delete().eq("id", id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Error al eliminar")
    return {"message": "Tarea eliminada correctamente"}

@router.post("/tasks/analyze", summary="Analizar prioridad con IA")
def analyze_task(task_content: str):
    priority = analyze_task_priority(task_content)
    return {"content": task_content, "priority": priority}

@router.post("/chat", summary="Hablar con el Asistente IA")
def chat_assistant(chat_input: ChatMessage):
    # 1. Obtener todas las tareas de la base de datos para dárselas como contexto
    response = supabase.table("tasks").select("*").execute()
    current_tasks = response.data if response.data else []
    
    # 2. Enviar el mensaje del usuario y las tareas a Gemini
    ai_response = chat_with_assistant(chat_input.message, current_tasks)
    
    return {"response": ai_response}