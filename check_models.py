import httpx
import os
from dotenv import load_dotenv

# Cargar la clave del .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# URL para listar los modelos
url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"

print("Consultando modelos disponibles en Google Gemini...")
response = httpx.get(url)

if response.status_code == 200:
    data = response.json()
    print("\n¡Éxito! Estos son los modelos que puedes usar para generar texto:")
    for model in data.get("models", []):
        # Filtramos solo los que sirven para generar texto (generateContent)
        if "generateContent" in model.get("supportedGenerationMethods", []):
            print(f"✅ {model['name'].replace('models/', '')}")
else:
    print(f"\nError al consultar: {response.status_code}")
    print(response.text)