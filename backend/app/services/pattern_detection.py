# app/services/pattern_detection.py
import ast
import re
from typing import Dict, List, Any

class PatternDetectionService:
    def __init__(self):
        self.patterns = self._initialize_patterns()
        self.anti_patterns = self._initialize_anti_patterns()
    
    def detect_patterns(self, code: str, language: str = "python") -> Dict[str, Any]:
        """
        Détecte les patterns et anti-patterns dans le code
        """
        if language != "python":
            return {"error": "Pattern detection currently only supports Python"}
        
        try:
            detected_patterns = []
            detected_anti_patterns = []
            
            # Analyse des patterns
            for pattern_name, pattern_func in self.patterns.items():
                if pattern_func(code):
                    detected_patterns.append(pattern_name)
            
            # Analyse des anti-patterns
            for anti_pattern_name, anti_pattern_func in self.anti_patterns.items():
                if anti_pattern_func(code):
                    detected_anti_patterns.append(anti_pattern_name)
            
            return {
                "patterns": detected_patterns,
                "anti_patterns": detected_anti_patterns,
                "pattern_score": self._calculate_pattern_score(detected_patterns, detected_anti_patterns),
                "recommendations": self._generate_pattern_recommendations(detected_anti_patterns)
            }
            
        except Exception as e:
            return {"error": f"Pattern detection failed: {str(e)}"}
    
    def _initialize_patterns(self) -> Dict[str, callable]:
        """Initialise les patterns à détecter"""
        return {
            "factory_pattern": self._detect_factory_pattern,
            "singleton_pattern": self._detect_singleton_pattern,
            # "strategy_pattern": self._detect_strategy_pattern,  #  RETIRÉ - méthode manquante
            # "observer_pattern": self._detect_observer_pattern,  #  RETIRÉ - méthode manquante
            # "decorator_pattern": self._detect_decorator_pattern,  #  RETIRÉ - méthode manquante
        }
    
    def _initialize_anti_patterns(self) -> Dict[str, callable]:
        """Initialise les anti-patterns à détecter"""
        return {
            "god_object": self._detect_god_object,
            "spaghetti_code": self._detect_spaghetti_code,
            "magic_numbers": self._detect_magic_numbers,
            "duplicate_code": self._detect_duplicate_code,
            "long_method": self._detect_long_method,
        }
    
    def _detect_factory_pattern(self, code: str) -> bool:
        """Détecte le pattern Factory"""
        return "def create_" in code or "class Factory" in code or "Factory(" in code
    
    def _detect_singleton_pattern(self, code: str) -> bool:
        """Détecte le pattern Singleton"""
        return "__instance" in code or "Singleton" in code or "get_instance()" in code
    
    # AJOUTEZ CES MÉTHODES MANQUANTES :
    def _detect_strategy_pattern(self, code: str) -> bool:
        """Détecte le pattern Strategy (simplifié)"""
        return "def execute(" in code or "strategy" in code.lower()
    
    def _detect_observer_pattern(self, code: str) -> bool:
        """Détecte le pattern Observer (simplifié)"""
        return "subscribe" in code or "notify" in code or "observer" in code.lower()
    
    def _detect_decorator_pattern(self, code: str) -> bool:
        """Détecte le pattern Decorator (simplifié)"""
        return "@" in code and "def " in code
    
    def _detect_god_object(self, code: str) -> bool:
        """Détecte l'anti-pattern God Object"""
        # Classe avec trop de méthodes ou trop longue
        class_pattern = r'class \w+:.*?def (\w+)\(.*?\):'
        methods = re.findall(class_pattern, code, re.DOTALL)
        return len(methods) > 10  # Plus de 10 méthodes dans une classe
    
    def _detect_magic_numbers(self, code: str) -> bool:
        """Détecte les nombres magiques"""
        magic_numbers = re.findall(r'\b([0-9]{2,})\b', code)  # Nombres à 2+ chiffres
        return len(magic_numbers) > 3  # Plus de 3 nombres magiques
    
    def _detect_duplicate_code(self, code: str) -> bool:
        """Détecte les duplications de code (simplifié)"""
        lines = code.split('\n')
        unique_lines = set(lines)
        return len(lines) > 20 and len(unique_lines) / len(lines) < 0.7
    
    def _detect_long_method(self, code: str) -> bool:
        """Détecte les méthodes trop longues"""
        return len(code.split('\n')) > 50
    
    def _detect_spaghetti_code(self, code: str) -> bool:
        """Détecte le spaghetti code (complexité élevée)"""
        return code.count('if ') + code.count('for ') + code.count('while ') > 10
    
    def _calculate_pattern_score(self, patterns: List[str], anti_patterns: List[str]) -> float:
        """Calcule un score basé sur les patterns détectés"""
        score = 50.0  # Score de base
        
        # Bonus pour les bons patterns
        score += len(patterns) * 5
        
        # Malus pour les anti-patterns
        score -= len(anti_patterns) * 10
        
        return max(min(score, 100), 0)
    
    def _generate_pattern_recommendations(self, anti_patterns: List[str]) -> List[str]:
        """Génère des recommandations basées sur les anti-patterns détectés"""
        recommendations = []
        recommendation_map = {
            "god_object": "Split the God object into smaller, focused classes with single responsibilities",
            "spaghetti_code": "Refactor code to follow clean architecture principles and reduce complexity",
            "magic_numbers": "Replace magic numbers with named constants or configuration values",
            "duplicate_code": "Extract duplicate code into reusable functions or classes",
            "long_method": "Break long methods into smaller, focused methods with clear purposes"
        }
        
        for anti_pattern in anti_patterns:
            if anti_pattern in recommendation_map:
                recommendations.append(recommendation_map[anti_pattern])
        
        return recommendations

# Instance globale
pattern_detection_service = PatternDetectionService()