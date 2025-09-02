# app/services/ai_service.py
import requests
import os
from typing import Optional
import logging
import time

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        self.use_ai = False
        self.api_token = os.getenv("HF_API_TOKEN", "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")
        self.model_id = "itsmeiliass/ida-starcoder2-qlora"
        self.setup_api()
    
    def setup_api(self):
        """Setup Hugging Face API connection"""
        try:
            print("🚀 Connecting to Hugging Face API...")
            print(f"Using model: {self.model_id}")
            print(f"Token set: {self.api_token != 'your_huggingface_token_here'}")
            
            # Test the API connection with a known public model
            test_model = "bigcode/starcoder2-3b"
            response = requests.get(
                f"https://huggingface.co/api/models/{test_model}",
                headers={"Authorization": f"Bearer {self.api_token}"} if self.api_token != "your_huggingface_token_here" else {},
                timeout=10
            )
            
            if response.status_code == 200:
                print("✅ Basic API connection works!")
                response2 = requests.get(
                    f"https://huggingface.co/api/models/{self.model_id}",
                    headers={"Authorization": f"Bearer {self.api_token}"} if self.api_token != "your_huggingface_token_here" else {},
                    timeout=10
                )
                
                if response2.status_code == 200:
                    self.use_ai = True
                    print("✅ Connected to our fine-tuned model successfully!")
                else:
                    print(f"❌ Our model access failed: {response2.status_code}")
                    print("🔄 Falling back to base model...")
                    self.model_id = "bigcode/starcoder2-3b"
                    self.use_ai = True
            else:
                print(f"❌ Basic API test failed: {response.status_code}")
                print("📋 Will use rule-based system")
                self.use_ai = False
                
        except Exception as e:
            print(f"❌ API setup failed: {e}")
            print("📋 Will use rule-based system")
            self.use_ai = False

    def _generate_with_api(self, function_code: str, mode: str = "doc") -> Optional[str]:
        """Generate using Hugging Face Inference API"""
        if not self.use_ai:
            print("❌ AI not enabled")
            return None
        
        try:
            prompt = (
                "### Task: Write a Python docstring for the function below.\n" if mode == "doc"
                else "### Task: Write a minimal pytest unit test for the function below.\n"
            ) + f"### Code:\n{function_code}\n\n### Response ({'docstring only' if mode == 'doc' else 'pytest code only'}):\n"

            print(f"📨 Sending request to: {self.model_id}")
            
            api_url = f"https://api-inference.huggingface.co/models/{self.model_id}"
            headers = {
                "Authorization": f"Bearer {self.api_token}" if self.api_token != "your_huggingface_token_here" else "",
                "Content-Type": "application/json"
            }
            headers = {k: v for k, v in headers.items() if v}  # remove empty headers
            
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 200,
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "do_sample": True,
                    "return_full_text": False
                }
            }
            
            max_retries = 3
            for attempt in range(max_retries):
                print(f"🔄 Attempt {attempt + 1}/{max_retries}")
                try:
                    response = requests.post(api_url, headers=headers, json=payload, timeout=30)
                    print(f"📥 Response status: {response.status_code}")
                    
                    if response.status_code == 200:
                        result = response.json()
                        if isinstance(result, list) and len(result) > 0:
                            return result[0].get('generated_text', '').strip()
                        else:
                            print("❌ Unexpected response format", result)
                    
                    elif response.status_code in [401, 403]:
                        print(f"🔐 Authentication error: {response.status_code}, retrying without token...")
                        response = requests.post(api_url, headers={"Content-Type": "application/json"}, json=payload, timeout=30)
                        if response.status_code == 200:
                            result = response.json()
                            if isinstance(result, list) and len(result) > 0:
                                return result[0].get('generated_text', '').strip()
                    
                    elif response.status_code == 404:
                        print(f"❌ Model not found: {self.model_id}")
                        if self.model_id != "bigcode/starcoder2-3b":
                            print("🔄 Falling back to base model...")
                            self.model_id = "bigcode/starcoder2-3b"
                            continue  # retry once with base model
                        else:
                            print("❌ Base model not found, using rule-based fallback.")
                            return None
                    
                    elif response.status_code == 503 and attempt < max_retries - 1:
                        wait_time = 5 * (attempt + 1)
                        print(f"⏳ Model loading, retrying in {wait_time}s...")
                        time.sleep(wait_time)
                        continue

                except requests.exceptions.Timeout:
                    print("❌ API request timed out")
                    if attempt < max_retries - 1:
                        time.sleep(5)
                        continue
                
                break

            print("❌ All AI generation attempts failed")
            return None

        except Exception as e:
            print(f"❌ API generation failed: {e}")
            logger.error(f"API generation failed: {e}")
            return None

    def _clean_docstring(self, docstring: str) -> str:
        if not docstring:
            return ""
        if '"""' in docstring:
            parts = docstring.split('"""')
            if len(parts) >= 3:
                docstring = '"""' + parts[1] + '"""'
        if not docstring.startswith('"""'):
            docstring = f'"""{docstring}'
        if not docstring.endswith('"""'):
            docstring = f'{docstring}"""'
        return docstring

    # -------------------- RULE-BASED FALLBACKS --------------------
    def _generate_rule_based_doc(self, function_code: str, function_name: str) -> str:
        try:
            lines = function_code.strip().split('\n')
            if not lines:
                return '"""\nTODO: Add documentation\n"""'
            signature = lines[0]
            params = []
            if '(' in signature and ')' in signature:
                param_part = signature.split('(', 1)[1].rsplit(')', 1)[0]
                param_list = [p.strip() for p in param_part.split(',') if p.strip()]
                for param in param_list:
                    param_name = param.split('=')[0].strip() if '=' in param else param.strip()
                    if param_name and not param_name.startswith('*'):
                        params.append(param_name)
            
            doc_lines = ['"""', f"{function_name} function.", ""]
            if params:
                doc_lines.append("Args:")
                for param in params:
                    doc_lines.append(f"    {param}: Description of {param}.")
                doc_lines.append("")
            
            return_type = "Any"
            if "->" in signature:
                return_part = signature.split("->")[1].strip()
                return_type = return_part.split(":")[0].strip() if ":" in return_part else return_part
            doc_lines.append("Returns:")
            doc_lines.append(f"    {return_type}: Description of return value.")
            doc_lines.append('"""')
            return '\n'.join(doc_lines)
        except Exception:
            return '"""\nTODO: Add comprehensive documentation\n"""'

    def _generate_rule_based_test(self, function_code: str, function_name: str) -> str:
        try:
            signature = function_code.strip().split('\n')[0]
            params = []
            if '(' in signature and ')' in signature:
                param_part = signature.split('(', 1)[1].rsplit(')', 1)[0]
                params = [p.strip().split('=')[0].strip() for p in param_part.split(',') if p.strip()]
            
            test_code = ["import pytest", "", f"def test_{function_name}():"]

            if params:
                test_values = []
                for param in params:
                    if param in ['a', 'x', 'num1']:
                        test_values.append('5')
                    elif param in ['b', 'y', 'num2']:
                        test_values.append('3')
                    elif 'list' in param or 'array' in param:
                        test_values.append('[1, 2, 3]')
                    elif 'string' in param or 'str' in param or 'text' in param:
                        test_values.append('"test"')
                    else:
                        test_values.append('None')
                test_code.append(f"    # Test with {', '.join(test_values)}")
                test_code.append(f"    result = {function_name}({', '.join(test_values)})")
                test_code.append("    assert result is not None")
            else:
                test_code.append(f"    result = {function_name}()")
                test_code.append("    assert result is not None")
            test_code.append("")
            return '\n'.join(test_code)
        except Exception:
            return f'''import pytest

def test_{function_name}():
    # Test basic functionality
    # TODO: Add specific test cases
    pass
'''

    # -------------------- MAIN INTERFACE --------------------
    def generate_documentation(self, function_code: str, function_name: str) -> str:
        print(f"🔍 Attempting AI documentation generation for: {function_name}")
        ai_result = self._generate_with_api(function_code, "doc")
        if ai_result and self._is_valid_output(ai_result, "doc"):
            print(f"✅ USING AI MODEL for: {function_name}")
            return self._clean_docstring(ai_result)
        print(f"🔄 FALLING BACK to rule-based for: {function_name}")
        return self._generate_rule_based_doc(function_code, function_name)

    def generate_test(self, function_code: str, function_name: str) -> str:
        print(f"🔍 Attempting AI test generation for: {function_name}")
        ai_result = self._generate_with_api(function_code, "test")
        if ai_result and self._is_valid_output(ai_result, "test"):
            print(f"✅ USING AI MODEL for: {function_name}")
            return ai_result
        print(f"🔄 FALLING BACK to rule-based for: {function_name}")
        return self._generate_rule_based_test(function_code, function_name)

    def _is_valid_output(self, output: str, mode: str) -> bool:
        if not output or len(output.strip()) < 10:
            return False
        if mode == "doc":
            return any(k in output.lower() for k in ['args', 'returns', 'param', 'function', 'description', '"""'])
        else:
            return any(k in output.lower() for k in ['def test', 'assert', 'import pytest', 'import unittest'])

# Create global instance
ai_service = AIService()
