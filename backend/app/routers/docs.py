# app/routers/docs.py
from fastapi import APIRouter, HTTPException
from app.services.ai_service import ai_service
from app.services.evaluation_service import evaluation_service

router = APIRouter()

@router.post("/generate-function-doc")
async def generate_function_documentation(request: dict):
    """
    Generate documentation for a function with quality evaluation
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
        
        # Évaluer la qualité
        evaluation = evaluation_service.evaluate_docstring(documentation, request['function_code'])
        
        return {
            "documentation": documentation,
            "function_name": request['function_name'],
            "evaluation": evaluation,
            "success": True
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Documentation generation failed: {str(e)}")

@router.post("/generate-test")
async def generate_test(request: dict):
    """
    Generate test for a function with quality evaluation
    Expects: {'function_code': 'def func(...): ...', 'function_name': 'func'}
    """
    try:
        if 'function_code' not in request or 'function_name' not in request:
            raise HTTPException(status_code=400, detail="Missing function_code or function_name")
        
        test_code = ai_service.generate_test(
            request['function_code'], 
            request['function_name']
        )
        
        if test_code is None:
            raise HTTPException(status_code=500, detail="Test generation failed")
        
        # Évaluer la qualité
        evaluation = evaluation_service.evaluate_test(test_code, request['function_code'])
        
        return {
            "test_code": test_code,
            "function_name": request['function_name'],
            "evaluation": evaluation,
            "success": True
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Test generation failed: {str(e)}")