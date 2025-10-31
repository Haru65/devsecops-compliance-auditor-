#!/usr/bin/env python3
"""
Demo script showing Legal-BERT + spaCy compliance analysis
Run this to see the AI engine in action
"""

def demo_ai_compliance():
    """Demonstrate AI compliance analysis with various text types"""
    
    print("🚀 Legal-BERT + spaCy Compliance Analysis Demo")
    print("=" * 60)
    
    # Sample texts for different compliance scenarios
    samples = {
        "Privacy Policy": """
        We collect personal information including names, email addresses, and usage data.
        This data is processed in accordance with GDPR and CCPA regulations.
        Users have the right to access, correct, or delete their personal information.
        We may share data with third-party processors who are bound by confidentiality agreements.
        Data retention periods vary by data type but do not exceed legal requirements.
        """,
        
        "Terms of Service": """
        By using this service, you agree to comply with all applicable laws and regulations.
        You must not engage in prohibited activities including fraud, harassment, or illegal content distribution.
        The service provider reserves the right to terminate accounts for violations.
        Users are liable for any damages resulting from misuse of the service.
        This agreement is governed by the laws of California, United States.
        """,
        
        "Software License": """
        Permission is hereby granted to use, copy, modify, and distribute this software.
        The software is provided "as is" without warranty of any kind.
        Users must include copyright notices in all copies or substantial portions.
        Commercial use requires a separate license agreement.
        Liability is limited to the maximum extent permitted by law.
        """,
        
        "Employment Contract": """
        The employee agrees to maintain confidentiality of proprietary information.
        Compensation includes salary, benefits, and performance-based bonuses.
        Either party may terminate employment with 30 days written notice.
        Non-compete restrictions apply for 12 months post-employment.
        Disputes shall be resolved through binding arbitration.
        """,
        
        "Data Processing Agreement": """
        The processor shall implement appropriate technical and organizational measures.
        Personal data must be processed only on documented instructions from the controller.
        Data subjects' rights must be facilitated including access and portability.
        Data breaches must be reported within 72 hours of discovery.
        Cross-border transfers require adequate safeguards or adequacy decisions.
        """
    }
    
    try:
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), "ai engine"))
        
        from compliance_analyzer import ComplianceAnalyzer
        
        print("🤖 Initializing AI Compliance Analyzer...")
        analyzer = ComplianceAnalyzer()
        
        # Check pipeline status
        status = analyzer.get_pipeline_status()
        print(f"📊 Pipeline Status: {status}")
        print()
        
        # Analyze each sample
        for doc_type, text in samples.items():
            print(f"📄 Analyzing: {doc_type}")
            print("-" * 40)
            
            # Run comprehensive analysis
            result = analyzer.analyze_text(text.strip(), "comprehensive")
            
            # Extract key metrics
            compliance_score = result.get('compliance_score', 0)
            risk_level = result.get('risk_assessment', {}).get('overall_risk', 'UNKNOWN')
            entities_count = len(result.get('combined_analysis', {}).get('entities', {}).get('combined', []))
            obligations_count = len(result.get('combined_analysis', {}).get('compliance_obligations', []))
            duration = result.get('analysis_duration', 0)
            
            # Display results
            print(f"✅ Analysis completed in {duration:.2f}s")
            print(f"📊 Compliance Score: {compliance_score:.2f}/1.0")
            print(f"⚠️  Risk Level: {risk_level}")
            print(f"🏷️  Entities Found: {entities_count}")
            print(f"📋 Obligations: {obligations_count}")
            
            # Show top recommendations
            recommendations = result.get('recommendations', [])
            if recommendations:
                print("💡 Top Recommendations:")
                for i, rec in enumerate(recommendations[:2], 1):
                    priority = rec.get('priority', 'LOW')
                    recommendation = rec.get('recommendation', 'No recommendation')
                    print(f"   {i}. [{priority}] {recommendation}")
            
            # Show key entities
            entities = result.get('combined_analysis', {}).get('entities', {}).get('combined', [])[:3]
            if entities:
                print("🎯 Key Entities:")
                for entity in entities:
                    text = entity.get('text', 'Unknown')
                    label = entity.get('label', 'Unknown')
                    confidence = entity.get('confidence', 0)
                    print(f"   - {text} ({label}, {confidence:.2f})")
            
            print()
        
        print("🎉 Demo completed successfully!")
        print("\n📚 Understanding the Results:")
        print("• Compliance Score: 0.0-1.0 (higher = more compliant)")
        print("• Risk Level: LOW/MEDIUM/HIGH (compliance risk assessment)")
        print("• Entities: Legal concepts, organizations, regulations identified")
        print("• Obligations: Compliance requirements and duties extracted")
        print("• Recommendations: AI-generated compliance improvement suggestions")
        
    except ImportError as e:
        print(f"❌ AI dependencies not available: {e}")
        print("\nTo install dependencies:")
        print("1. Run: ./setup.sh")
        print("2. Or manually: pip install torch transformers spacy")
        print("3. Download models: python -m spacy download en_core_web_sm")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    demo_ai_compliance()