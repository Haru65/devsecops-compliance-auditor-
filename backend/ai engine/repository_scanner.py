"""
Repository Scanner - AI Engine Component for Code Compliance Scanning
Scans repositories using AI-generated compliance rules from policies
"""

import logging
import os
import json
from typing import Dict, List, Any, Optional
from pathlib import Path
import re
from datetime import datetime
import asyncio

logger = logging.getLogger(__name__)

class RepositoryScanner:
    """
    Scans repositories for compliance violations using AI-generated rules
    """
    
    def __init__(self, policy_processor=None):
        """
        Initialize repository scanner
        
        Args:
            policy_processor: PolicyProcessor instance for accessing compliance rules
        """
        self.policy_processor = policy_processor
        self.compliance_rules = {}
        self.scan_patterns = {}
        self.scan_results = {}
        
        self._load_compliance_rules()
    
    def _load_compliance_rules(self):
        """Load compliance rules from policy processor"""
        if self.policy_processor:
            rules_data = self.policy_processor.get_compliance_rules_for_scanning()
            self.compliance_rules = {rule["rule_id"]: rule for rule in rules_data["rules"]}
            self.scan_patterns = rules_data["scan_patterns"]
            logger.info(f"Loaded {len(self.compliance_rules)} compliance rules for scanning")
        else:
            logger.warning("No policy processor available, using default rules")
            self._load_default_rules()
    
    def _load_default_rules(self):
        """Load default compliance rules when policy processor is unavailable"""
        self.compliance_rules = {
            "security_001": {
                "rule_id": "security_001",
                "description": "Passwords should not be hardcoded",
                "category": "security",
                "severity": "HIGH",
                "scan_patterns": ["password", "pwd", "passwd"],
                "compliance_check": {"check_type": "pattern_match"}
            },
            "data_001": {
                "rule_id": "data_001", 
                "description": "Personal data handling requires proper protection",
                "category": "data_protection",
                "severity": "HIGH",
                "scan_patterns": ["personal_data", "pii", "sensitive"],
                "compliance_check": {"check_type": "pattern_match"}
            },
            "logging_001": {
                "rule_id": "logging_001",
                "description": "Audit logging should be implemented",
                "category": "compliance",
                "severity": "MEDIUM", 
                "scan_patterns": ["log", "audit", "trace"],
                "compliance_check": {"check_type": "pattern_match"}
            }
        }
        
        self.scan_patterns = {
            "security": ["password", "pwd", "passwd", "auth", "token"],
            "data_protection": ["personal_data", "pii", "sensitive", "confidential"],
            "compliance": ["log", "audit", "trace", "record", "monitor"]
        }
    
    def scan_repository(self, repo_path: str, file_extensions: List[str] = None) -> Dict[str, Any]:
        """
        Scan repository for compliance violations
        
        Args:
            repo_path: Path to repository root
            file_extensions: File extensions to scan (default: common code files)
            
        Returns:
            Comprehensive scan results
        """
        scan_start = datetime.now()
        
        if file_extensions is None:
            file_extensions = ['.py', '.js', '.ts', '.java', '.cpp', '.c', '.cs', '.php', '.rb', '.go']
        
        results = {
            "repository_path": repo_path,
            "scan_timestamp": scan_start.isoformat(),
            "scan_summary": {},
            "violations": [],
            "compliance_score": 0.0,
            "scanned_files": [],
            "rules_applied": len(self.compliance_rules),
            "scan_duration": 0
        }
        
        try:
            repo_path = Path(repo_path)
            if not repo_path.exists():
                raise FileNotFoundError(f"Repository path not found: {repo_path}")
            
            # Find all code files
            code_files = []
            for ext in file_extensions:
                code_files.extend(repo_path.rglob(f'*{ext}'))
            
            logger.info(f"Scanning {len(code_files)} files in {repo_path}")
            
            # Scan each file
            for file_path in code_files:
                try:
                    file_results = self._scan_file(file_path)
                    if file_results:
                        results["scanned_files"].append(file_results)
                        results["violations"].extend(file_results.get("violations", []))
                        
                except Exception as e:
                    logger.error(f"Failed to scan file {file_path}: {e}")
                    results["violations"].append({
                        "file_path": str(file_path),
                        "violation_type": "scan_error",
                        "message": f"Failed to scan file: {str(e)}",
                        "severity": "LOW"
                    })
            
            # Calculate compliance metrics
            results["scan_summary"] = self._calculate_scan_summary(results)
            results["compliance_score"] = self._calculate_compliance_score(results)
            
            # Calculate scan duration
            scan_end = datetime.now()
            results["scan_duration"] = (scan_end - scan_start).total_seconds()
            
            logger.info(f"Repository scan completed: {len(results['violations'])} violations found")
            return results
            
        except Exception as e:
            logger.error(f"Repository scan failed: {e}")
            return {
                "repository_path": repo_path,
                "scan_timestamp": scan_start.isoformat(),
                "error": str(e),
                "scan_duration": (datetime.now() - scan_start).total_seconds()
            }
    
    def _scan_file(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """
        Scan individual file for compliance violations
        
        Args:
            file_path: Path to file to scan
            
        Returns:
            File scan results or None if file couldn't be scanned
        """
        try:
            # Read file content
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            file_results = {
                "file_path": str(file_path),
                "file_size": len(content),
                "line_count": len(content.split('\n')),
                "violations": [],
                "compliance_checks": []
            }
            
            # Apply each compliance rule
            for rule_id, rule in self.compliance_rules.items():
                violations = self._apply_rule_to_file(content, file_path, rule)
                file_results["violations"].extend(violations)
                
                # Record compliance check
                file_results["compliance_checks"].append({
                    "rule_id": rule_id,
                    "violations_found": len(violations),
                    "category": rule.get("category", "unknown")
                })
            
            return file_results
            
        except Exception as e:
            logger.error(f"File scan failed for {file_path}: {e}")
            return None
    
    def _apply_rule_to_file(self, content: str, file_path: Path, rule: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Apply a specific compliance rule to file content
        
        Args:
            content: File content
            file_path: Path to file
            rule: Compliance rule to apply
            
        Returns:
            List of violations found
        """
        violations = []
        
        try:
            scan_patterns = rule.get("scan_patterns", [])
            rule_id = rule.get("rule_id", "unknown")
            category = rule.get("category", "unknown")
            severity = rule.get("severity", "MEDIUM")
            description = rule.get("description", "Compliance rule violation")
            
            # Pattern-based scanning
            for pattern in scan_patterns:
                violations.extend(self._find_pattern_violations(
                    content, file_path, pattern, rule_id, category, severity, description
                ))
            
            # Additional rule-specific checks
            compliance_check = rule.get("compliance_check", {})
            check_type = compliance_check.get("check_type", "pattern_match")
            
            if check_type == "pattern_match":
                # Already handled above
                pass
            elif check_type == "function_analysis":
                violations.extend(self._analyze_functions(content, file_path, rule))
            elif check_type == "import_analysis":
                violations.extend(self._analyze_imports(content, file_path, rule))
            
            return violations
            
        except Exception as e:
            logger.error(f"Rule application failed for {rule.get('rule_id', 'unknown')}: {e}")
            return []
    
    def _find_pattern_violations(self, content: str, file_path: Path, pattern: str, 
                               rule_id: str, category: str, severity: str, description: str) -> List[Dict[str, Any]]:
        """Find pattern-based violations in file content"""
        violations = []
        lines = content.split('\n')
        
        # Create regex pattern (case-insensitive)
        try:
            regex_pattern = re.compile(pattern, re.IGNORECASE)
        except re.error:
            # If pattern is not valid regex, treat as literal string
            regex_pattern = re.compile(re.escape(pattern), re.IGNORECASE)
        
        for line_num, line in enumerate(lines, 1):
            matches = regex_pattern.finditer(line)
            for match in matches:
                # Skip matches in comments (basic check)
                if self._is_in_comment(line, match.start()):
                    continue
                
                violation = {
                    "rule_id": rule_id,
                    "file_path": str(file_path),
                    "line_number": line_num,
                    "column_start": match.start(),
                    "column_end": match.end(),
                    "matched_text": match.group(),
                    "line_content": line.strip(),
                    "category": category,
                    "severity": severity,
                    "description": description,
                    "suggestion": self._generate_suggestion(pattern, category)
                }
                violations.append(violation)
        
        return violations
    
    def _is_in_comment(self, line: str, position: int) -> bool:
        """Check if position is within a comment"""
        # Basic comment detection for common languages
        comment_markers = ['#', '//', '/*', '*', '<!--']
        
        line_before_pos = line[:position]
        for marker in comment_markers:
            if marker in line_before_pos:
                marker_pos = line_before_pos.rfind(marker)
                if marker_pos < position:
                    return True
        
        return False
    
    def _generate_suggestion(self, pattern: str, category: str) -> str:
        """Generate suggestion for fixing violation"""
        suggestions = {
            "password": "Use environment variables or secure credential management",
            "pwd": "Use environment variables or secure credential management", 
            "passwd": "Use environment variables or secure credential management",
            "personal_data": "Implement proper data protection measures (encryption, access controls)",
            "pii": "Handle personally identifiable information according to privacy regulations",
            "sensitive": "Apply appropriate security controls for sensitive data",
            "log": "Ensure audit logging includes necessary compliance information",
            "audit": "Implement comprehensive audit trails for compliance",
            "auth": "Use secure authentication mechanisms",
            "token": "Implement secure token management practices"
        }
        
        return suggestions.get(pattern.lower(), f"Review {category} compliance requirements")
    
    def _analyze_functions(self, content: str, file_path: Path, rule: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze function definitions for compliance"""
        violations = []
        
        # Basic function detection patterns for common languages
        function_patterns = [
            r'def\s+(\w+)\s*\(',  # Python
            r'function\s+(\w+)\s*\(',  # JavaScript
            r'(\w+)\s*\([^)]*\)\s*{',  # C/C++/Java/C#
        ]
        
        for pattern in function_patterns:
            matches = re.finditer(pattern, content, re.MULTILINE)
            for match in matches:
                # Check if function needs compliance review
                func_name = match.group(1) if match.groups() else "unknown"
                if any(keyword in func_name.lower() for keyword in ["auth", "login", "password", "data", "user"]):
                    violations.append({
                        "rule_id": rule["rule_id"],
                        "file_path": str(file_path),
                        "function_name": func_name,
                        "category": rule["category"],
                        "severity": "MEDIUM",
                        "description": f"Function '{func_name}' may require compliance review",
                        "suggestion": "Review function for compliance with security/privacy requirements"
                    })
        
        return violations
    
    def _analyze_imports(self, content: str, file_path: Path, rule: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze import statements for compliance"""
        violations = []
        
        # Look for potentially problematic imports
        risky_imports = [
            "subprocess", "os.system", "eval", "exec",  # Python security risks
            "crypto", "hashlib", "ssl",  # Crypto libraries (may need review)
            "requests", "urllib",  # Network libraries
            "sqlite3", "mysql", "postgresql"  # Database libraries
        ]
        
        import_patterns = [
            r'import\s+(\w+)',
            r'from\s+(\w+)\s+import',
            r'require\([\'"](\w+)[\'"]\)',  # Node.js
        ]
        
        for pattern in import_patterns:
            matches = re.finditer(pattern, content)
            for match in matches:
                imported_module = match.group(1)
                if any(risky in imported_module.lower() for risky in risky_imports):
                    violations.append({
                        "rule_id": rule["rule_id"],
                        "file_path": str(file_path),
                        "imported_module": imported_module,
                        "category": "security",
                        "severity": "LOW",
                        "description": f"Import '{imported_module}' may require security review",
                        "suggestion": "Ensure secure usage of imported module"
                    })
        
        return violations
    
    def _calculate_scan_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate summary statistics for scan results"""
        violations = results.get("violations", [])
        
        # Count by severity
        severity_counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
        for violation in violations:
            severity = violation.get("severity", "LOW")
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        
        # Count by category
        category_counts = {}
        for violation in violations:
            category = violation.get("category", "unknown")
            category_counts[category] = category_counts.get(category, 0) + 1
        
        # Files with violations
        files_with_violations = len(set(v.get("file_path") for v in violations))
        total_files_scanned = len(results.get("scanned_files", []))
        
        return {
            "total_violations": len(violations),
            "severity_breakdown": severity_counts,
            "category_breakdown": category_counts,
            "files_with_violations": files_with_violations,
            "total_files_scanned": total_files_scanned,
            "violation_rate": files_with_violations / max(total_files_scanned, 1)
        }
    
    def _calculate_compliance_score(self, results: Dict[str, Any]) -> float:
        """Calculate overall compliance score (0-1)"""
        violations = results.get("violations", [])
        total_files = len(results.get("scanned_files", []))
        
        if total_files == 0:
            return 0.0
        
        # Weight violations by severity
        severity_weights = {"HIGH": 3, "MEDIUM": 2, "LOW": 1}
        weighted_violations = sum(
            severity_weights.get(v.get("severity", "LOW"), 1) 
            for v in violations
        )
        
        # Calculate score (higher violations = lower score)
        max_possible_violations = total_files * 10  # Assume max 10 violations per file
        compliance_score = max(0.0, 1.0 - (weighted_violations / max_possible_violations))
        
        return round(compliance_score, 3)
    
    def get_scan_report(self, results: Dict[str, Any]) -> str:
        """Generate human-readable scan report"""
        report = []
        
        report.append("=" * 60)
        report.append("COMPLIANCE SCAN REPORT")
        report.append("=" * 60)
        
        # Summary
        summary = results.get("scan_summary", {})
        report.append(f"Repository: {results.get('repository_path', 'Unknown')}")
        report.append(f"Scan Date: {results.get('scan_timestamp', 'Unknown')}")
        report.append(f"Compliance Score: {results.get('compliance_score', 0.0):.1%}")
        report.append(f"Total Violations: {summary.get('total_violations', 0)}")
        report.append(f"Files Scanned: {summary.get('total_files_scanned', 0)}")
        report.append("")
        
        # Severity breakdown
        severity_breakdown = summary.get("severity_breakdown", {})
        report.append("VIOLATIONS BY SEVERITY:")
        for severity in ["HIGH", "MEDIUM", "LOW"]:
            count = severity_breakdown.get(severity, 0)
            report.append(f"  {severity}: {count}")
        report.append("")
        
        # Category breakdown
        category_breakdown = summary.get("category_breakdown", {})
        if category_breakdown:
            report.append("VIOLATIONS BY CATEGORY:")
            for category, count in category_breakdown.items():
                report.append(f"  {category}: {count}")
            report.append("")
        
        # Top violations
        violations = results.get("violations", [])
        high_violations = [v for v in violations if v.get("severity") == "HIGH"]
        
        if high_violations:
            report.append("HIGH SEVERITY VIOLATIONS:")
            for violation in high_violations[:10]:  # Top 10
                report.append(f"  File: {violation.get('file_path', 'Unknown')}")
                report.append(f"  Line: {violation.get('line_number', 'Unknown')}")
                report.append(f"  Issue: {violation.get('description', 'Unknown')}")
                report.append(f"  Suggestion: {violation.get('suggestion', 'Review required')}")
                report.append("")
        
        report.append("=" * 60)
        
        return "\n".join(report)
    
    async def scan_repository_async(self, repo_path: str, file_extensions: List[str] = None) -> Dict[str, Any]:
        """Async version of repository scanning"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.scan_repository, repo_path, file_extensions)