# app/routers/refactor.py
from fastapi import APIRouter, HTTPException
from app.services.ai_service import ai_service

router = APIRouter()

@router.post("/refactor")
async def refactor_code(request: dict):
    """
    Refactor code to make it more efficient and readable
    Expects: {'code': 'code content', 'language': 'python'}
    """
    try:
        if 'code' not in request:
            raise HTTPException(status_code=400, detail="No code provided")
        
        language = request.get('language', 'python')
        refactored_code = ai_service.refactor_code(request['code'], language)
        
        return {
            "original_code": request['code'],
            "refactored_code": refactored_code,
            "language": language,
            "success": True
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Refactoring failed: {str(e)}")

@router.post("/explain")
async def explain_code(request: dict):
    """
    Explain code in natural language
    Expects: {'code': 'code content', 'language': 'python'}
    """
    try:
        if 'code' not in request:
            raise HTTPException(status_code=400, detail="No code provided")
        
        language = request.get('language', 'python')
        explanation = ai_service.explain_code(request['code'], language)
        
        return {
            "code": request['code'],
            "explanation": explanation,
            "language": language,
            "success": True
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Explanation failed: {str(e)}")