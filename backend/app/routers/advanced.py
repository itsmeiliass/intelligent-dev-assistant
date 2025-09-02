# app/routers/advanced.py
from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.services.advanced_analysis import advanced_analysis_service
from app.services.benchmark_service import benchmark_service
from app.services.pattern_detection import pattern_detection_service
import asyncio

router = APIRouter()

@router.post("/advanced-analysis")
async def advanced_code_analysis(request: dict):
    """
    Advanced code quality analysis with multiple metrics
    Expects: {'code': 'code content', 'language': 'python'}
    """
    try:
        if 'code' not in request:
            raise HTTPException(status_code=400, detail="No code provided")
        
        language = request.get('language', 'python')
        analysis = advanced_analysis_service.analyze_code_quality(request['code'], language)
        
        return {
            "analysis": analysis,
            "language": language,
            "success": "error" not in analysis
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Advanced analysis failed: {str(e)}")

@router.post("/pattern-detection")
async def detect_code_patterns(request: dict):
    """
    Detect design patterns and anti-patterns in code
    Expects: {'code': 'code content', 'language': 'python'}
    """
    try:
        if 'code' not in request:
            raise HTTPException(status_code=400, detail="No code provided")
        
        language = request.get('language', 'python')
        patterns = pattern_detection_service.detect_patterns(request['code'], language)
        
        return {
            "patterns": patterns,
            "language": language,
            "success": "error" not in patterns
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pattern detection failed: {str(e)}")

@router.post("/run-benchmark")
async def run_benchmark(background_tasks: BackgroundTasks, request: dict):
    """
    Run comprehensive benchmark on code samples
    Expects: {'samples': [{'code': '...', 'function_name': '...'}, ...]}
    """
    try:
        if 'samples' not in request or not request['samples']:
            raise HTTPException(status_code=400, detail="No code samples provided")
        
        # Exécution asynchrone en arrière-plan
        background_tasks.add_task(
            benchmark_service.run_comprehensive_benchmark,
            request['samples']
        )
        
        return {
            "message": "Benchmark started in background",
            "sample_count": len(request['samples']),
            "success": True
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Benchmark failed: {str(e)}")

@router.get("/benchmark-results")
async def get_benchmark_results(limit: int = 5):
    """
    Get historical benchmark results
    """
    try:
        results = benchmark_service.get_historical_benchmarks(limit)
        
        return {
            "results": results,
            "count": len(results),
            "success": True
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get benchmark results: {str(e)}")