# app/services/code_analysis.py
import ast
import tree_sitter
from tree_sitter import Language, Parser
from pathlib import Path
from typing import Dict, List, Any
import os

class CodeAnalysisService:
    def __init__(self):
        # Initialize Tree-sitter (for multi-language support later)
        self.setup_tree_sitter()
    
    def setup_tree_sitter(self):
        """Setup Tree-sitter parsers (we'll start with Python)"""
        try:
            # Create a languages directory if it doesn't exist
            languages_dir = Path("app/services/languages")
            languages_dir.mkdir(exist_ok=True)
            
            # For now, we'll use AST for Python. Tree-sitter setup can be added later for other languages.
            self.python_parser = ast
            self.parsers = {}
            
        except Exception as e:
            print(f"Tree-sitter setup warning: {e}. Using standard AST parsing.")
    
    def parse_python_file(self, code_content: str) -> Dict[str, Any]:
        """
        Parse a Python file and extract its structure using AST
        """
        try:
            tree = ast.parse(code_content)
            
            functions = []
            classes = []
            imports = []
            
            for node in ast.walk(tree):
                # Extract function definitions
                if isinstance(node, ast.FunctionDef):
                    functions.append({
                        'name': node.name,
                        'lineno': node.lineno,
                        'args': [arg.arg for arg in node.args.args],
                        'docstring': ast.get_docstring(node) or ''
                    })
                
                # Extract class definitions
                elif isinstance(node, ast.ClassDef):
                    classes.append({
                        'name': node.name,
                        'lineno': node.lineno,
                        'docstring': ast.get_docstring(node) or ''
                    })
                
                # Extract imports
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append({
                            'type': 'import',
                            'module': alias.name,
                            'alias': alias.asname or ''
                        })
                elif isinstance(node, ast.ImportFrom):
                    for alias in node.names:
                        imports.append({
                            'type': 'from_import',
                            'module': node.module or '',
                            'name': alias.name,
                            'alias': alias.asname or ''
                        })
            
            return {
                'functions': functions,
                'classes': classes,
                'imports': imports,
                'success': True
            }
            
        except SyntaxError as e:
            return {
                'success': False,
                'error': f'Syntax error: {e}',
                'functions': [],
                'classes': [],
                'imports': []
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Parsing error: {e}',
                'functions': [],
                'classes': [],
                'imports': []
            }
    
    def analyze_repository_file(self, file_content: str, file_extension: str) -> Dict[str, Any]:
        """
        Analyze a code file based on its extension
        """
        if file_extension == '.py':
            return self.parse_python_file(file_content)
        else:
            return {
                'success': False,
                'error': f'Unsupported file type: {file_extension}',
                'functions': [],
                'classes': [],
                'imports': []
            }
    
    def get_code_summary(self, analysis_result: Dict[str, Any]) -> str:
        """
        Generate a natural language summary of the code analysis
        """
        if not analysis_result['success']:
            return f"Analysis failed: {analysis_result.get('error', 'Unknown error')}"
        
        func_count = len(analysis_result['functions'])
        class_count = len(analysis_result['classes'])
        import_count = len(analysis_result['imports'])
        
        summary = f"This code contains {func_count} function(s), {class_count} class(es), and {import_count} import(s)."
        
        if func_count > 0:
            summary += "\n\nFunctions:"
            for func in analysis_result['functions']:
                summary += f"\n- {func['name']}({', '.join(func['args'])})"
        
        if class_count > 0:
            summary += "\n\nClasses:"
            for cls in analysis_result['classes']:
                summary += f"\n- {cls['name']}"
        
        return summary

# Create a global instance
code_analysis_service = CodeAnalysisService()