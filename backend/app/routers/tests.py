# app/routers/tests.py
from fastapi import APIRouter, HTTPException
from app.services.ai_service import ai_service

router = APIRouter()

@router.post("/generate-test")
async def generate_test_case(request: dict):
    """
    Generate a test case for a function
    Expects: {'function_code': 'def func(...): ...', 'function_name': 'func'}
    """
    try:
        if 'function_code' not in request:
            raise HTTPException(status_code=400, detail="No function code provided")
        
        function_name = request.get('function_name', 'unknown_function')
        test_code = ai_service.generate_test(
            request['function_code'], 
            function_name
        )
        
        return {
            "test_code": test_code,
            "function_name": function_name,
            "success": True
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Test generation failed: {str(e)}")