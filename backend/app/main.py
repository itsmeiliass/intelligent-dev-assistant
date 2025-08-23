# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

# Import routers we will create in the next steps
from app.routers import github, analysis, docs, tests

# Initialize the FastAPI application
app = FastAPI(
    title="Intelligent Development Assistant API",
    description="API for AI-powered code analysis, documentation, and test generation.",
    version="0.1.0"
)

# Configure CORS (Important for frontend-backend communication)
# This allows your React frontend (which runs on a different port) to talk to this backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # The default port for Create-React-App
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Basic health check endpoint
@app.get("/")
async def root():
    return {"message": "Intelligent Development Assistant API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# We will add these lines later when we create the routers
app.include_router(github.router, prefix="/api/github", tags=["GitHub"])
app.include_router(analysis.router, prefix="/api/analysis", tags=["Analysis"])
app.include_router(docs.router, prefix="/api/docs", tags=["Documentation"])
app.include_router(tests.router, prefix="/api/tests", tags=["Tests"])

# This block allows us to run the app with `python -m uvicorn app.main:app --reload`
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)