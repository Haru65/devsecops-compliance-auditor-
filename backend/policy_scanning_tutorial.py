#!/usr/bin/env python3
"""
Policy Scanning Tutorial
Shows how to scan and import legal policies step by step
"""

import sys
import os
from pathlib import Path

# Add the ai engine to path
current_dir = Path(__file__).parent
ai_engine_path = current_dir / "ai engine"
sys.path.append(str(ai_engine_path))

from compliance_analyzer import ComplianceAnalyzer

def scan_policies_step_by_step():
    """
    Step-by-step tutorial for scanning policies
    """
    
    print("🔍 POLICY SCANNING TUTORIAL")
    print("=" * 50)
    
    # Step 1: Initialize the analyzer
    print("\n📋 Step 1: Initialize Compliance Analyzer")
    analyzer = ComplianceAnalyzer()
    
    # Check what's available
    status = analyzer.get_pipeline_status()
    print(f"Available components: {status['pipelines_loaded']}")
    
    # Step 2: Create sample policies if they don't exist
    print("\n📁 Step 2: Prepare Policy Documents")
    policies_dir = current_dir / "policies" / "my_policies"
    policies_dir.mkdir(parents=True, exist_ok=True)
    
    # Create a sample GDPR policy
    gdpr_policy = """
# GDPR Compliance Policy

## Data Protection Requirements

### Article 25: Data Protection by Design
- Personal data processing must implement appropriate technical and organizational measures
- Data protection must be integrated into processing activities from the outset
- Privacy settings must be set to the most protective by default

### Article 32: Security of Processing
- Implement appropriate technical and organizational measures to ensure data security
- Use encryption of personal data where appropriate
- Ensure ongoing confidentiality, integrity, availability and resilience of systems
- Regular testing and evaluation of security measures is required

### Article 33: Breach Notification
- Data breaches must be reported to supervisory authority within 72 hours
- High-risk breaches must be communicated to data subjects without undue delay
- Maintain records of all personal data breaches

### Data Subject Rights (Articles 15-22)
- Right of access: Provide copy of personal data upon request
- Right to rectification: Correct inaccurate personal data
- Right to erasure: Delete personal data when no longer needed
- Right to data portability: Provide data in machine-readable format

### Technical Requirements
- Use strong encryption for data at rest and in transit
- Implement access controls and authentication
- Regular security audits and penetration testing
- Data minimization and purpose limitation
- Consent management systems required
    """
    
    with open(policies_dir / "gdpr_policy.md", "w") as f:
        f.write(gdpr_policy)
    
    # Create a security policy
    security_policy = """
Information Security Policy

1. PASSWORD REQUIREMENTS
- Passwords must be at least 12 characters long
- Must contain uppercase, lowercase, numbers, and special characters
- Passwords must not be stored in plain text
- Multi-factor authentication required for admin access

2. DATA ENCRYPTION
- All sensitive data must be encrypted using AES-256
- Database connections must use TLS 1.2 or higher
- API communications must use HTTPS only
- Encryption keys must be rotated every 90 days

3. ACCESS CONTROL
- Principle of least privilege must be enforced
- User access must be reviewed quarterly
- Shared accounts are prohibited
- Session timeouts must be implemented

4. LOGGING AND MONITORING
- All access to sensitive data must be logged
- Security logs must be retained for 2 years
- Real-time monitoring for suspicious activities
- Automated alerts for security incidents

5. VULNERABILITY MANAGEMENT
- Regular security assessments required
- Critical vulnerabilities must be patched within 48 hours
- Penetration testing annually
- Code security reviews for all releases
    """
    
    with open(policies_dir / "security_policy.txt", "w") as f:
        f.write(security_policy)
    
    print(f"✅ Created sample policies in: {policies_dir}")
    
    # Step 3: Import and scan the policies
    print("\n🔄 Step 3: Import and Process Policies")
    
    try:
        # Import the policies
        import_results = analyzer.import_policies(str(policies_dir))
        
        if "error" in import_results:
            print(f"❌ Error importing policies: {import_results['error']}")
            return
        
        print(f"✅ Successfully imported {import_results.get('processed_count', 0)} policies")
        print(f"   📊 Total files processed: {import_results.get('imported_count', 0)}")
        print(f"   ❌ Failed files: {import_results.get('failed_count', 0)}")
        
        # Show some details about the imported policies
        policies = import_results.get('policies', [])
        for policy in policies:
            print(f"\n   📄 Policy: {policy.get('policy_id', 'Unknown')}")
            print(f"      Status: {policy.get('processing_status', 'Unknown')}")
            print(f"      Categories: {[c.get('category') for c in policy.get('categories', [])]}")
            print(f"      Rules generated: {len(policy.get('compliance_rules', []))}")
    
    except Exception as e:
        print(f"❌ Error during policy import: {e}")
        return
    
    # Step 4: Get policy summary
    print("\n📊 Step 4: Policy Summary")
    try:
        summary = analyzer.get_policy_summary()
        if "error" not in summary:
            print(f"📁 Total policies: {summary.get('total_policies', 0)}")
            print(f"⚖️  Total compliance rules: {summary.get('total_rules', 0)}")
            print(f"📂 Categories found: {list(summary.get('categories', {}).keys())}")
            
            # Show category breakdown
            categories = summary.get('categories', {})
            for category, count in categories.items():
                print(f"   - {category}: {count} policies")
    
    except Exception as e:
        print(f"❌ Error getting policy summary: {e}")
    
    # Step 5: Get generated compliance rules
    print("\n⚖️  Step 5: Generated Compliance Rules")
    try:
        rules = analyzer.get_compliance_rules()
        if "error" not in rules:
            rules_list = rules.get('rules', [])
            print(f"📋 Generated {len(rules_list)} compliance rules")
            
            # Show first few rules as examples
            print("\n🔍 Sample Rules:")
            for i, rule in enumerate(rules_list[:3]):
                print(f"\n   Rule {i+1}: {rule.get('rule_id', 'Unknown')}")
                print(f"   📝 Description: {rule.get('description', 'No description')[:100]}...")
                print(f"   📂 Category: {rule.get('category', 'Unknown')}")
                print(f"   ⚠️  Severity: {rule.get('severity', 'Unknown')}")
                print(f"   🔍 Scan patterns: {rule.get('scan_patterns', [])}")
            
            if len(rules_list) > 3:
                print(f"\n   ... and {len(rules_list) - 3} more rules")
    
    except Exception as e:
        print(f"❌ Error getting compliance rules: {e}")
    
    # Step 6: Show where the data is stored
    print("\n💾 Step 6: Data Storage")
    print(f"📁 Policies stored in: {current_dir / 'policies'}")
    print("   - processed_policies.json: Full policy data")
    print("   - compliance_rules.json: Generated compliance rules")
    
    # Check if JSON files were created
    json_files = [
        current_dir / "policies" / "processed_policies.json",
        current_dir / "policies" / "compliance_rules.json"
    ]
    
    for json_file in json_files:
        if json_file.exists():
            print(f"   ✅ {json_file.name} created")
        else:
            print(f"   ❌ {json_file.name} not found")
    
    print("\n🎉 Policy scanning completed successfully!")
    print("\n📋 Next Steps:")
    print("1. Add your own policy documents to the 'policies' folder")
    print("2. Use the compliance rules to scan code repositories")
    print("3. Review and customize the generated rules as needed")
    print("4. Integrate with your CI/CD pipeline for automated compliance checking")

