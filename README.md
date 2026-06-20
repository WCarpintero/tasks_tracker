# Agenda Inteligente IA — Sistema de Gestión de Tareas con Asistente Conversacional

Este proyecto consiste en una **API de Gestión de Tareas con Priorización e Inteligencia Artificial Conversacional**, desarrollada como entrega para el curso de **Desarrollo de Aplicaciones Web II**. El sistema combina un potente backend robusto implementado en **FastAPI**, persistencia en la nube mediante **Supabase (PostgreSQL)**, procesamiento avanzado de lenguaje natural con el modelo de última generación **Google Gemini 2.5-Flash**, y una interfaz web interactiva premium (**Súper Dashboard**) servida con archivos estáticos de FastAPI.

El objetivo principal es ofrecer una solución integral (CRUD completo) potenciada por IA que no solo clasifique automáticamente la prioridad de las tareas del usuario según el texto, sino que además funcione como un asistente personal conversacional capaz de interpretar toda la agenda en tiempo real, dar consejos de productividad y reportar un diagnóstico proactivo de tareas pendientes al ingresar al sistema.

---

## 📋 Características Principales

### 🧠 Backend e Integración con IA
* **CRUD Completo de Tareas (Entity: `tasks`):** Operaciones completas para Crear, Leer, Actualizar y Eliminar registros mediante métodos HTTP estándares (`POST`, `GET`, `PUT`, `DELETE`).
* **Parámetros Extendidos:** Cada tarea incluye validaciones estrictas de datos usando **Pydantic V2** para campos esenciales: `id`, `title`, `description`, `status` (*pendiente* o *completado*), `priority` (*alta*, *media*, *baja*) y `due_date` (*fecha límite opcional*).
* **Endpoint de Clasificación de Prioridad (`/tasks/analyze`):** Envía el contenido de la tarea a la API de Google Gemini para retornar una sugerencia inteligente de prioridad (alta, media o baja) basada en la urgencia implícita del texto.
* **Endpoint de Asistente Personal Conversacional (`/chat`):** Un chatbot avanzado que inyecta automáticamente toda la lista de tareas almacenadas en Supabase como contexto dentro del prompt del modelo de lenguaje. Esto permite al asistente responder preguntas situacionales complejas como: *"¿Qué debería hacer primero hoy?"* o *"Dame un resumen de lo que tengo pendiente"*.

### 🎨 Frontend Interactivo (Súper Dashboard)
* **Interfaz de Usuario Monopágina (SPA):** Panel desarrollado de forma limpia con HTML5, JavaScript asíncrono (`fetch` API) y estilos basados en **Tailwind CSS** y **FontAwesome** (sin necesidad de instalaciones pesadas de node).
* **Notificación de Bienvenida Proactiva:** Al cargar la página, el sistema realiza una llamada automatizada y transparente al endpoint de chat solicitando un diagnóstico inicial. El asistente virtual recibe al usuario dándole los buenos días e informando de inmediato el estatus real de su agenda.
* **Sistema de Filtros Dinámicos:** Permite alternar instantáneamente la vista del listado entre *Todas las tareas*, *Pendientes* o *Completadas* en caliente.
* **Métricas y Rachas de Progreso:** Muestra indicadores en tiempo real de tareas pendientes, completadas y un contador interactivo de rachas (*días productivos*) para gamificar el cumplimiento de objetivos.
* **Interacción Dinámica entre Paneles:** Al marcar una tarea como completada ("Marcar Hecha"), el frontend dispara un mensaje automático al chat lateral y la IA responde felicitando efusivamente al usuario por su avance.

---

## 📂 Estructura Arquitectónica del Proyecto

El proyecto sigue una arquitectura limpia basada en la separación de responsabilidades solicitada en los estándares del curso:

