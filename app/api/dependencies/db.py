from app.infrastructure.db.session import SessionLocal

def get_db():
    """
    Genera una sesión de base de datos para cada petición.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()