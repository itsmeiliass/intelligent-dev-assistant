# app/services/ai_service.py
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import torch
import re
from typing import Any

class AIService:
    def __init__(self):
        self.setup_models()
    
    def setup_models(self):
        """Initialize with authenticated StarCoder access"""
        try:
            print("🚀 Initializing dual-layer AI system with StarCoder...")
            
            # First, try to load StarCoder with authentication
            try:
                print("📦 Loading StarCoderbase-1b (gated model)...")
                
                # Load tokenizer and model with proper authentication
                self.tokenizer = AutoTokenizer.from_pretrained(
                    "bigcode/starcoderbase-1b",
                    token=True
                )
                
                self.model = AutoModelForCausalLM.from_pretrained(
                    "bigcode/starcoderbase-1b", 
                    token=True,
                    device_map="auto",
                    torch_dtype=torch.float16,
                    trust_remote_code=True
                )
                
                # Create generation pipeline without device parameter
                self.generation_pipeline = pipeline(
                    "text-generation",
                    model=self.model,
                    tokenizer=self.tokenizer,
                    torch_dtype=torch.float16,
                    trust_remote_code=True
                )
                
                print("✅ StarCoder loaded successfully with authentication!")
                print("🤖 Using advanced code generation capabilities!")
                
            except Exception as e:
                print(f"❌ StarCoder loading failed: {e}")
                raise Exception("StarCoder authentication failed")
                
        except Exception as e:
            print(f"📋 Falling back to enhanced rule-based system: {e}")
            self.generation_pipeline = None
            self.tokenizer = None
            self.model = None

    # -------------------- LAYER 1: STARCODER AI GENERATION --------------------
    def _generate_with_local_ai(self, function_code: str, function_name: str) -> str:
        """Generate documentation using StarCoder with optimized prompts"""
        if not self.generation_pipeline:
            print("❌ No generation pipeline available")
            return None
            
        try:
            # More specific prompt with examples
            prompt = f"""# Write a Python docstring for this function:

{function_code}

# Example of good docstring format:
\"\"\"
Brief description of what the function does.

Args:
    param1: Description of first parameter
    param2: Description of second parameter

Returns:
    Description of return value
\"\"\"

# Now write the docstring for the above function:
\"\"\"
"""
            
            print(f"🤖 Sending prompt to StarCoder for function: {function_name}")
            
            result = self.generation_pipeline(
                prompt,
                max_new_tokens=200,
                num_return_sequences=1,
                temperature=0.4,
                do_sample=True,
                top_p=0.92,
                repetition_penalty=1.1,
                pad_token_id=self.tokenizer.eos_token_id,
                return_full_text=False
            )
            
            generated_text = result[0]['generated_text']
            print(f"🤖 StarCoder raw output ({len(generated_text)} chars): {generated_text[:200]}...")
            
            # Extract content between triple quotes
            doc_match = re.search(r'\"\"\"(.*?)\"\"\"', generated_text, re.DOTALL)
            if doc_match:
                docstring = doc_match.group(1).strip()
                print(f"🤖 Extracted docstring ({len(docstring)} chars): {docstring[:100]}...")
            else:
                # If no triple quotes, use the generated text directly
                docstring = generated_text.strip()
                print(f"🤖 Using direct output as docstring ({len(docstring)} chars): {docstring[:100]}...")
            
            # Clean up comments and extra spaces
            docstring = re.sub(r'^#.*$', '', docstring, flags=re.MULTILINE).strip()
            docstring = re.sub(r'\n\s*\n', '\n\n', docstring)  # Remove extra blank lines
            
            if self._is_ai_output_valid(docstring):
                print("🎯 Using StarCoder-generated documentation!")
                return docstring
            else:
                print("❌ AI output failed validation")
                return None
                
        except Exception as e:
            print(f"🤖 StarCoder generation failed: {e}")
            return None

    def _is_ai_output_valid(self, docstring: str) -> bool:
        """
        ✅ LENIENT VALIDATION RULES:
        Accept any meaningful text that looks like documentation
        """
        # Rule 1: Minimum length
        if not docstring or len(docstring.strip()) < 15:
            print("❌ Validation: Docstring too short or empty")
            return False
            
        # Rule 2: No repetition
        if self._has_repetition(docstring):
            print("❌ Validation: Docstring has repetition")
            return False
            
        # Rule 3: No actual code
        if self._contains_actual_code(docstring):
            print("❌ Validation: Docstring contains actual code")
            return False
        
        # Rule 4: Accept ANY documentation-like text
        has_doc_content = any(word in docstring.lower() for word in [
            'function', 'parameter', 'return', 'arg', 'description', 
            'input', 'output', 'value', 'number', 'string', 'boolean',
            'list', 'dict', 'calculate', 'process', 'validate', 'add',
            'sum', 'multiply', 'operation', 'result', 'documentation',
            'brief', 'explanation', 'purpose'
        ])
        
        # Also accept any text that has some structure
        has_structure = len(docstring.split('\n')) >= 2 or ':' in docstring or '-' in docstring
        
        if not has_doc_content and not has_structure:
            print("❌ Validation: Doesn't look like documentation")
            return False
            
        print("✅ Validation: AI output passed - accepting documentation text")
        return True

    def _contains_actual_code(self, text: str) -> bool:
        """
        ✅ SMART CODE DETECTION:
        Only reject actual Python code, not docstring formatting
        """
        # These are actual code indicators (REJECT)
        code_indicators = [
            'def ', 'import ', 'class ', 'return ', '= ', 
            ': ', '()', 'self.', 'print(', 'if ', 'for ', 'while ',
            'try:', 'except:', 'raise ', 'yield ', 'assert ', 'lambda '
        ]
        
        # These are docstring formatting (ACCEPT)
        docstring_formatting = ['---', '===', '***', '___', '    ', '@param', '@return']
        
        # Check for actual code
        has_real_code = any(indicator in text for indicator in code_indicators)
        
        # Check if it's just docstring formatting
        has_doc_formatting = any(fmt in text for fmt in docstring_formatting)
        
        # Only reject if it has real code AND not just formatting
        return has_real_code and not has_doc_formatting

    # -------------------- LAYER 2: ENHANCED RULE-BASED FALLBACK --------------------
    def _generate_rule_based_doc(self, function_code: str, function_name: str) -> str:
        """Layer 2: Enhanced rule-based fallback"""
        try:
            args_match = re.search(r'def\s+\w+\((.*?)\):', function_code)
            if not args_match:
                return f"\"\"\"\n{function_name}: Function implementation.\n\nReturns:\n    Result value.\n\"\"\""
            
            args_str = args_match.group(1)
            args = []
            for arg in args_str.split(','):
                arg = arg.strip()
                if arg:
                    if '=' in arg:
                        name, default = arg.split('=', 1)
                        args.append({'name': name.strip(), 'default': default.strip()})
                    else:
                        args.append({'name': arg, 'default': None})
            
            return_type = 'Any'
            return_match = re.search(r'->\s*(\w+):', function_code)
            if return_match:
                return_type = return_match.group(1)
            
            # Generate intelligent documentation
            description = self._get_function_description(function_name, function_code)
            
            doc = f"\"\"\"\n{description}\n\n"
            
            if args:
                doc += "Args:\n"
                for arg in args:
                    arg_desc = self._get_argument_description(arg['name'])
                    if arg['default']:
                        doc += f"    {arg['name']}: {arg_desc} Defaults to {arg['default']}.\n"
                    else:
                        doc += f"    {arg['name']}: {arg_desc}\n"
            
            return_desc = self._get_return_description(function_name, return_type)
            doc += f"\nReturns:\n    {return_type}: {return_desc}\n\"\"\""
            
            return doc
            
        except Exception as e:
            return f"\"\"\"\n{function_name}: Function implementation.\n\nError: {str(e)[:50]}...\n\"\"\""

    def _get_function_description(self, function_name: str, function_code: str) -> str:
        """Intelligent function description based on name and content"""
        name_lower = function_name.lower()
        
        if any(word in name_lower for word in ['calculate', 'compute', 'math', 'sum', 'add']):
            return f"{function_name}: Performs mathematical calculation."
        elif any(word in name_lower for word in ['get', 'fetch', 'retrieve', 'find']):
            return f"{function_name}: Retrieves data or information."
        elif any(word in name_lower for word in ['set', 'update', 'modify', 'change']):
            return f"{function_name}: Updates or modifies data."
        elif any(word in name_lower for word in ['validate', 'check', 'verify', 'test']):
            return f"{function_name}: Validates input or conditions."
        elif any(word in name_lower for word in ['create', 'make', 'build', 'generate']):
            return f"{function_name}: Creates new instance or data."
        elif "return a + b" in function_code:
            return f"{function_name}: Adds two numbers together."
        elif "return a * b" in function_code:
            return f"{function_name}: Multiplies two numbers."
        else:
            return f"{function_name}: Function implementation."

    def _get_argument_description(self, arg_name: str) -> str:
        """Context-aware argument descriptions"""
        arg_lower = arg_name.lower()
        
        if any(word in arg_lower for word in ['num', 'count', 'value', 'x', 'y', 'n']):
            return "Numeric value. "
        elif any(word in arg_lower for word in ['name', 'text', 'str', 'title', 'msg']):
            return "Text string. "
        elif any(word in arg_lower for word in ['list', 'array', 'items', 'elements']):
            return "Collection of items. "
        elif any(word in arg_lower for word in ['dict', 'map', 'data', 'config']):
            return "Key-value mapping. "
        elif any(word in arg_lower for word in ['flag', 'enable', 'active', 'status']):
            return "Boolean indicator. "
        else:
            return "Input parameter. "

    def _get_return_description(self, function_name: str, return_type: str) -> str:
        """Intelligent return value descriptions"""
        name_lower = function_name.lower()
        
        if any(word in name_lower for word in ['calculate', 'compute', 'math']):
            return "Result of mathematical operation."
        elif any(word in name_lower for word in ['get', 'fetch', 'retrieve']):
            return "Requested data or information."
        elif any(word in name_lower for word in ['validate', 'check']):
            return "Validation result status."
        else:
            return "Result of the operation."

    # -------------------- MAIN INTERFACE --------------------
    def generate_documentation(self, function_code: str, function_name: str) -> str:
        """Dual-layer generation: Try StarCoder first, then fallback to rule-based"""
        print(f"🔍 generate_documentation called with: {function_name}")
        
        # LAYER 1: Try StarCoder AI model
        ai_result = self._generate_with_local_ai(function_code, function_name)
        
        if ai_result:
            print(f"🎯 STARCODER USED: {ai_result[:100]}...")
            return f"\"\"\"\n{ai_result}\n\"\"\""
        
        # LAYER 2: Fallback to rule-based
        print("📋 USING RULE-BASED FALLBACK")
        fallback_result = self._generate_rule_based_doc(function_code, function_name)
        print(f"📋 FALLBACK RESULT: {fallback_result[:100]}...")
        return fallback_result

    # -------------------- SMART TEST GENERATION --------------------
    def generate_test(self, function_code: str, function_name: str) -> str:
        """Generate intelligent tests with better assertions"""
        try:
            args_match = re.search(r'def\s+\w+\((.*?)\):', function_code)
            if args_match:
                args = [arg.strip() for arg in args_match.group(1).split(',') if arg.strip() and arg != 'self']
                test_values = []
                for arg in args:
                    clean_arg = re.sub(r':.*', '', arg).strip()
                    clean_arg = re.sub(r'=.*', '', clean_arg).strip()
                    arg_lower = clean_arg.lower()

                    if any(x in arg_lower for x in ['num', 'count', 'value', 'x', 'y', 'n']):
                        test_values.append("5")
                    elif any(x in arg_lower for x in ['name', 'text', 'str']):
                        test_values.append('"test"')
                    elif any(x in arg_lower for x in ['flag', 'enable']):
                        test_values.append("True")
                    elif any(x in arg_lower for x in ['list', 'array']):
                        test_values.append("[1, 2, 3]")
                    elif any(x in arg_lower for x in ['dict', 'map']):
                        test_values.append('{"key": "value"}')
                    else:
                        test_values.append("1")
                test_args = ', '.join(test_values)
            else:
                test_args = ""

            test_code = f"""
import pytest

def test_{function_name}():
    \"\"\"Test for {function_name} function.\"\"\"
    # Test basic functionality
    result = {function_name}({test_args})
    assert result is not None
    # Additional test cases recommended
"""
            return test_code.strip()
            
        except Exception as e:
            return f"# Test generation error: {str(e)}"

    # -------------------- UTILITY METHODS --------------------
    def _has_repetition(self, text: str, max_repeats: int = 2) -> bool:
        """Check for repetitive content"""
        lines = text.split('\n')
        counts = {}
        for line in lines:
            clean_line = line.strip()
            if clean_line and len(clean_line) > 10:
                counts[clean_line] = counts.get(clean_line, 0) + 1
                if counts[clean_line] > max_repeats:
                    return True
        return False

    def explain_code(self, code_snippet: str) -> str:
        """Explain code in natural language"""
        if "def " in code_snippet and "return " in code_snippet:
            return "This function performs a calculation and returns a result."
        elif "def " in code_snippet:
            return "This is a function definition."
        elif "class " in code_snippet:
            return "This defines a class."
        elif "import " in code_snippet:
            return "This imports modules."
        else:
            return "This code performs operations."

# Create global instance
ai_service = AIService()