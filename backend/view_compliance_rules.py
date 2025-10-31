#!/usr/bin/env python3
"""
Policy Rules Viewer - Examine generated compliance rules
"""

import json
import sys
from pathlib import Path

def view_compliance_rules():
    """View and analyze the generated compliance rules"""
    
    print("📋 COMPLIANCE RULES VIEWER")
    print("=" * 40)
    
    # Load the compliance rules
    rules_file = Path("policies/compliance_rules.json")
    policies_file = Path("policies/processed_policies.json")
    
    if not rules_file.exists():
        print("❌ No compliance rules found. Run policy scanning first.")
        return
    
    # Load rules
    with open(rules_file, 'r', encoding='utf-8') as f:
        rules = json.load(f)
    
    print(f"📊 Total Rules: {len(rules)}")
    
    # Analyze rules by category
    categories = {}
    severity_counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
    
    for rule_id, rule in rules.items():
        category = rule.get('category', 'unknown')
        severity = rule.get('severity', 'LOW')
        
        categories[category] = categories.get(category, 0) + 1
        severity_counts[severity] = severity_counts.get(severity, 0) + 1
    
    print(f"\n📂 Rules by Category:")
    for category, count in sorted(categories.items()):
        print(f"   {category}: {count} rules")
    
    print(f"\n⚠️  Rules by Severity:")
    for severity, count in severity_counts.items():
        print(f"   {severity}: {count} rules")
    
    # Show detailed rules
    print(f"\n🔍 DETAILED RULES:")
    print("-" * 80)
    
    for i, (rule_id, rule) in enumerate(rules.items()):
        if i >= 10:  # Show first 10 rules
            print(f"\n... and {len(rules) - 10} more rules")
            break
            
        print(f"\n🔧 Rule {i+1}: {rule_id}")
        print(f"   📝 Description: {rule.get('description', 'No description')[:100]}...")
        print(f"   📂 Category: {rule.get('category', 'Unknown')}")
        print(f"   ⚠️  Severity: {rule.get('severity', 'Unknown')}")
        print(f"   🎯 Confidence: {rule.get('confidence', 'Unknown')}")
        
        patterns = rule.get('scan_patterns', [])
        if patterns:
            print(f"   🔍 Scan Patterns ({len(patterns)}): {', '.join(patterns[:5])}")
            if len(patterns) > 5:
                print(f"       ... and {len(patterns) - 5} more patterns")
        
        compliance_check = rule.get('compliance_check', {})
        if compliance_check:
            check_type = compliance_check.get('check_type', 'Unknown')
            print(f"   ✅ Check Type: {check_type}")

def view_processed_policies():
    """View the processed policies"""
    
    print("\n📄 PROCESSED POLICIES")
    print("=" * 40)
    
    policies_file = Path("policies/processed_policies.json")
    
    if not policies_file.exists():
        print("❌ No processed policies found.")
        return
    
    with open(policies_file, 'r', encoding='utf-8') as f:
        policies = json.load(f)
    
    print(f"📊 Total Policies: {len(policies)}")
    
    for policy_id, policy in policies.items():
        print(f"\n📄 Policy: {policy_id}")
        print(f"   📁 File: {policy.get('file_path', 'Unknown')}")
        print(f"   ✅ Status: {policy.get('processing_status', 'Unknown')}")
        print(f"   📊 Word Count: {policy.get('metadata', {}).get('word_count', 'Unknown')}")
        
        categories = policy.get('categories', [])
        if categories:
            category_names = [c.get('category', 'Unknown') for c in categories]
            print(f"   📂 Categories: {', '.join(category_names)}")
        
        rules = policy.get('compliance_rules', [])
        print(f"   ⚖️  Generated Rules: {len(rules)}")
        
        requirements = policy.get('key_requirements', [])
        print(f"   📋 Key Requirements: {len(requirements)}")
        
        if requirements:
            print(f"   🔍 Sample Requirements:")
            for i, req in enumerate(requirements[:2]):
                req_text = req.get('requirement', 'No requirement')[:80]
                print(f"      {i+1}. {req_text}...")

