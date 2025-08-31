# app/services/evaluation_service.py
import numpy as np
from typing import Dict, Any
import re

class EvaluationService:
    def __init__(self):
        pass
    
    def evaluate_docstring(self, generated_doc: str, original_code: str = None) -> Dict[str, Any]:
        """
        Évalue la qualité d'une docstring générée
        """
        if not generated_doc:
            return {"score": 0, "metrics": {}}
        
        # Métriques de base
        metrics = {
            'length': len(generated_doc),
            'line_count': len(generated_doc.split('\n')),
            'has_triple_quotes': '"""' in generated_doc or "'''" in generated_doc,
            'has_args_section': 'Args:' in generated_doc or 'Parameters:' in generated_doc,
            'has_returns_section': 'Returns:' in generated_doc or 'Return:' in generated_doc,
            'has_examples_section': 'Examples:' in generated_doc,
            'has_raises_section': 'Raises:' in generated_doc,
        }
        
        # Score composite
        score = 0
        if metrics['has_triple_quotes']: score += 20
        if metrics['has_args_section']: score += 25
        if metrics['has_returns_section']: score += 25
        if metrics['has_examples_section']: score += 15
        if metrics['has_raises_section']: score += 15
        
        # Ajuster basé sur la longueur (trop court = mauvais, trop long = potentiellement mauvais)
        if 50 <= metrics['length'] <= 500:
            score += 10
        elif metrics['length'] < 50:
            score -= 10
        
        metrics['readability_score'] = self._calculate_readability(generated_doc)
        score += min(metrics['readability_score'] * 2, 20)  # Max 20 points pour la lisibilité
        
        return {
            "score": min(max(score, 0), 100),  # Normaliser entre 0-100
            "metrics": metrics
        }
    
    def evaluate_test(self, generated_test: str, original_code: str = None) -> Dict[str, Any]:
        """
        Évalue la qualité d'un test généré
        """
        if not generated_test:
            return {"score": 0, "metrics": {}}
        
        metrics = {
            'length': len(generated_test),
            'line_count': len(generated_test.split('\n')),
            'has_imports': 'import ' in generated_test,
            'has_test_function': 'def test_' in generated_test,
            'has_assertions': 'assert ' in generated_test,
            'has_pytest_import': 'import pytest' in generated_test or 'from pytest' in generated_test,
            'assertion_count': generated_test.count('assert '),
        }
        
        score = 0
        if metrics['has_imports']: score += 15
        if metrics['has_test_function']: score += 25
        if metrics['has_assertions']: score += 40
        if metrics['has_pytest_import']: score += 20
        score += min(metrics['assertion_count'] * 5, 20)  # Max 20 points pour les assertions
        
        return {
            "score": min(max(score, 0), 100),
            "metrics": metrics
        }
    
    def _calculate_readability(self, text: str) -> float:
        """
        Calcule un score de lisibilité simple
        """
        sentences = re.split(r'[.!?]+', text)
        words = text.split()
        
        if len(sentences) == 0 or len(words) == 0:
            return 0.5
        
        avg_sentence_length = len(words) / len(sentences)
        avg_word_length = sum(len(word) for word in words) / len(words)
        
        # Score basé sur la formule Flesch simplifiée
        readability = 206.835 - (1.015 * avg_sentence_length) - (84.6 * (avg_word_length / 100))
        return max(min(readability / 100, 1.0), 0)  # Normaliser entre 0-1

# Create global instance
evaluation_service = EvaluationService()