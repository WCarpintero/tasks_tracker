from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = "pendiente"
    priority: Optional[str] = "media"
    due_date: Optional[date] = None

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    
    # Forma correcta de hacerlo en Pydantic V2
    model_config = ConfigDict(from_attributes=True)

class ChatMessage(BaseModel):
    message: str

# Esto obliga a Pydantic a resolver cualquier problema de definición
TaskBase.model_rebuild()
TaskCreate.model_rebuild()
Task.model_rebuild()