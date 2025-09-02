# app/services/advanced_analysis.py
import ast
import radon
from radon.complexity import cc_visit
from radon.metrics import mi_visit
from radon.raw import analyze
import lizard
from typing import Dict, List, Any
import numpy as np

class AdvancedCodeAnalysis:
    def __init__(self):
        self.metrics_history = {}
    
    def analyze_code_quality(self, code: str, language: str = "python") -> Dict[str, Any]:
        """
        Analyse avancée de la qualité du code avec multiples métriques
        """
        if language != "python":
            return {"error": "Advanced analysis currently only supports Python"}
        
        try:
            # Analyse Radon
            complexity_analysis = self._radon_analysis(code)
            # Analyse Lizard
            lizard_analysis = self._lizard_analysis(code)
            # Analyse AST personnalisée
            ast_analysis = self._ast_analysis(code)
            
            # Score composite de qualité
            quality_score = self._calculate_quality_score(
                complexity_analysis, 
                lizard_analysis, 
                ast_analysis
            )
            
            return {
                "quality_score": quality_score,
                "radon_metrics": complexity_analysis,
                "lizard_metrics": lizard_analysis,
                "ast_metrics": ast_analysis,
                "recommendations": self._generate_recommendations(
                    complexity_analysis, 
                    lizard_analysis
                )
            }
            
        except Exception as e:
            return {"error": f"Advanced analysis failed: {str(e)}"}
    
    def _radon_analysis(self, code: str) -> Dict[str, Any]:
        """Analyse avec Radon"""
        try:
            # Complexité cyclomatique
            complexities = cc_visit(code)
            cc_scores = [c.complexity for c in complexities]
            
            # Maintainability Index
            mi_score = mi_visit(code, multi=True)
            
            # Raw metrics
            raw_metrics = analyze(code)
            
            return {
                "cyclomatic_complexity": {
                    "average": np.mean(cc_scores) if cc_scores else 0,
                    "max": max(cc_scores) if cc_scores else 0,
                    "functions": [{"name": c.name, "complexity": c.complexity} for c in complexities]
                },
                "maintainability_index": mi_score,
                "raw_metrics": {
                    "lines": raw_metrics.loc,
                    "comments": raw_metrics.comments,
                    "blank_lines": raw_metrics.blank,
                    "comment_ratio": raw_metrics.comments / raw_metrics.loc if raw_metrics.loc > 0 else 0
                }
            }
        except:
            return {"error": "Radon analysis failed"}
    
    def _lizard_analysis(self, code: str) -> Dict[str, Any]:
        """Analyse avec Lizard"""
        try:
            analysis = lizard.analyze_file.analyze_source_code("temp.py", code)
            
            return {
                "function_count": len(analysis.function_list),
                "average_nloc": analysis.average_nloc,
                "average_token_count": analysis.average_token_count,
                "function_metrics": [
                    {
                        "name": func.name,
                        "nloc": func.nloc,
                        "complexity": func.cyclomatic_complexity,
                        "token_count": func.token_count,
                        "parameter_count": func.parameter_count
                    }
                    for func in analysis.function_list
                ]
            }
        except:
            return {"error": "Lizard analysis failed"}
    
    def _ast_analysis(self, code: str) -> Dict[str, Any]:
        """Analyse AST personnalisée"""
        try:
            tree = ast.parse(code)
            
            function_count = 0
            class_count = 0
            import_count = 0
            depth_levels = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    function_count += 1
                elif isinstance(node, ast.ClassDef):
                    class_count += 1
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    import_count += 1
                elif hasattr(node, 'lineno'):
                    depth_levels.append(self._get_node_depth(node))
            
            return {
                "function_count": function_count,
                "class_count": class_count,
                "import_count": import_count,
                "average_depth": np.mean(depth_levels) if depth_levels else 0,
                "max_depth": max(depth_levels) if depth_levels else 0
            }
        except:
            return {"error": "AST analysis failed"}
    
    def _calculate_quality_score(self, radon_metrics: Dict, lizard_metrics: Dict, ast_metrics: Dict) -> float:
        """Calcule un score de qualité composite"""
        score = 100.0
        
        # Pénalités pour complexité élevée
        if "cyclomatic_complexity" in radon_metrics:
            avg_complexity = radon_metrics["cyclomatic_complexity"].get("average", 0)
            if avg_complexity > 10:
                score -= (avg_complexity - 10) * 2
        
        # Bonus pour bon maintainability index
        if "maintainability_index" in radon_metrics:
            mi = radon_metrics["maintainability_index"]
            if mi > 85:
                score += 5
            elif mi < 65:
                score -= (65 - mi) * 2
        
        return max(min(score, 100), 0)
    
    def _generate_recommendations(self, radon_metrics: Dict, lizard_metrics: Dict) -> List[str]:
        """Génère des recommandations d'amélioration"""
        recommendations = []
        
        if "cyclomatic_complexity" in radon_metrics:
            avg_cc = radon_metrics["cyclomatic_complexity"].get("average", 0)
            if avg_cc > 7:
                recommendations.append("Refactor complex functions into smaller, single-purpose functions")
        
        if "maintainability_index" in radon_metrics:
            mi = radon_metrics["maintainability_index"]
            if mi < 70:
                recommendations.append("Add comments and improve code documentation")
        
        return recommendations
    
    def _get_node_depth(self, node, depth=0):
        """Calcule la profondeur d'un nœud AST"""
        if not hasattr(node, 'parent'):
            return depth
        return self._get_node_depth(node.parent, depth + 1)

# Instance globale
advanced_analysis_service = AdvancedCodeAnalysis()