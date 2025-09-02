# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

# Import routers - TOUS vos routers existants + le nouveau
from app.routers import github, analysis, docs, tests, refactor, advanced  # ✅ Ajout de 'advanced'

# Initialize the FastAPI application
app = FastAPI(
    title="Intelligent Development Assistant API",
    description="API for AI-powered code analysis, documentation, and test generation.",
    version="2.0"  # ✅ Version mise à jour
)

# Configure CORS - GARDEZ VOTRE CONFIGURATION EXISTANTE
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # ✅ Gardez votre config frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Basic health check endpoint - GARDEZ VOTRE ENDPOINT EXISTANT
@app.get("/")
async def root():
    return {"message": "Intelligent Development Assistant API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}


app.include_router(github.router, prefix="/api/github", tags=["GitHub"])
app.include_router(analysis.router, prefix="/api/analysis", tags=["Analysis"])
app.include_router(docs.router, prefix="/api/docs", tags=["Documentation"])
app.include_router(tests.router, prefix="/api/tests", tags=["Tests"])
app.include_router(refactor.router, prefix="/api/refactor", tags=["Refactoring"])


app.include_router(advanced.router, prefix="/api/advanced", tags=["Advanced Analysis"])


@app.get("/api/features")
async def get_features():
    """Retourne toutes les fonctionnalités disponibles"""
    return {
        "version": "2.0",
        "features": [
            {"name": "GitHub Integration", "path": "/api/github", "tags": ["GitHub"]},
            {"name": "Code Analysis", "path": "/api/analysis", "tags": ["Analysis"]},
            {"name": "Documentation Generation", "path": "/api/docs", "tags": ["Documentation"]},
            {"name": "Test Generation", "path": "/api/tests", "tags": ["Tests"]},
            {"name": "Code Refactoring", "path": "/api/refactor", "tags": ["Refactoring"]},
            {"name": "Advanced Analysis", "path": "/api/advanced", "tags": ["Advanced Analysis"]}
        ]
    }

@app.get("/api/metrics")
async def get_metrics():
    """Retourne les métriques globales de l'API"""
    return {
        "active_services": 6,  # ✅ Mise à jour avec le nouveau service
        "supported_languages": ["Python"],
        "ai_integration": "StarCoder2 Fine-tuned",
        "analysis_types": ["Basic", "Advanced", "Pattern", "Quality"],
        "performance": "High"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)