def search_rules_by_pattern():
    """Search compliance rules by scan pattern"""
    
    print("\n🔍 PATTERN SEARCH")
    print("=" * 40)
    
    pattern = input("Enter a pattern to search for (e.g., 'password', 'encryption', 'data'): ").lower()
    
    rules_file = Path("policies/compliance_rules.json")
    if not rules_file.exists():
        print("❌ No compliance rules found.")
        return
    
    with open(rules_file, 'r', encoding='utf-8') as f:
        rules = json.load(f)
    
    matching_rules = []
    
    for rule_id, rule in rules.items():
        # Search in scan patterns
        patterns = rule.get('scan_patterns', [])
        if any(pattern in p.lower() for p in patterns):
            matching_rules.append((rule_id, rule))
        
        # Search in description
        description = rule.get('description', '').lower()
        if pattern in description:
            matching_rules.append((rule_id, rule))
    
    # Remove duplicates
    unique_rules = []
    seen_ids = set()
    for rule_id, rule in matching_rules:
        if rule_id not in seen_ids:
            unique_rules.append((rule_id, rule))
            seen_ids.add(rule_id)
    
    print(f"\n🎯 Found {len(unique_rules)} rules matching '{pattern}':")
    
    for rule_id, rule in unique_rules:
        print(f"\n🔧 {rule_id}")
        print(f"   📝 {rule.get('description', 'No description')[:100]}...")
        print(f"   📂 Category: {rule.get('category', 'Unknown')}")
        print(f"   ⚠️  Severity: {rule.get('severity', 'Unknown')}")
        
        patterns = rule.get('scan_patterns', [])
        matching_patterns = [p for p in patterns if pattern in p.lower()]
        if matching_patterns:
            print(f"   🎯 Matching patterns: {', '.join(matching_patterns)}")

def export_rules_for_scanning():
    """Export rules in a format suitable for external tools"""
    
    print("\n💾 EXPORT RULES")
    print("=" * 40)
    
    rules_file = Path("policies/compliance_rules.json")
    if not rules_file.exists():
        print("❌ No compliance rules found.")
        return
    
    with open(rules_file, 'r', encoding='utf-8') as f:
        rules = json.load(f)
    
    # Create different export formats
    
    # 1. Simple pattern list
    all_patterns = set()
    for rule in rules.values():
        patterns = rule.get('scan_patterns', [])
        all_patterns.update(patterns)
    
    with open('exported_scan_patterns.txt', 'w') as f:
        for pattern in sorted(all_patterns):
            f.write(f"{pattern}\n")
    
    print(f"✅ Exported {len(all_patterns)} unique scan patterns to: exported_scan_patterns.txt")
    
    # 2. Rules by category
    categories = {}
    for rule in rules.values():
        category = rule.get('category', 'unknown')
        if category not in categories:
            categories[category] = []
        categories[category].append(rule)
    
    with open('rules_by_category.json', 'w') as f:
        json.dump(categories, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Exported rules by category to: rules_by_category.json")
    
    # 3. High severity rules only
    high_severity_rules = {
        rule_id: rule for rule_id, rule in rules.items() 
        if rule.get('severity') == 'HIGH'
    }
    
    with open('high_severity_rules.json', 'w') as f:
        json.dump(high_severity_rules, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Exported {len(high_severity_rules)} high-severity rules to: high_severity_rules.json")

def main():
    """Main menu for viewing compliance rules"""
    
    while True:
        print("\n" + "="*50)
        print("📋 COMPLIANCE RULES ANALYSIS MENU")
        print("="*50)
        print("1. View all compliance rules")
        print("2. View processed policies")
        print("3. Search rules by pattern")
        print("4. Export rules for external tools")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ")
        
        if choice == '1':
            view_compliance_rules()
        elif choice == '2':
            view_processed_policies()
        elif choice == '3':
            search_rules_by_pattern()
        elif choice == '4':
            export_rules_for_scanning()
        elif choice == '5':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()