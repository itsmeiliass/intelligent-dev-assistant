#!/usr/bin/env python3
"""
Script de test pour les fonctionnalités avancées - Version améliorée
"""
import requests
import json
import time
import subprocess
import threading
import sys
from pathlib import Path

BASE_URL = "http://localhost:8000"

def start_server():
    """Démarre le serveur FastAPI en arrière-plan"""
    try:
        print("🚀 Starting FastAPI server...")
        # Chemin vers votre environnement virtuel
        venv_python = Path("venv/Scripts/python.exe")
        
        # Démarre le serveur en arrière-plan
        process = subprocess.Popen([
            str(venv_python), "-m", "uvicorn", 
            "app.main:app", "--host", "0.0.0.0", "--port", "8000"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Attendre que le serveur démarre
        time.sleep(3)
        return process
        
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        return None

def wait_for_server(max_retries=10, retry_delay=2):
    """Attend que le serveur soit disponible"""
    for i in range(max_retries):
        try:
            response = requests.get(f"{BASE_URL}/health", timeout=5)
            if response.status_code == 200:
                print("✅ Server is ready!")
                return True
        except requests.ConnectionError:
            print(f"⏳ Waiting for server... (Attempt {i+1}/{max_retries})")
            time.sleep(retry_delay)
    
    print("❌ Server did not start in time")
    return False

def test_advanced_features():
    """Test complet des fonctionnalités avancées"""
    
    # Vérifie d'abord si le serveur est déjà démarré
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Server is already running!")
    except requests.ConnectionError:
        print("❌ Server not running. Starting it now...")
        server_process = start_server()
        if not server_process or not wait_for_server():
            print("❌ Could not start server. Please start it manually:")
            print("   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
            return
    
    # Code sample pour les tests
    test_code = """
def calculate_statistics(data):
    \"\"\"Calculate basic statistics from data\"\"\"
    if not data:
        return None
    
    n = len(data)
    mean = sum(data) / n
    sorted_data = sorted(data)
    mid = n // 2
    
    if n % 2 == 0:
        median = (sorted_data[mid-1] + sorted_data[mid]) / 2
    else:
        median = sorted_data[mid]
    
    variance = sum((x - mean) ** 2 for x in data) / n
    std_dev = variance ** 0.5
    
    return {
        'count': n,
        'mean': mean,
        'median': median,
        'std_dev': std_dev,
        'min': min(data),
        'max': max(data)
    }
    """
    
    print("🧪 Testing Advanced Features...")
    
    # Test advanced analysis
    print("\n1. Testing Advanced Analysis...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/advanced/advanced-analysis",
            json={"code": test_code, "language": "python"},
            timeout=30
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   Quality Score: {result.get('analysis', {}).get('quality_score', 'N/A')}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Failed: {e}")
    
    # Test pattern detection
    print("\n2. Testing Pattern Detection...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/advanced/pattern-detection",
            json={"code": test_code, "language": "python"},
            timeout=30
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   Patterns: {result.get('patterns', {}).get('patterns', [])}")
    except Exception as e:
        print(f"   ❌ Failed: {e}")
    
    # Test basic endpoints to ensure they still work
    print("\n3. Testing Basic Endpoints (backward compatibility)...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/docs/generate-function-doc",
            json={"function_code": test_code, "function_name": "calculate_statistics"},
            timeout=30
        )
        print(f"   Documentation Generation: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Failed: {e}")
    
    print("\n✅ Advanced features testing completed!")

if __name__ == "__main__":
    test_advanced_features()