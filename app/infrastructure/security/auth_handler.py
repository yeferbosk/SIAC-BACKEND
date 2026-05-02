import os
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.infrastructure.db.models import EmpleadoModel
from app.api.dependencies.db import get_db

# Configuración básica (Idealmente esto iría en .env)
SECRET_KEY = os.getenv("SECRET_KEY", "SIAC_SUPER_SECRET_KEY_2026")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 480 # 8 horas de sesión

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

import bcrypt

# --- Gestión de Contraseñas ---

def verify_password(plain_password: str, hashed_password: str):
    """
    Verifica si una contraseña en texto plano coincide con el hash almacenado.
    """
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def get_password_hash(password: str):
    """
    Genera un hash seguro a partir de una contraseña usando bcrypt.
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Genera un token JWT para un empleado.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Dependencia para validar el token y obtener el empleado actual.
    Inyecta el ID del usuario en la sesión de MySQL para auditoría.
    """
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar el token de acceso",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # 1. Decodificar Token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    # 2. Buscar usuario en DB
    user = db.query(EmpleadoModel).filter(EmpleadoModel.email == email).first()
    if user is None:
        raise credentials_exception
        
    # 3. Auditoría: Establecer el ID del usuario en la sesión de MySQL.
    # Usamos la conexión directa para asegurar que el trigger vea la variable.
    try:
        # Esto asegura que la variable se mantenga viva en la conexión actual
        db.execute(text("SET @usuario_id = :uid"), {"uid": user.id_empleado})
    except Exception as e:
        print(f"Error estableciendo @usuario_id: {e}")
        raise HTTPException(status_code=500, detail="Error de sesión de auditoría")
    
    return user