```text
tasks_traking/
│
├── database/
│   └── supabase.py          # Inicialización y cliente de conexión con la BD en Supabase
│
├── routes/
│   └── tasks.py             # Definición de rutas y endpoints de la API (FastAPI Router)
│
├── schemas/
│   └── task_schema.py       # Modelos de validación de datos y tipado de negocio (Pydantic V2)
│
├── services/
│   └── ai_service.py        # Lógica de comunicación HTTP con la API de Google Gemini (httpx)
│
├── static/
│   └── index.html           # Interfaz gráfica premium (Súper Dashboard y Chat de Asistencia)
│
├── .env                     # Variables de entorno confidenciales (URLs, API Keys y credenciales)
├── .gitignore               # Archivo de exclusión para evitar la subida de claves secretas a Git
├── check_models.py          # Script de diagnóstico para validación de compatibilidad de modelos IA
├── main.py                  # Punto de entrada de la aplicación FastAPI y montaje de estáticos
└── requirements.txt         # Listado de dependencias y librerías del proyecto de Python

🛠️ Requerimientos del Sistema (Pre-requisitos)
Para poner a funcionar la aplicación correctamente en cualquier máquina local, asegúrese de contar con:

Python 3.10 o superior instalado en el sistema operativo (Desarrollado y probado bajo entornos Windows/Python 3.14).

Cuenta activa en Supabase (para la base de datos PostgreSQL en la nube).

Clave de API de Google AI Studio (completamente gratuita para el acceso al modelo gemini-2.5-flash).

Navegador web moderno (Chrome, Edge, Firefox, Brave).

🚀 Guía de Instalación y Configuración Paso a Paso
Siga estos pasos exactos en su terminal para levantar el entorno desde cero:

Paso 1: Clonación del repositorio y preparación de la carpeta
Abra su terminal o consola de comandos, ubíquese en su directorio de trabajo y acceda a la carpeta raíz del proyecto:

Bash
cd C:\wamp64\www\tasks_traking
Paso 2: Creación y activación del Entorno Virtual (venv)
Es fundamental aislar las dependencias del proyecto para evitar conflictos de librerías globales:

En Windows (PowerShell / CMD):

Bash
python -m venv venv
.\venv\Scripts\Activate
En Linux / macOS:

Bash
python3 -m venv venv
source venv/bin/activate
Una vez activado, verá el indicador (venv) al inicio de la línea de comandos.

Paso 3: Instalación de las Dependencias Oficiales
Instale las librerías necesarias ejecutando el gestor de paquetes de Python (pip):

Bash
pip install -r requirements.txt
Nota: Si no cuenta con el archivo requirements.txt, puede instalar las librerías directamente con el siguiente comando:

Bash
pip install fastapi uvicorn supabase httpx python-dotenv pydantic
Paso 4: Preparación de la Base de Datos en Supabase (Script SQL)
Acceda a su panel de control en Supabase, cree un nuevo proyecto o abra uno existente, diríjase a la sección SQL Editor y ejecute el siguiente query para construir la tabla con la estructura exacta de datos requerida por el esquema de la aplicación:

SQL
-- Creación de la tabla principal de tareas
CREATE TABLE tasks (
    id BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    title TEXT NOT NULL,
    description TEXT,
    status TEXT DEFAULT 'pendiente',
    priority TEXT DEFAULT 'media',
    due_date DATE
);

-- Habilitar permisos de lectura/escritura públicos para facilitar pruebas en entornos locales
ALTER TABLE tasks ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Permitir todo a usuarios anonimos" ON tasks FOR ALL USING (true) WITH CHECK (true);
Paso 5: Configuración de Variables de Entorno Seguras
Cree un archivo de texto plano en la raíz exacta del proyecto (al mismo nivel de main.py) con el nombre .env (asegúrese de que no termine en .txt). Configure las variables sin usar espacios ni comillas, sustituyendo los valores de ejemplo por sus credenciales reales:

Fragmento de código
SUPABASE_URL=[https://tu-proyecto-id.supabase.co](https://tu-proyecto-id.supabase.co)
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.tu_anon_key_copiada_de_supabase
GEMINI_API_KEY=AIzaSyTuClaveSecretaGratuitaCopiadaDesdeGoogleAIStudio
⚠️ REGLA DE ORO DE SEGURIDAD: El archivo .env contiene claves de acceso críticas. Por diseño del curso, este archivo NUNCA debe subirse a repositorios públicos como GitHub. Asegúrese de tener creado un archivo llamado .gitignore en la raíz que contenga la línea .env y la carpeta venv/.

💻 Ejecución del Servidor y Despliegue Local
Una vez completados los pasos previos, levante el servidor de desarrollo local utilizando Uvicorn con soporte de recarga automática en caliente (--reload):

Bash
uvicorn main:app --reload
Si todo está correcto, la terminal mostrará la salida confirmando el inicio exitoso:

Plaintext
INFO:     Uvicorn running on [http://127.0.0.1:8000](http://127.0.0.1:8000) (Press CTRL+C to quit)
INFO:     Started reloader process using WatchFiles
INFO:     Application startup complete.
📑 Manual de Uso y Pruebas Técnicas
El sistema ofrece dos vías complementarias e integradas para interactuar con sus funcionalidades:

1. Documentación del Backend Interactiva (Swagger UI)
FastAPI autogenera especificaciones OpenAPI en tiempo real. Puede probar cada endpoint de forma aislada ingresando desde su navegador a:
👉 http://127.0.0.1:8000/docs

Endpoints CRUD de Gestión Base:
POST /tasks: Crea un nuevo registro insertando el modelo de datos en Supabase.

GET /tasks: Retorna el arreglo completo de tareas de la base de datos.

GET /tasks/{id}: Busca y extrae una tarea específica filtrada por su identificador numérico único.

PUT /tasks/{id}: Modifica los parámetros de una tarea existente (útil para cambiar de estado o actualizar plazos).

DELETE /tasks/{id}: Remueve de forma permanente una fila de la tabla en Supabase.

Endpoints de Inteligencia Artificial Avanzada:
POST /tasks/analyze: Toma el contenido textual de una tarea y retorna una cadena simplificada (alta, media, baja) determinando su nivel de urgencia mediante Gemini.

POST /chat: El endpoint estrella conversacional. Acepta un cuerpo JSON con el atributo message. Lee todas las tareas actuales del usuario en Supabase, genera un string formateado de contexto, e instruye a Gemini actuar como asistente de productividad para resolver dudas personalizadas.

2. Panel Visual del Usuario (Súper Dashboard)
Diseñado para la demostración del usuario final y la presentación del video del proyecto. Ingrese a la siguiente URL desde el navegador:
👉 http://127.0.0.1:8000/static/index.html

Verificación de Bienvenida: Observe cómo el chat de la derecha carga automáticamente un resumen inteligente de sus tareas al entrar.

Agregar Tareas con Plazo: Ingrese un título, elija una fecha límite del calendario interactivo y presione "Añadir". Verá la tarjeta aparecer instantáneamente a la izquierda y el asistente emitirá un comentario automático sobre ella.

Ejecutar la Magia de la IA: Presione el botón de la varita mágica (✨) en cualquiera de las tarjetas. El botón mostrará un indicador de carga animado y, tras décimas de segundo, la tarjeta mutará de color automáticamente (Ej: Rojo si la IA detectó prioridad alta, o Amarillo si detectó prioridad media).

Marcar Hecho / Reabrir: Haga clic en "Marcar Hecha". El elemento se atenuará y se tachará visualmente, alterando los contadores de la parte superior del dashboard y disparando un mensaje de celebración en la consola del chatbot.

🛠️ Notas de Ingeniería y Solución de Problemas Comunes
Conflicto de Caché en Inicialización de Modelos (Error 500 Abriendo /docs)
Durante la fase de desarrollo, la recarga automática de Uvicorn puede provocar desincronizaciones en la caché de FastAPI al mapear esquemas dinámicos de Pydantic V2 que contienen tipos de datos temporales complejos (datetime.date). Esto suele manifestarse lanzando un error interno del servidor: pydantic.errors.PydanticUserError: TaskCreate is not fully defined.

Nuestra Solución Definitiva: El código del esquema (schemas/task_schema.py) implementa la directiva avanzada ConfigDict(from_attributes=True) propia de la nueva versión de Pydantic y fuerza el reprocesamiento inmediato de los grafos de los modelos invocando explícitamente las funciones de reconstrucción al final del archivo:

Python
TaskBase.model_rebuild()
TaskCreate.model_rebuild()
Task.model_rebuild()
Si se presentara alguna desincronización residual durante la edición de archivos, simplemente limpie la memoria deteniendo el proceso en la consola con Ctrl + C y vuelva a inicializar el comando uvicorn main:app --reload.