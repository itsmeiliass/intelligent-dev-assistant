# app/services/benchmark_service.py
import time
import asyncio
from typing import Dict, List, Any
from datetime import datetime
import json
from pathlib import Path
import numpy as np

class BenchmarkService:
    def __init__(self):
        self.benchmark_data = []
        self.benchmark_dir = Path("benchmarks")
        self.benchmark_dir.mkdir(exist_ok=True)
    
    async def run_comprehensive_benchmark(self, code_samples: List[Dict]) -> Dict[str, Any]:
        """
        Exécute un benchmark complet sur plusieurs échantillons de code
        """
        results = {
            "timestamp": datetime.now().isoformat(),
            "total_samples": len(code_samples),
            "results": []
        }
        
        for sample in code_samples:
            sample_result = await self._benchmark_single_sample(sample)
            results["results"].append(sample_result)
        
        # Calcul des statistiques globales
        results["summary"] = self._calculate_summary_statistics(results["results"])
        
        # Sauvegarde des résultats
        self._save_benchmark_results(results)
        
        return results
    
    async def _benchmark_single_sample(self, sample: Dict) -> Dict[str, Any]:
        """Benchmark un seul échantillon de code"""
        code = sample.get("code", "")
        function_name = sample.get("function_name", "unknown")
        
        start_time = time.time()
        
        # Test de génération de documentation
        doc_start = time.time()
        from app.services.ai_service import ai_service
        documentation = ai_service.generate_documentation(code, function_name)
        doc_time = time.time() - doc_start
        
        # Test de génération de tests
        test_start = time.time()
        test_code = ai_service.generate_test(code, function_name)
        test_time = time.time() - test_start
        
        # Évaluation de la qualité
        from app.services.evaluation_service import evaluation_service
        doc_quality = evaluation_service.evaluate_docstring(documentation, code)
        test_quality = evaluation_service.evaluate_test(test_code, code)
        
        total_time = time.time() - start_time
        
        return {
            "function_name": function_name,
            "code_length": len(code),
            "timing": {
                "total_seconds": total_time,
                "documentation_seconds": doc_time,
                "test_generation_seconds": test_time
            },
            "quality_metrics": {
                "documentation_score": doc_quality["score"],
                "test_score": test_quality["score"]
            },
            "success": True
        }
    
    def _calculate_summary_statistics(self, results: List[Dict]) -> Dict[str, Any]:
        """Calcule les statistiques de benchmark"""
        doc_scores = [r["quality_metrics"]["documentation_score"] for r in results if r["success"]]
        test_scores = [r["quality_metrics"]["test_score"] for r in results if r["success"]]
        doc_times = [r["timing"]["documentation_seconds"] for r in results if r["success"]]
        test_times = [r["timing"]["test_generation_seconds"] for r in results if r["success"]]
        
        return {
            "documentation": {
                "average_score": np.mean(doc_scores) if doc_scores else 0,
                "median_score": np.median(doc_scores) if doc_scores else 0,
                "std_dev_score": np.std(doc_scores) if doc_scores else 0,
                "average_time_seconds": np.mean(doc_times) if doc_times else 0
            },
            "test_generation": {
                "average_score": np.mean(test_scores) if test_scores else 0,
                "median_score": np.median(test_scores) if test_scores else 0,
                "std_dev_score": np.std(test_scores) if test_scores else 0,
                "average_time_seconds": np.mean(test_times) if test_times else 0
            },
            "success_rate": sum(1 for r in results if r["success"]) / len(results) if results else 0
        }
    
    def _save_benchmark_results(self, results: Dict):
        """Sauvegarde les résultats de benchmark"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.benchmark_dir / f"benchmark_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
    
    def get_historical_benchmarks(self, limit: int = 10) -> List[Dict]:
        """Récupère les benchmarks historiques"""
        benchmark_files = sorted(self.benchmark_dir.glob("benchmark_*.json"), reverse=True)
        results = []
        
        for file in benchmark_files[:limit]:
            try:
                with open(file, 'r') as f:
                    data = json.load(f)
                    results.append(data)
            except:
                continue
        
        return results

# Instance globale
benchmark_service = BenchmarkService()