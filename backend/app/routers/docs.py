# app/routers/docs.py
from fastapi import APIRouter, HTTPException
from app.services.ai_service import ai_service

router = APIRouter()

@router.post("/generate-function-doc")
async def generate_function_documentation(request: dict):
    """
    Generate documentation for a function
    Expects: {'function_code': 'def func(...): ...', 'function_name': 'func'}
    """
    try:
        if 'function_code' not in request or 'function_name' not in request:
            raise HTTPException(status_code=400, detail="Missing function_code or function_name")
        
        documentation = ai_service.generate_documentation(
            request['function_code'], 
            request['function_name']
        )
        
        if documentation is None:
            raise HTTPException(status_code=500, detail="Documentation generation failed")
        
        return {
            "documentation": documentation,
            "function_name": request['function_name'],
            "success": True
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Documentation generation failed: {str(e)}")