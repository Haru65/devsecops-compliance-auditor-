#!/usr/bin/env python3
"""
Demo script for the enhanced AI compliance auditor
Demonstrates policy import and repository scanning functionality
"""

import os
import sys
import json
from pathlib import Path

# Add the ai engine to path
current_dir = Path(__file__).parent
ai_engine_path = current_dir / "ai engine"
sys.path.append(str(ai_engine_path))

try:
    from compliance_analyzer import ComplianceAnalyzer
    print("✓ Successfully imported ComplianceAnalyzer")
except ImportError as e:
    print(f"✗ Failed to import ComplianceAnalyzer: {e}")
    sys.exit(1)

def create_sample_policies():
    """Create sample policy documents for testing"""
    policies_dir = current_dir / "policies" / "sample_policies"
    policies_dir.mkdir(parents=True, exist_ok=True)
    
    # Sample Data Protection Policy
    data_policy = """
# Data Protection Policy

## Version: 1.0
## Date: 2024-01-01

This policy outlines our approach to data protection and privacy compliance.

### Key Requirements:

1. **Personal Data Protection**: All personal data must be encrypted both in transit and at rest.
2. **Access Controls**: Only authorized personnel shall have access to personal data.
3. **Data Retention**: Personal data must not be retained longer than necessary.
4. **Audit Logging**: All access to personal data must be logged and audited.
5. **Breach Notification**: Data breaches must be reported within 72 hours.

### Security Requirements:

- Passwords must be stored using secure hashing algorithms
- Authentication must use multi-factor authentication where possible
- All data transmissions must use TLS encryption
- Regular security audits are mandatory

### Compliance Obligations:

This policy ensures compliance with:
- GDPR (General Data Protection Regulation)
- CCPA (California Consumer Privacy Act)
- ISO 27001 Standards

### Penalties:

Violation of this policy may result in:
- Employee disciplinary action
- Financial penalties up to €20 million or 4% of annual revenue
- Legal sanctions as per applicable law
"""
    
    with open(policies_dir / "data_protection_policy.md", "w") as f:
        f.write(data_policy)
    
    # Sample Security Policy
    security_policy = """
# Information Security Policy

## Purpose
This policy establishes security requirements for all systems and applications.

## Security Controls:

### Authentication & Authorization
- All users must authenticate using strong passwords
- Multi-factor authentication is required for admin access
- User access must be reviewed quarterly

### Data Security
- Sensitive data must be encrypted using AES-256
- Database connections must use TLS
- API endpoints must implement proper authentication

### Monitoring & Logging
- Security events must be logged centrally
- Log retention period is minimum 1 year
- Automated monitoring must detect anomalies

### Incident Response
- Security incidents must be reported immediately
- Incident response plan must be activated within 1 hour
- Post-incident review is mandatory

## Enforcement
Violations will result in immediate review and potential termination.
"""
    
    with open(policies_dir / "security_policy.txt", "w") as f:
        f.write(security_policy)
    
    # Sample Privacy Policy
    privacy_policy = """
Privacy Policy - User Data Handling

This policy governs how we handle user personal information.

Data Collection:
- We collect only necessary personal data
- Consent must be obtained before data collection
- Users have the right to data portability

Data Processing:
- Personal data processing must have legal basis
- Data minimization principles must be applied
- Automated decision-making requires human oversight

User Rights:
- Right to access personal data
- Right to rectification of incorrect data
- Right to erasure (right to be forgotten)
- Right to data portability

Technical Measures:
- Implement privacy by design
- Conduct privacy impact assessments
- Regular privacy audits required
"""
    
    with open(policies_dir / "privacy_policy.txt", "w") as f:
        f.write(privacy_policy)
    
    print(f"✓ Created sample policies in: {policies_dir}")
    return str(policies_dir)

