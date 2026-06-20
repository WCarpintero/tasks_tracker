from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles  
from routes.tasks import router as tasks_router

app = FastAPI(title="Gestión de Tareas con Priorización IA")

# Para poder abrir las vistas 
app.mount("/static", StaticFiles(directory="static"), name="static")

# Incluir las rutas de tareas
app.include_router(tasks_router)

@app.get("/")
def root():
    return {"message": "API de Gestión de Tareas funcionando correctamente"}