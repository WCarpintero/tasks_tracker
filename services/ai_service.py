import httpx
import os
from dotenv import load_dotenv

load_dotenv()

def analyze_task_priority(content: str):
    api_key = os.getenv("GEMINI_API_KEY")
    url = furl = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    
    prompt = f"Analiza esta tarea y dime si su prioridad es 'alta', 'media' o 'baja' basándote en el texto: '{content}'. Responde solo con una palabra."
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    
    try:
        # Usamos httpx para realizar la petición asíncrona o síncrona
        response = httpx.post(url, json=payload, timeout=10.0)
        if response.status_code == 200:
            result = response.json()
            priority = result["candidates"][0]["content"]["parts"][0]["text"].strip().lower()
            return priority
        return "media"  # Fallback si falla la API
    except Exception:
        return "media" # Fallback en caso de error de conexión
    
def chat_with_assistant(user_message: str, tasks_context: list):
    api_key = os.getenv("GEMINI_API_KEY")
    
    # 1. Verificamos si la clave se está leyendo del .env
    if not api_key:
        return "Error: No se encontró la GEMINI_API_KEY. Revisa tu archivo .env"
        
    url = furl = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    
    # Usamos .get() por si alguna tarea antigua no tiene los campos completos
    context = "\n".join([f"- {t.get('title', 'Sin título')} (Estado: {t.get('status', 'N/A')}, Prioridad: {t.get('priority', 'N/A')})" for t in tasks_context])
    
    prompt = f"""Eres un asistente virtual experto en productividad. 
    Aquí está la lista actual de tareas de tu usuario:
    {context}
    
    El usuario te dice: "{user_message}"
    Responde de forma conversacional, amigable, breve y motivadora."""
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    
    try:
        response = httpx.post(url, json=payload, timeout=15.0)
        if response.status_code == 200:
            result = response.json()
            return result["candidates"][0]["content"]["parts"][0]["text"].strip()
        
        # 2. Si falla, devolvemos el error exacto que da Google
        return f"Error de Google ({response.status_code}): {response.text}"
    except Exception as e:
        return f"Error interno del servidor: {str(e)}"