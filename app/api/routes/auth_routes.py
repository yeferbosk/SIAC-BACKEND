from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from datetime import timedelta
from app.api.dependencies.db import get_db
from app.infrastructure.db.models import EmpleadoModel
from app.infrastructure.security.auth_handler import (
    create_access_token, 
    ACCESS_TOKEN_EXPIRE_MINUTES,
    verify_password
)

router = APIRouter(prefix="/auth", tags=["Autenticación"])

# Esquema de datos para la solicitud de inicio de sesión
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

@router.post("/login")
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Login con email y password vía JSON. Retorna JWT con rol y nombre.
    """
    # 1. Buscar al empleado por email
    user = db.query(EmpleadoModel).filter(EmpleadoModel.email == login_data.email).first()

    # 2. Validar existencia y contraseña
    if not user or not verify_password(login_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.activo:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Cuenta de empleado desactivada",
        )

    # 3. Crear Token con información extendida
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": user.email, 
            "id": user.id_empleado,
            "rol": user.rol,
            "nombre": user.nombre
        },
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}
