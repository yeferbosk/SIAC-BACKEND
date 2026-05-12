from fastapi import FastAPI, Depends
from app.api.routes.cliente_routes import router as cliente_router
from app.api.routes.empleado_routes import router as empleado_router
from app.api.routes.transformador_routes import router as transformador_router
from app.api.routes.pedido_routes import router as pedido_router
from app.api.routes.auth_routes import router as auth_router
from app.infrastructure.security.auth_handler import get_current_user

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="SIAC API - Sistema Inteligente de Automatización Comercial")

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro de Rutas
# Nota: auth_router es público para el login. Los demás requieren token JWT.
app.include_router(auth_router) 
app.include_router(cliente_router, dependencies=[Depends(get_current_user)])
app.include_router(empleado_router, dependencies=[Depends(get_current_user)])
app.include_router(transformador_router, dependencies=[Depends(get_current_user)])
app.include_router(pedido_router, dependencies=[Depends(get_current_user)])


@app.get("/")
def root():
    return {
        "message": "SIAC API funcionando 🚀",
        "docs": "/docs"
    }