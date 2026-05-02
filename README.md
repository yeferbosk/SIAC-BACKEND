# 🚀 SIAC - Sistema Inteligente de Automatización Comercial

¡Bienvenido al backend de **SIAC**! El motor que impulsa la gestión inteligente de transformadores para **Induelectro**. Este proyecto está construido con **FastAPI** y sigue una **Arquitectura Hexagonal** (Ports & Adapters) para ser tan sólido como un transformador de alta potencia. ⚡

---

## 🛠️ Tech Stack

*   **Framework:** [FastAPI](https://fastapi.tiangolo.com/) (Rápido, moderno y con documentación automática).
*   **ORM:** [SQLAlchemy](https://www.sqlalchemy.org/) (Para hablar con la base de datos como un profesional).
*   **Base de Datos:** MySQL (Robusta y confiable).
*   **Arquitectura:** Hexagonal (Separación total de lógica de negocio e infraestructura).

---

## 🏁 ¡Arranca el Proyecto en 3 Pasos!

Sigue estas instrucciones para tener el servidor volando en tu máquina local.

### 1. Clonar y Preparar el Terreno 🏗️

```bash
# Clona el repositorio
git clone https://github.com/yeferbosk/SIAC-BACKEND.git
cd SIAC-BACKEND
```

### 2. El Entorno Virtual (Tu zona segura) 🛡️

Es vital usar un entorno virtual para no mezclar las librerías del proyecto con las de tu sistema.

**En Windows:**
```powershell
# Crear el entorno
python -m venv venv

# Activar el entorno
.\venv\Scripts\activate
```

**En Linux/Mac:**
```bash
# Crear el entorno
python3 -m venv venv

# Activar el entorno
source venv/bin/activate
```

### 3. Instalar Dependencias y ¡Goooo! 🏎️💨

```bash
# Instala todo lo necesario
pip install fastapi uvicorn sqlalchemy pymysql email-validator python-dotenv

# Lanza el servidor
uvicorn app.main:app --reload
```

---

## ⚙️ Configuración (Archivo .env)

Asegúrate de tener un archivo `.env` en la raíz del proyecto con tus credenciales de MySQL:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=tu_usuario
DB_PASSWORD=tu_password
DB_NAME=siac_db
```

---

## 📖 Documentación Interactiva

Una de las mejores cosas de FastAPI es que la documentación se escribe sola. Una vez que el servidor esté corriendo, visita:

*   **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) (Para probar los endpoints directamente).
*   **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) (Una vista más limpia de la API).

---

## 🏗️ Estructura del Proyecto

```text
app/
├── api/             # Adaptadores de entrada (Rutas y Schemas)
├── application/     # Casos de uso (Lógica de la aplicación)
├── domain/          # El corazón (Entidades y Puertos/Interfaces)
└── infrastructure/  # Adaptadores de salida (DB, Repositorios, Twilio)
```

---

## 🤝 Contribuir

¿Viste un cable suelto o quieres mejorar la potencia? 
1. Haz un Fork.
2. Crea tu rama: `git checkout -b feature/NuevaMejora`.
3. Haz un commit: `git commit -m "Añadida nueva funcionalidad"`.
4. ¡Envía un Pull Request!

---

Hecho con ❤️ por el equipo de **Induelectro**.
