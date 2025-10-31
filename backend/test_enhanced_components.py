#!/usr/bin/env python3
"""
Test script for the enhanced AI compliance auditor
"""

import sys
import os
from pathlib import Path

# Add the ai engine to path
current_dir = Path(__file__).parent
ai_engine_path = current_dir / "ai engine"
sys.path.append(str(ai_engine_path))

def test_imports():
    """Test if all components can be imported"""
    try:
        print("Testing component imports...")
        
        from policy_processor import PolicyProcessor
        print("✓ PolicyProcessor imported successfully")
        
        from repository_scanner import RepositoryScanner
        print("✓ RepositoryScanner imported successfully")
        
        from compliance_analyzer import ComplianceAnalyzer
        print("✓ ComplianceAnalyzer imported successfully")
        
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality without dependencies"""
    try:
        print("\nTesting basic functionality...")
        
        # Test PolicyProcessor initialization
        from policy_processor import PolicyProcessor
        processor = PolicyProcessor()
        print("✓ PolicyProcessor initialized")
        
        # Test RepositoryScanner initialization
        from repository_scanner import RepositoryScanner
        scanner = RepositoryScanner()
        print("✓ RepositoryScanner initialized")
        
        # Test ComplianceAnalyzer initialization
        from compliance_analyzer import ComplianceAnalyzer
        analyzer = ComplianceAnalyzer()
        print("✓ ComplianceAnalyzer initialized")
        
        # Test pipeline status
        status = analyzer.get_pipeline_status()
        print(f"✓ Pipeline status: {status['pipelines_loaded']}")
        
        return True
    except Exception as e:
        print(f"✗ Basic functionality test failed: {e}")
        return False

def test_api_imports():
    """Test if main API components work"""
    try:
        print("\nTesting API imports...")
        
        # Test main imports
        from fastapi import FastAPI
        from pydantic import BaseModel
        print("✓ FastAPI components imported")
        
        # Test if main.py can be imported
        sys.path.append(str(current_dir))
        # Note: We can't import main.py directly as it starts the server
        # But we can check if the file exists and has the right structure
        main_file = current_dir / "main.py"
        if main_file.exists():
            with open(main_file, 'r') as f:
                content = f.read()
                if "PolicyImportRequest" in content and "scan/repository" in content:
                    print("✓ Main API file has new endpoints")
                else:
                    print("✗ Main API file missing new endpoints")
                    return False
        
        return True
    except Exception as e:
        print(f"✗ API import test failed: {e}")
        return False

def test_directory_structure():
    """Test if required directories exist"""
    try:
        print("\nTesting directory structure...")
        
        # Check ai engine directory
        ai_engine_dir = current_dir / "ai engine"
        if ai_engine_dir.exists():
            print("✓ AI engine directory exists")
        else:
            print("✗ AI engine directory missing")
            return False
        
        # Check for new files
        required_files = [
            "ai engine/policy_processor.py",
            "ai engine/repository_scanner.py",
            "ai engine/compliance_analyzer.py"
        ]
        
        for file_path in required_files:
            file_full_path = current_dir / file_path
            if file_full_path.exists():
                print(f"✓ {file_path} exists")
            else:
                print(f"✗ {file_path} missing")
                return False
        
        return True
    except Exception as e:
        print(f"✗ Directory structure test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("AI Compliance Auditor - Component Tests")
    print("=" * 50)
    
    tests = [
        ("Import Tests", test_imports),
        ("Basic Functionality", test_basic_functionality),
        ("API Components", test_api_imports),
        ("Directory Structure", test_directory_structure)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * 20)
        success = test_func()
        results.append((test_name, success))
    
    # Summary
    print("\n" + "=" * 50)
    print("TEST RESULTS SUMMARY")
    print("=" * 50)
    
    for test_name, success in results:
        status = "PASS" if success else "FAIL"
        print(f"{test_name}: {status}")
    
    total_passed = sum(1 for _, success in results if success)
    print(f"\nOverall: {total_passed}/{len(results)} tests passed")
    
    if total_passed == len(results):
        print("\n🎉 All tests passed! The enhanced AI compliance auditor is ready to use.")
        print("\nNext steps:")
        print("1. Run the setup script: ./setup.sh")
        print("2. Run the demo: python3 demo_enhanced_ai.py")
        print("3. Start the API server: python3 main.py")
    else:
        print("\n⚠️  Some tests failed. Please check the error messages above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())