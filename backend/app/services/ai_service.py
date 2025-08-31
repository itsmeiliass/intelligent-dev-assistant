# app/services/ai_service.py
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel, PeftConfig
import torch
import re
from typing import Any
import os

class AIService:
    def __init__(self):
        self.setup_models()
    
    def setup_models(self):
        """
        Charge StarCoder2 + LoRA fine-tunés.
        Si échec -> fallback rule-based.
        """
        try:
            print("🚀 Loading our FINE-TUNED StarCoder2 model...")
            self.base_model_id = "bigcode/starcoder2-3b"
            self.adapter_repo = "itsmeiliass/ida-starcoder2-qlora"
            
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.base_model_id, 
                use_fast=True
            )
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token

            base_model = AutoModelForCausalLM.from_pretrained(
                self.base_model_id,
                torch_dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32,
                device_map="auto"
            )
            
            # Chargez VOS adapteurs fine-tunés
            self.model = PeftModel.from_pretrained(base_model, self.adapter_repo)
            self.model.eval()

            print("✅ Our fine-tuned model loaded successfully!")
            
        except Exception as e:
            print(f"❌ Failed to load fine-tuned model: {e}")
            print("📋 Falling back to enhanced rule-based system")
            self.model = None
            self.tokenizer = None

    # -------------------- LAYER 1: FINE-TUNED MODEL INFERENCE --------------------
    def _generate_with_fine_tuned_ai(self, function_code: str, function_name: str, mode: str = "doc") -> str:
        """
        Génère une docstring ou un test avec le modèle fine-tuné.
        mode: "doc" -> docstring, "test" -> test
        """
        if self.model is None or self.tokenizer is None:
            return None
        
        if mode == "doc":
            prompt = (
                "### Task: Write a comprehensive Google-style Python docstring for the function below.\n"
                f"### Code:\n{function_code}\n\n"
                "### Response (docstring only, Google format with Args and Returns sections):\n"
            )
        else:
            prompt = (
                "### Task: Write minimal pytest unit tests for the function below.\n"
                f"### Code:\n{function_code}\n\n"
                "### Response (pytest code only):\n"
            )

        try:
            inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=2048)
            device = next(self.model.parameters()).device
            inputs = {k: v.to(device) for k, v in inputs.items()}
            
            with torch.inference_mode():
                out = self.model.generate(
                    **inputs,
                    max_new_tokens=300,
                    do_sample=True,
                    temperature=0.3,
                    top_p=0.9,
                    eos_token_id=self.tokenizer.eos_token_id,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            text = self.tokenizer.decode(out[0], skip_special_tokens=True)
            completion = text[len(prompt):].strip()
            
            # Nettoyer la sortie
            if mode == "doc":
                if '"""' in completion:
                    completion = completion.split('"""')[0]
                completion = completion.strip()
            
            return completion
            
        except Exception as e:
            print(f"🤖 Fine-tuned model generation failed: {e}")
            return None

    # -------------------- LAYER 2: ENHANCED RULE-BASED FALLBACK --------------------
    def _generate_rule_based_doc(self, function_code: str, function_name: str) -> str:
        """Fallback rule-based amélioré"""
        # [Garder votre implémentation existante]
        # ... votre code actuel ...

    def _generate_rule_based_test(self, function_code: str, function_name: str) -> str:
        """Fallback rule-based pour les tests"""
        # [Garder votre implémentation existante]
        # ... votre code actuel ...

    # -------------------- MAIN INTERFACE --------------------
    def generate_documentation(self, function_code: str, function_name: str) -> str:
        print(f"🔍 generate_documentation called for: {function_name}")
        
        # Essayer d'abord le modèle fine-tuné
        ai_result = self._generate_with_fine_tuned_ai(function_code, function_name, mode="doc")
        if ai_result and self._is_ai_output_valid(ai_result, mode="doc"):
            print("✅ Using our fine-tuned model!")
            return f"\"\"\"\n{ai_result}\n\"\"\""
        
        # Fallback vers le système rule-based
        print("📋 Using rule-based fallback for documentation")
        return self._generate_rule_based_doc(function_code, function_name)

    def generate_test(self, function_code: str, function_name: str) -> str:
        print(f"🔍 generate_test called for: {function_name}")
        
        # Essayer d'abord le modèle fine-tuné
        ai_result = self._generate_with_fine_tuned_ai(function_code, function_name, mode="test")
        if ai_result and self._is_ai_output_valid(ai_result, mode="test"):
            print("✅ Using our fine-tuned model!")
            return ai_result
        
        # Fallback vers le système rule-based
        print("📋 Using rule-based fallback for test")
        return self._generate_rule_based_test(function_code, function_name)

    # -------------------- NEW: REFACTORING FEATURE --------------------
    def refactor_code(self, code: str, language: str = "python") -> str:
        """
        Suggest code refactoring improvements
        """
        if self.model is None or self.tokenizer is None:
            return "# Refactoring requires AI model (currently unavailable)"
        
        try:
            prompt = f"""### Task: Refactor this {language} code to make it more efficient, readable, and Pythonic
### Code to refactor:
{code}

### Refactored code (code only, no explanations):
"""
            
            inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=2048)
            device = next(self.model.parameters()).device
            inputs = {k: v.to(device) for k, v in inputs.items()}
            
            with torch.inference_mode():
                out = self.model.generate(
                    **inputs,
                    max_new_tokens=500,
                    do_sample=True,
                    temperature=0.4,
                    top_p=0.9,
                    eos_token_id=self.tokenizer.eos_token_id
                )
            
            text = self.tokenizer.decode(out[0], skip_special_tokens=True)
            refactored_code = text[len(prompt):].strip()
            
            # Extraire seulement le code
            if "```" in refactored_code:
                refactored_code = refactored_code.split("```")[1]
                if refactored_code.startswith("python"):
                    refactored_code = refactored_code[6:].strip()
            
            return refactored_code
            
        except Exception as e:
            print(f"🤖 Refactoring failed: {e}")
            return f"# Refactoring failed: {str(e)}"

    # -------------------- NEW: CODE EXPLANATION --------------------
    def explain_code(self, code: str, language: str = "python") -> str:
        """
        Explain code in natural language
        """
        if self.model is None or self.tokenizer is None:
            return "Code explanation requires AI model (currently unavailable)"
        
        try:
            prompt = f"""### Task: Explain this {language} code in simple natural language
### Code:
{code}

### Explanation (clear and concise):
"""
            
            inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=2048)
            device = next(self.model.parameters()).device
            inputs = {k: v.to(device) for k, v in inputs.items()}
            
            with torch.inference_mode():
                out = self.model.generate(
                    **inputs,
                    max_new_tokens=200,
                    do_sample=True,
                    temperature=0.3,
                    top_p=0.9,
                    eos_token_id=self.tokenizer.eos_token_id
                )
            
            text = self.tokenizer.decode(out[0], skip_special_tokens=True)
            explanation = text[len(prompt):].strip()
            
            return explanation
            
        except Exception as e:
            print(f"🤖 Code explanation failed: {e}")
            return f"Explanation failed: {str(e)}"

    # -------------------- VALIDATION UTILITIES --------------------
    def _is_ai_output_valid(self, output: str, mode: str = "doc") -> bool:
        """
        Valide la sortie de l'IA
        """
        if not output or len(output.strip()) < 10:
            return False
            
        if mode == "doc":
            # Pour docstrings: vérifier que ça ressemble à de la documentation
            has_doc_keywords = any(word in output.lower() for word in [
                'function', 'param', 'arg', 'return', 'description', 'example'
            ])
            return has_doc_keywords or len(output.split('\n')) >= 2
            
        else:  # mode == "test"
            # Pour tests: vérifier que ça ressemble à du code de test
            has_test_keywords = any(word in output.lower() for word in [
                'test', 'assert', 'import', 'def test_', 'pytest'
            ])
            return has_test_keywords or 'assert' in output

# Create global instance
ai_service = AIService()