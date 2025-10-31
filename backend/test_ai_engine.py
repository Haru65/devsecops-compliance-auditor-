#!/usr/bin/env python3
"""
Test script for AI-powered Compliance Auditor
Tests the Legal-BERT + spaCy pipeline implementation
"""

import sys
import os
import json

# Add ai engine to path
sys.path.append(os.path.join(os.path.dirname(__file__), "ai engine"))

def test_ai_engine():
    """Test the AI engine components"""
    print("Testing AI Engine Components...")
    print("=" * 50)
    
    # Test Legal-BERT Pipeline
    print("\n1. Testing Legal-BERT Pipeline...")
    try:
        from legal_bert_pipeline import LegalBERTPipeline
        
        # Initialize pipeline (this will try to download models)
        print("   Initializing Legal-BERT pipeline...")
        bert_pipeline = LegalBERTPipeline()
        
        # Test classification
        test_text = "Users must comply with all applicable laws and regulations when using this service."
        print(f"   Testing classification with: '{test_text[:50]}...'")
        
        classification_result = bert_pipeline.classify_compliance_text(test_text)
        print(f"   Classification result: {classification_result}")
        
        # Test entity extraction
        entities_result = bert_pipeline.extract_legal_entities(test_text)
        print(f"   Entities found: {len(entities_result)}")
        
        # Test compliance analysis
        compliance_result = bert_pipeline.analyze_compliance_obligations(test_text)
        print(f"   Compliance analysis completed. Score: {compliance_result.get('compliance_analysis', {}).get('compliance_score', 0)}")
        
        print("   ✅ Legal-BERT pipeline test passed!")
        
    except ImportError as e:
        print(f"   ❌ Legal-BERT dependencies not available: {e}")
    except Exception as e:
        print(f"   ⚠️  Legal-BERT test failed: {e}")
    
    # Test spaCy Entity Extractor
    print("\n2. Testing spaCy Entity Extractor...")
    try:
        from entity_extractor import LegalEntityExtractor
        
        print("   Initializing spaCy entity extractor...")
        extractor = LegalEntityExtractor()
        
        test_text = "The privacy policy must comply with GDPR regulations and protect user data."
        print(f"   Testing extraction with: '{test_text}'")
        
        extraction_result = extractor.extract_entities(test_text)
        print(f"   Entities found: {len(extraction_result.get('entities', []))}")
        print(f"   Legal patterns: {list(extraction_result.get('legal_patterns', {}).keys())}")
        print(f"   Compliance entities: {len(extraction_result.get('compliance_entities', []))}")
        
        print("   ✅ spaCy entity extractor test passed!")
        
    except ImportError as e:
        print(f"   ❌ spaCy dependencies not available: {e}")
    except Exception as e:
        print(f"   ⚠️  spaCy test failed: {e}")
    
    # Test Combined Compliance Analyzer
    print("\n3. Testing Combined Compliance Analyzer...")
    try:
        from compliance_analyzer import ComplianceAnalyzer
        
        print("   Initializing compliance analyzer...")
        analyzer = ComplianceAnalyzer()
        
        # Test pipeline status
        status = analyzer.get_pipeline_status()
        print(f"   Pipeline status: {status}")
        
        # Test comprehensive analysis
        test_text = """
        This privacy policy describes how we collect, use, and protect your personal information.
        Users must provide accurate information and comply with our terms of service.
        We may share data with third parties as required by law or with your consent.
        You have the right to request deletion of your personal data under GDPR.
        """
        
        print(f"   Testing comprehensive analysis...")
        analysis_result = analyzer.analyze_text(test_text, "comprehensive")
        
        print(f"   Analysis completed!")
        print(f"   - Compliance score: {analysis_result.get('compliance_score', 0):.2f}")
        print(f"   - Risk level: {analysis_result.get('risk_assessment', {}).get('overall_risk', 'UNKNOWN')}")
        print(f"   - Recommendations: {len(analysis_result.get('recommendations', []))}")
        print(f"   - Analysis duration: {analysis_result.get('analysis_duration', 0):.2f}s")
        
        print("   ✅ Compliance analyzer test passed!")
        
    except ImportError as e:
        print(f"   ❌ Compliance analyzer dependencies not available: {e}")
    except Exception as e:
        print(f"   ⚠️  Compliance analyzer test failed: {e}")
    
    print("\n" + "=" * 50)
    print("AI Engine Testing Complete!")

def test_simple_text():
    """Test with a simple compliance text"""
    print("\n4. Testing with Sample Legal Text...")
    
    sample_text = """
    TERMS OF SERVICE
    
    1. Acceptance of Terms
    By accessing and using this service, you accept and agree to be bound by the terms and provision of this agreement.
    
    2. Data Protection
    We collect and process personal data in accordance with GDPR regulations. Users have the right to:
    - Access their personal data
    - Request correction of inaccurate data
    - Request deletion of their data
    - Withdraw consent at any time
    
    3. Prohibited Activities
    Users shall not:
    - Violate any applicable laws or regulations
    - Infringe on intellectual property rights
    - Engage in harmful or malicious activities
    
    4. Liability and Indemnification
    The service provider shall not be liable for any damages arising from the use of this service.
    Users agree to indemnify and hold harmless the service provider from any claims.
    
    5. Governing Law
    This agreement shall be governed by and construed in accordance with the laws of [Jurisdiction].
    """
    
    try:
        from compliance_analyzer import ComplianceAnalyzer
        analyzer = ComplianceAnalyzer()
        
        print("   Analyzing sample legal document...")
        result = analyzer.analyze_text(sample_text, "comprehensive")
        
        print(f"\n   📊 ANALYSIS RESULTS:")
        print(f"   - Document type: {result.get('spacy_results', {}).get('legal_analysis', {}).get('document_type', 'unknown')}")
        print(f"   - Compliance score: {result.get('compliance_score', 0):.2f}/1.0")
        print(f"   - Risk level: {result.get('risk_assessment', {}).get('overall_risk', 'UNKNOWN')}")
        print(f"   - Entities found: {len(result.get('combined_analysis', {}).get('entities', {}).get('combined', []))}")
        print(f"   - Obligations: {len(result.get('combined_analysis', {}).get('compliance_obligations', []))}")
        
        recommendations = result.get('recommendations', [])
        if recommendations:
            print(f"\n   📋 RECOMMENDATIONS:")
            for rec in recommendations[:3]:  # Show first 3
                print(f"   - [{rec.get('priority', 'LOW')}] {rec.get('recommendation', 'No recommendation')}")
        
        print("   ✅ Sample text analysis completed!")
        
    except Exception as e:
        print(f"   ⚠️  Sample text analysis failed: {e}")

if __name__ == "__main__":
    print("🤖 AI-Powered Compliance Auditor Test Suite")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists("ai engine"):
        print("❌ Error: 'ai engine' directory not found!")
        print("Please run this script from the backend directory.")
        sys.exit(1)
    
    try:
        test_ai_engine()
        test_simple_text()
        
        print("\n🎉 All tests completed!")
        print("\nTo start the server with AI capabilities:")
        print("1. Make sure all dependencies are installed: ./setup.sh")
        print("2. Run the server: python main.py")
        print("3. Test AI endpoints at: http://localhost:8000/docs")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Test suite failed: {e}")
        import traceback
        traceback.print_exc()