def create_sample_code_repository():
    """Create sample code repository for testing"""
    repo_dir = current_dir / "sample_repo"
    repo_dir.mkdir(parents=True, exist_ok=True)
    
    # Sample Python application with various compliance issues
    main_py = """
# Sample application with compliance issues
import os
import hashlib
import sqlite3
import requests

# ISSUE: Hardcoded password
DATABASE_PASSWORD = "admin123"  
API_KEY = "sk-1234567890abcdef"

class UserManager:
    def __init__(self):
        # ISSUE: Hardcoded database connection
        self.db_conn = sqlite3.connect("users.db")
        
    def authenticate_user(self, username, password):
        # ISSUE: Plain text password comparison
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        return self.db_conn.execute(query).fetchone()
    
    def store_personal_data(self, user_data):
        # ISSUE: No encryption for personal data
        personal_info = {
            'ssn': user_data['ssn'],
            'email': user_data['email'],
            'phone': user_data['phone']
        }
        # Store without encryption
        with open('user_data.txt', 'a') as f:
            f.write(str(personal_info) + '\\n')
    
    def log_access(self, user_id, action):
        # GOOD: Audit logging implemented
        log_entry = f"{user_id}: {action} at {os.getenv('TIMESTAMP')}"
        with open('audit.log', 'a') as f:
            f.write(log_entry + '\\n')

def make_api_call(endpoint):
    # ISSUE: No proper authentication
    headers = {'Authorization': f'Bearer {API_KEY}'}
    response = requests.get(endpoint, headers=headers, verify=False)  # ISSUE: SSL verification disabled
    return response.json()

if __name__ == "__main__":
    manager = UserManager()
    # Process users without proper validation
"""
    
    with open(repo_dir / "main.py", "w") as f:
        f.write(main_py)
    
    # Sample configuration file
    config_py = """
# Configuration with security issues
import os

# ISSUE: Hardcoded credentials
DATABASE_URL = "postgresql://admin:password123@localhost/myapp"
SECRET_KEY = "super-secret-key-that-should-not-be-hardcoded"

# ISSUE: Debug mode enabled in production
DEBUG = True

# Some good practices
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

# ISSUE: Weak encryption
ENCRYPTION_KEY = "12345678"  # Too short for proper encryption
"""
    
    with open(repo_dir / "config.py", "w") as f:
        f.write(config_py)
    
    # Sample JavaScript file
    js_file = """
// Sample JavaScript with compliance issues
const API_KEY = 'pk_live_abcd1234';  // ISSUE: Hardcoded API key

class DataHandler {
    constructor() {
        this.personalData = [];
    }
    
    // ISSUE: No encryption for personal data
    storePersonalInfo(userData) {
        this.personalData.push({
            ssn: userData.ssn,
            creditCard: userData.creditCard,
            email: userData.email
        });
    }
    
    // GOOD: Audit logging
    logAccess(userId, action) {
        console.log(`Audit: ${userId} performed ${action} at ${new Date()}`);
    }
    
    // ISSUE: No proper authentication
    authenticateUser(username, password) {
        return username === 'admin' && password === 'admin';
    }
}

// ISSUE: Sensitive data in localStorage
localStorage.setItem('user_token', 'sensitive_token_value');
"""
    
    with open(repo_dir / "app.js", "w") as f:
        f.write(js_file)
    
    print(f"✓ Created sample code repository in: {repo_dir}")
    return str(repo_dir)

def demo_policy_processing():
    """Demonstrate policy processing functionality"""
    print("\n" + "="*60)
    print("DEMO: Policy Processing and Rule Generation")
    print("="*60)
    
    try:
        # Initialize compliance analyzer
        analyzer = ComplianceAnalyzer()
        
        # Check status
        status = analyzer.get_pipeline_status()
        print(f"Pipeline Status: {status}")
        
        # Create sample policies
        policies_dir = create_sample_policies()
        
        # Import policies
        print(f"\nImporting policies from: {policies_dir}")
        import_results = analyzer.import_policies(policies_dir)
        
        if "error" in import_results:
            print(f"✗ Policy import failed: {import_results['error']}")
            return False
        
        print(f"✓ Successfully imported {import_results.get('processed_count', 0)} policies")
        print(f"  - Total files: {import_results.get('imported_count', 0)}")
        print(f"  - Failed: {import_results.get('failed_count', 0)}")
        
        # Get policy summary
        summary = analyzer.get_policy_summary()
        if "error" not in summary:
            print(f"\nPolicy Summary:")
            print(f"  - Total policies: {summary.get('total_policies', 0)}")
            print(f"  - Total rules: {summary.get('total_rules', 0)}")
            print(f"  - Categories: {list(summary.get('categories', {}).keys())}")
        
        # Get compliance rules
        rules = analyzer.get_compliance_rules()
        if "error" not in rules:
            print(f"\nGenerated {len(rules.get('rules', []))} compliance rules")
            print(f"Rule categories: {rules.get('categories', [])}")
        
        return True
        
    except Exception as e:
        print(f"✗ Policy processing demo failed: {e}")
        return False

def demo_repository_scanning():
    """Demonstrate repository scanning functionality"""
    print("\n" + "="*60)
    print("DEMO: Repository Compliance Scanning")
    print("="*60)
    
    try:
        # Initialize compliance analyzer
        analyzer = ComplianceAnalyzer()
        
        # Create sample repository
        repo_dir = create_sample_code_repository()
        
        # Scan repository
        print(f"\nScanning repository: {repo_dir}")
        scan_results = analyzer.scan_repository(repo_dir)
        
        if "error" in scan_results:
            print(f"✗ Repository scan failed: {scan_results['error']}")
            return False
        
        # Display results
        summary = scan_results.get("scan_summary", {})
        print(f"✓ Repository scan completed in {scan_results.get('scan_duration', 0):.2f}s")
        print(f"  - Files scanned: {summary.get('total_files_scanned', 0)}")
        print(f"  - Total violations: {summary.get('total_violations', 0)}")
        print(f"  - Compliance score: {scan_results.get('compliance_score', 0):.1%}")
        
        # Show severity breakdown
        severity = summary.get("severity_breakdown", {})
        print(f"  - High severity: {severity.get('HIGH', 0)}")
        print(f"  - Medium severity: {severity.get('MEDIUM', 0)}")
        print(f"  - Low severity: {severity.get('LOW', 0)}")
        
        # Show category breakdown
        categories = summary.get("category_breakdown", {})
        if categories:
            print(f"  - Violation categories: {list(categories.keys())}")
        
        # Show some violations
        violations = scan_results.get("violations", [])
        if violations:
            print(f"\nSample violations (showing first 5):")
            for i, violation in enumerate(violations[:5]):
                print(f"  {i+1}. {violation.get('description', 'No description')}")
                print(f"     File: {violation.get('file_path', 'Unknown')}")
                print(f"     Severity: {violation.get('severity', 'Unknown')}")
                print(f"     Line: {violation.get('line_number', 'Unknown')}")
                print()
        
        return True
        
    except Exception as e:
        print(f"✗ Repository scanning demo failed: {e}")
        return False

