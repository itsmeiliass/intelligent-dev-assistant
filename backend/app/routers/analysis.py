# app/routers/analysis.py
from fastapi import APIRouter, HTTPException
from app.services.code_analysis import code_analysis_service

router = APIRouter()

@router.post("/analyze-python")
async def analyze_python_code(code: dict):
    """
    Analyze Python code and return its structure
    Expects: {'code': 'python code content'}
    """
    try:
        if 'code' not in code:
            raise HTTPException(status_code=400, detail="No code provided")
        
        analysis_result = code_analysis_service.parse_python_file(code['code'])
        summary = code_analysis_service.get_code_summary(analysis_result)
        
        return {
            'analysis': analysis_result,
            'summary': summary,
            'language': 'python'
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@router.post("/analyze-file")
async def analyze_code_file(analysis_request: dict):
    """
    Analyze a code file with specified language
    Expects: {'code': 'code content', 'language': 'python'}
    """
    try:
        if 'code' not in analysis_request or 'language' not in analysis_request:
            raise HTTPException(status_code=400, detail="Missing code or language field")
        
        # Map language to file extension
        language_extensions = {
            'python': '.py',
            'javascript': '.js',
            'java': '.java',
            'cpp': '.cpp'
        }
        
        file_extension = language_extensions.get(analysis_request['language'], '.txt')
        
        analysis_result = code_analysis_service.analyze_repository_file(
            analysis_request['code'], 
            file_extension
        )
        
        summary = code_analysis_service.get_code_summary(analysis_result)
        
        return {
            'analysis': analysis_result,
            'summary': summary,
            'language': analysis_request['language']
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")