def show_policy_files():
    """Show existing policy files and their content"""
    print("\n📁 EXISTING POLICY FILES")
    print("=" * 30)
    
    policies_base = current_dir / "policies"
    
    # Check different policy directories
    policy_dirs = [
        policies_base / "sample_policies",
        policies_base / "my_policies",
        policies_base
    ]
    
    for policy_dir in policy_dirs:
        if policy_dir.exists():
            print(f"\n📂 Directory: {policy_dir}")
            
            # List policy files
            policy_files = []
            for ext in ['.txt', '.md', '.pdf', '.doc', '.docx']:
                policy_files.extend(policy_dir.glob(f'*{ext}'))
            
            if policy_files:
                for file_path in policy_files:
                    print(f"   📄 {file_path.name}")
                    try:
                        # Show first few lines of text files
                        if file_path.suffix.lower() in ['.txt', '.md']:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                lines = f.readlines()[:3]
                                for line in lines:
                                    print(f"      {line.strip()}")
                                if len(lines) >= 3:
                                    print("      ...")
                    except Exception as e:
                        print(f"      (Could not read: {e})")
            else:
                print("   (No policy files found)")

def main():
    """Main function to run the policy scanning tutorial"""
    print("🚀 Welcome to the Policy Scanning Tutorial!")
    print("\nThis tutorial will show you how to:")
    print("1. Import legal policy documents")
    print("2. Convert them to compliance rules using AI")
    print("3. Use the rules for repository scanning")
    
    choice = input("\nChoose an option:\n1. Run full tutorial\n2. Show existing policy files\n3. Both\nEnter choice (1/2/3): ")
    
    if choice in ['2', '3']:
        show_policy_files()
    
    if choice in ['1', '3']:
        scan_policies_step_by_step()

if __name__ == "__main__":
    main()