from fastapi import FastAPI
from app.api.routes.cliente_routes import router as cliente_router
from app.api.routes.empleado_routes import router as empleado_router
from app.api.routes.transformador_routes import router as transformador_router
from app.api.routes.pedido_routes import router as pedido_router

app = FastAPI(title="SIAC API - Sistema Inteligente de Automatización Comercial")

app.include_router(cliente_router)
app.include_router(empleado_router)
app.include_router(transformador_router)
app.include_router(pedido_router)


@app.get("/")
def root():
    return {
        "message": "SIAC API funcionando 🚀",
        "docs": "/docs"
    }