def demo_comprehensive_analysis():
    """Demonstrate comprehensive compliance analysis"""
    print("\n" + "="*60)
    print("DEMO: Comprehensive Compliance Analysis")
    print("="*60)
    
    try:
        # Initialize compliance analyzer
        analyzer = ComplianceAnalyzer()
        
        # Create sample data
        policies_dir = create_sample_policies()
        repo_dir = create_sample_code_repository()
        
        # Run comprehensive analysis
        print(f"Running comprehensive analysis...")
        print(f"  - Policies: {policies_dir}")
        print(f"  - Repository: {repo_dir}")
        
        analysis_results = analyzer.comprehensive_compliance_analysis(
            repo_path=repo_dir,
            policies_folder=policies_dir
        )
        
        if "error" in analysis_results:
            print(f"✗ Comprehensive analysis failed: {analysis_results['error']}")
            return False
        
        # Display results
        print(f"✓ Comprehensive analysis completed in {analysis_results.get('analysis_duration', 0):.2f}s")
        
        # Policy import results
        policy_import = analysis_results.get("policy_import", {})
        print(f"\nPolicy Import:")
        print(f"  - Policies processed: {policy_import.get('processed_count', 0)}")
        
        # Repository scan results
        repo_scan = analysis_results.get("repository_scan", {})
        scan_summary = repo_scan.get("scan_summary", {})
        print(f"\nRepository Scan:")
        print(f"  - Files scanned: {scan_summary.get('total_files_scanned', 0)}")
        print(f"  - Total violations: {scan_summary.get('total_violations', 0)}")
        print(f"  - Compliance score: {repo_scan.get('compliance_score', 0):.1%}")
        
        # Compliance summary
        compliance_summary = analysis_results.get("compliance_summary", {})
        print(f"\nCompliance Summary:")
        print(f"  - Risk level: {compliance_summary.get('risk_level', 'Unknown')}")
        print(f"  - Rules generated: {compliance_summary.get('compliance_rules_generated', 0)}")
        
        # Recommendations
        recommendations = analysis_results.get("recommendations", [])
        if recommendations:
            print(f"\nRecommendations:")
            for i, rec in enumerate(recommendations[:3]):
                print(f"  {i+1}. [{rec.get('priority', 'UNKNOWN')}] {rec.get('recommendation', 'No recommendation')}")
        
        return True
        
    except Exception as e:
        print(f"✗ Comprehensive analysis demo failed: {e}")
        return False

def main():
    """Run all demonstrations"""
    print("AI Compliance Auditor - Enhanced Demo")
    print("=====================================")
    
    # Check if AI components are available
    try:
        analyzer = ComplianceAnalyzer()
        status = analyzer.get_pipeline_status()
        print(f"Available pipelines: {status.get('pipelines_loaded', [])}")
    except Exception as e:
        print(f"⚠️  AI engine initialization warning: {e}")
        print("Continuing with available components...")
    
    results = []
    
    # Run demonstrations
    print("\nRunning demonstrations...")
    
    results.append(("Policy Processing", demo_policy_processing()))
    results.append(("Repository Scanning", demo_repository_scanning()))
    results.append(("Comprehensive Analysis", demo_comprehensive_analysis()))
    
    # Summary
    print("\n" + "="*60)
    print("DEMO RESULTS SUMMARY")
    print("="*60)
    
    for demo_name, success in results:
        status = "✓ PASSED" if success else "✗ FAILED"
        print(f"{demo_name}: {status}")
    
    total_passed = sum(1 for _, success in results if success)
    print(f"\nOverall: {total_passed}/{len(results)} demonstrations passed")
    
    if total_passed == len(results):
        print("\n🎉 All demonstrations completed successfully!")
        print("\nNext steps:")
        print("1. Import your legal policies into the 'policies' folder")
        print("2. Use the API endpoints to scan your repositories")
        print("3. Review compliance reports and implement recommendations")
    else:
        print("\n⚠️  Some demonstrations failed. Check the error messages above.")

if __name__ == "__main__":
    main()