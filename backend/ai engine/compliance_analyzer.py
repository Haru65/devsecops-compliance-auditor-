"""
Compliance Analyzer - Main AI Engine Component
Combines Legal-BERT and spaCy for comprehensive compliance analysis
Now includes Policy Processing and Repository Scanning capabilities
"""

import logging
from typing import Dict, List, Any, Optional
import asyncio
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class ComplianceAnalyzer:
    """
    Main compliance analyzer that combines Legal-BERT, spaCy, Policy Processing and Repository Scanning
    """
    
    def __init__(self, use_legal_bert: bool = True, use_spacy: bool = True, policies_dir: str = "policies"):
        """
        Initialize compliance analyzer
        
        Args:
            use_legal_bert: Whether to use Legal-BERT pipeline
            use_spacy: Whether to use spaCy pipeline
            policies_dir: Directory for policy documents
        """
        self.use_legal_bert = use_legal_bert
        self.use_spacy = use_spacy
        self.policies_dir = policies_dir
        
        # Initialize pipelines
        self.legal_bert_pipeline = None
        self.entity_extractor = None
        self.policy_processor = None
        self.repository_scanner = None
        
        self._initialize_pipelines()
    
    def _initialize_pipelines(self):
        """Initialize AI pipelines"""
        try:
            if self.use_legal_bert:
                logger.info("Initializing Legal-BERT pipeline...")
                try:
                    try:
                        from .legal_bert_pipeline import LegalBERTPipeline
                    except ImportError:
                        from legal_bert_pipeline import LegalBERTPipeline
                    self.legal_bert_pipeline = LegalBERTPipeline()
                    logger.info("Legal-BERT pipeline initialized successfully")
                except Exception as e:
                    logger.warning(f"Failed to initialize Legal-BERT: {e}")
                    self.use_legal_bert = False
            
            if self.use_spacy:
                logger.info("Initializing spaCy entity extractor...")
                try:
                    try:
                        from .entity_extractor import LegalEntityExtractor
                    except ImportError:
                        from entity_extractor import LegalEntityExtractor
                    self.entity_extractor = LegalEntityExtractor()
                    logger.info("spaCy entity extractor initialized successfully")
                except Exception as e:
                    logger.warning(f"Failed to initialize spaCy: {e}")
                    self.use_spacy = False
            
            # Initialize Policy Processor
            logger.info("Initializing Policy Processor...")
            try:
                try:
                    from .policy_processor import PolicyProcessor
                except ImportError:
                    from policy_processor import PolicyProcessor
                self.policy_processor = PolicyProcessor(self.policies_dir)
                logger.info("Policy processor initialized successfully")
            except Exception as e:
                logger.warning(f"Failed to initialize Policy Processor: {e}")
                self.policy_processor = None
            
            # Initialize Repository Scanner
            logger.info("Initializing Repository Scanner...")
            try:
                try:
                    from .repository_scanner import RepositoryScanner
                except ImportError:
                    from repository_scanner import RepositoryScanner
                self.repository_scanner = RepositoryScanner(self.policy_processor)
                logger.info("Repository scanner initialized successfully")
            except Exception as e:
                logger.warning(f"Failed to initialize Repository Scanner: {e}")
                self.repository_scanner = None
            
            if not self.use_legal_bert and not self.use_spacy:
                logger.warning("No AI pipelines available, falling back to rule-based analysis")
                
        except Exception as e:
            logger.error(f"Pipeline initialization failed: {e}")
            raise
    
    def analyze_text(self, text: str, analysis_type: str = "comprehensive") -> Dict[str, Any]:
        """
        Analyze text for compliance issues using available AI pipelines
        
        Args:
            text: Input text to analyze
            analysis_type: Type of analysis ("comprehensive", "quick", "entities_only", "classification_only")
            
        Returns:
            Comprehensive analysis results
        """
        analysis_start = datetime.now()
        
        try:
            results = {
                "text_length": len(text),
                "analysis_type": analysis_type,
                "timestamp": analysis_start.isoformat(),
                "pipelines_used": [],
                "legal_bert_results": {},
                "spacy_results": {},
                "combined_analysis": {},
                "compliance_score": 0.0,
                "risk_assessment": {},
                "recommendations": []
            }
            
            # Legal-BERT Analysis
            if self.use_legal_bert and analysis_type in ["comprehensive", "classification_only"]:
                try:
                    logger.info("Running Legal-BERT analysis...")
                    bert_results = self.legal_bert_pipeline.analyze_compliance_obligations(text)
                    results["legal_bert_results"] = bert_results
                    results["pipelines_used"].append("legal-bert")
                    logger.info("Legal-BERT analysis completed")
                except Exception as e:
                    logger.error(f"Legal-BERT analysis failed: {e}")
                    results["legal_bert_results"] = {"error": str(e)}
            
            # spaCy Analysis
            if self.use_spacy and analysis_type in ["comprehensive", "entities_only"]:
                try:
                    logger.info("Running spaCy entity extraction...")
                    spacy_results = self.entity_extractor.extract_entities(text)
                    results["spacy_results"] = spacy_results
                    results["pipelines_used"].append("spacy")
                    logger.info("spaCy analysis completed")
                except Exception as e:
                    logger.error(f"spaCy analysis failed: {e}")
                    results["spacy_results"] = {"error": str(e)}
            
            # Combined Analysis
            if analysis_type == "comprehensive":
                results["combined_analysis"] = self._combine_analyses(
                    results["legal_bert_results"],
                    results["spacy_results"]
                )
                
                results["compliance_score"] = self._calculate_overall_compliance_score(results)
                results["risk_assessment"] = self._assess_overall_risk(results)
                results["recommendations"] = self._generate_recommendations(results)
            
            # Quick analysis fallback
            elif analysis_type == "quick":
                results["combined_analysis"] = self._quick_rule_based_analysis(text)
                results["compliance_score"] = 0.5  # Default score for rule-based
            
            # Calculate analysis duration
            analysis_end = datetime.now()
            results["analysis_duration"] = (analysis_end - analysis_start).total_seconds()
            
            return results
            
        except Exception as e:
            logger.error(f"Text analysis failed: {e}")
            return {
                "error": str(e),
                "text_length": len(text),
                "analysis_type": analysis_type,
                "timestamp": analysis_start.isoformat(),
                "pipelines_used": [],
                "analysis_duration": (datetime.now() - analysis_start).total_seconds()
            }
    
    def _combine_analyses(self, bert_results: Dict, spacy_results: Dict) -> Dict[str, Any]:
        """Combine results from both pipelines"""
        try:
            combined = {
                "entities": {
                    "legal_bert": bert_results.get("entities", []),
                    "spacy": spacy_results.get("entities", []),
                    "combined": self._merge_entities(
                        bert_results.get("entities", []),
                        spacy_results.get("entities", [])
                    )
                },
                "compliance_obligations": bert_results.get("compliance_analysis", {}).get("obligations", []),
                "legal_patterns": spacy_results.get("legal_patterns", {}),
                "privacy_entities": spacy_results.get("compliance_entities", []),
                "document_structure": spacy_results.get("legal_analysis", {}),
                "classification": bert_results.get("classification", {})
            }
            
            return combined
            
        except Exception as e:
            logger.error(f"Analysis combination failed: {e}")
            return {"error": str(e)}
    
    def _merge_entities(self, bert_entities: List[Dict], spacy_entities: List[Dict]) -> List[Dict]:
        """Merge entities from both pipelines, removing duplicates"""
        merged = []
        seen_entities = set()
        
        # Add BERT entities
        for entity in bert_entities:
            entity_key = (entity.get("text", "").lower(), entity.get("label", ""))
            if entity_key not in seen_entities:
                entity["source"] = "legal-bert"
                merged.append(entity)
                seen_entities.add(entity_key)
        
        # Add spaCy entities (avoid duplicates)
        for entity in spacy_entities:
            entity_key = (entity.get("text", "").lower(), entity.get("label", ""))
            if entity_key not in seen_entities:
                entity["source"] = "spacy"
                merged.append(entity)
                seen_entities.add(entity_key)
        
        return merged
    
    def _calculate_overall_compliance_score(self, results: Dict) -> float:
        """Calculate overall compliance score"""
        try:
            scores = []
            
            # BERT compliance score
            bert_score = results.get("legal_bert_results", {}).get("compliance_analysis", {}).get("compliance_score", 0.0)
            if bert_score > 0:
                scores.append(bert_score)
            
            # spaCy completeness score
            spacy_score = results.get("spacy_results", {}).get("legal_analysis", {}).get("completeness_score", 0.0)
            if spacy_score > 0:
                scores.append(spacy_score)
            
            # Entity diversity score
            entity_count = len(results.get("combined_analysis", {}).get("entities", {}).get("combined", []))
            entity_score = min(entity_count / 10.0, 1.0)  # Normalize to 0-1
            scores.append(entity_score)
            
            return sum(scores) / len(scores) if scores else 0.0
            
        except Exception as e:
            logger.error(f"Compliance score calculation failed: {e}")
            return 0.0
    
    def _assess_overall_risk(self, results: Dict) -> Dict[str, Any]:
        """Assess overall compliance risk"""
        try:
            risk_factors = []
            
            # Privacy entities risk
            privacy_entities = results.get("spacy_results", {}).get("compliance_entities", [])
            high_risk_count = len([e for e in privacy_entities if e.get("privacy_risk") == "HIGH"])
            
            if high_risk_count > 0:
                risk_factors.append({
                    "factor": "high_risk_privacy_data",
                    "count": high_risk_count,
                    "severity": "HIGH"
                })
            
            # BERT risk assessment
            bert_risk = results.get("legal_bert_results", {}).get("compliance_analysis", {}).get("risk_level", "LOW")
            if bert_risk in ["HIGH", "MEDIUM"]:
                risk_factors.append({
                    "factor": "legal_complexity",
                    "level": bert_risk,
                    "severity": bert_risk
                })
            
            # Obligations count
            obligations = results.get("combined_analysis", {}).get("compliance_obligations", [])
            if len(obligations) > 5:
                risk_factors.append({
                    "factor": "high_obligation_count",
                    "count": len(obligations),
                    "severity": "MEDIUM"
                })
            
            # Overall risk level
            high_severity_count = len([rf for rf in risk_factors if rf.get("severity") == "HIGH"])
            medium_severity_count = len([rf for rf in risk_factors if rf.get("severity") == "MEDIUM"])
            
            if high_severity_count > 0:
                overall_risk = "HIGH"
            elif medium_severity_count > 1:
                overall_risk = "HIGH"
            elif medium_severity_count > 0:
                overall_risk = "MEDIUM"
            else:
                overall_risk = "LOW"
            
            return {
                "overall_risk": overall_risk,
                "risk_factors": risk_factors,
                "risk_score": len(risk_factors) / 10.0  # Normalize
            }
            
        except Exception as e:
            logger.error(f"Risk assessment failed: {e}")
            return {"overall_risk": "UNKNOWN", "error": str(e)}
    
    def _generate_recommendations(self, results: Dict) -> List[Dict[str, str]]:
        """Generate compliance recommendations"""
        recommendations = []
        
        try:
            # Privacy data recommendations
            privacy_entities = results.get("spacy_results", {}).get("compliance_entities", [])
            high_risk_entities = [e for e in privacy_entities if e.get("privacy_risk") == "HIGH"]
            
            if high_risk_entities:
                recommendations.append({
                    "category": "data_protection",
                    "priority": "HIGH",
                    "recommendation": f"Implement proper data protection measures for {len(high_risk_entities)} high-risk data elements detected",
                    "details": "Consider encryption, access controls, and data minimization practices"
                })
            
            # Legal obligations recommendations
            obligations = results.get("combined_analysis", {}).get("compliance_obligations", [])
            if len(obligations) > 3:
                recommendations.append({
                    "category": "compliance_tracking",
                    "priority": "MEDIUM",
                    "recommendation": f"Establish tracking system for {len(obligations)} compliance obligations",
                    "details": "Implement regular compliance audits and monitoring procedures"
                })
            
            # Document completeness
            completeness_score = results.get("spacy_results", {}).get("legal_analysis", {}).get("completeness_score", 0.0)
            if completeness_score < 0.7:
                recommendations.append({
                    "category": "documentation",
                    "priority": "MEDIUM",
                    "recommendation": "Improve document completeness and legal coverage",
                    "details": f"Current completeness score: {completeness_score:.2f}. Consider adding missing legal sections"
                })
            
            # Classification confidence
            classification_confidence = results.get("legal_bert_results", {}).get("classification", {}).get("confidence", 0.0)
            if classification_confidence < 0.6:
                recommendations.append({
                    "category": "legal_review",
                    "priority": "LOW",
                    "recommendation": "Consider professional legal review",
                    "details": f"AI classification confidence is low ({classification_confidence:.2f})"
                })
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Recommendation generation failed: {e}")
            return [{"category": "error", "priority": "LOW", "recommendation": f"Error generating recommendations: {str(e)}"}]
    
    def _quick_rule_based_analysis(self, text: str) -> Dict[str, Any]:
        """Fallback rule-based analysis when AI pipelines are unavailable"""
        text_lower = text.lower()
        
        # Simple keyword-based analysis
        compliance_keywords = {
            "privacy": ["privacy", "personal data", "personal information", "pii"],
            "security": ["security", "encryption", "password", "authentication"],
            "liability": ["liability", "damages", "indemnification", "limitation"],
            "termination": ["termination", "cancellation", "expiry", "end"],
            "governing_law": ["governing law", "jurisdiction", "applicable law"]
        }
        
        found_categories = {}
        for category, keywords in compliance_keywords.items():
            count = sum(1 for keyword in keywords if keyword in text_lower)
            found_categories[category] = count > 0
        
        return {
            "rule_based_analysis": True,
            "categories_detected": found_categories,
            "total_categories": sum(1 for present in found_categories.values() if present),
            "analysis_method": "keyword_matching"
        }
    
    async def analyze_text_async(self, text: str, analysis_type: str = "comprehensive") -> Dict[str, Any]:
        """Async version of text analysis"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.analyze_text, text, analysis_type)
    
    def get_pipeline_status(self) -> Dict[str, Any]:
        """Get status of AI pipelines"""
        return {
            "legal_bert_available": self.use_legal_bert and self.legal_bert_pipeline is not None,
            "spacy_available": self.use_spacy and self.entity_extractor is not None,
            "policy_processor_available": self.policy_processor is not None,
            "repository_scanner_available": self.repository_scanner is not None,
            "pipelines_loaded": [
                name for name, available in [
                    ("legal-bert", self.use_legal_bert and self.legal_bert_pipeline is not None),
                    ("spacy", self.use_spacy and self.entity_extractor is not None),
                    ("policy-processor", self.policy_processor is not None),
                    ("repository-scanner", self.repository_scanner is not None)
                ] if available
            ]
        }
    
    # New Policy Management Methods
    
    def import_policies(self, policies_folder_path: str) -> Dict[str, Any]:
        """
        Import legal policies from a folder and convert them to compliance rules
        
        Args:
            policies_folder_path: Path to folder containing policy documents
            
        Returns:
            Import results with processing status
        """
        if not self.policy_processor:
            logger.error("Policy processor not available")
            return {"error": "Policy processor not initialized"}
        
        try:
            logger.info(f"Importing policies from {policies_folder_path}")
            results = self.policy_processor.import_policy_folder(policies_folder_path)
            
            # Reload scanner with new rules
            if self.repository_scanner:
                self.repository_scanner._load_compliance_rules()
            
            logger.info(f"Policy import completed: {results.get('processed_count', 0)} policies processed")
            return results
            
        except Exception as e:
            logger.error(f"Policy import failed: {e}")
            return {"error": str(e)}
    
    def get_compliance_rules(self) -> Dict[str, Any]:
        """Get all compliance rules generated from policies"""
        if not self.policy_processor:
            return {"error": "Policy processor not available"}
        
        return self.policy_processor.get_compliance_rules_for_scanning()
    
    def get_policy_summary(self) -> Dict[str, Any]:
        """Get summary of all processed policies"""
        if not self.policy_processor:
            return {"error": "Policy processor not available"}
        
        return self.policy_processor.get_policy_summary()
    
    def process_single_policy(self, policy_content: str, policy_id: str = None) -> Dict[str, Any]:
        """
        Process a single policy document
        
        Args:
            policy_content: The policy text content
            policy_id: Optional policy identifier
            
        Returns:
            Processing results
        """
        if not self.policy_processor:
            return {"error": "Policy processor not available"}
        
        if not policy_id:
            policy_id = f"manual_policy_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        try:
            result = self.policy_processor.process_policy(
                policy_id=policy_id,
                content=policy_content
            )
            
            # Reload scanner with new rules
            if self.repository_scanner:
                self.repository_scanner._load_compliance_rules()
            
            return result
            
        except Exception as e:
            logger.error(f"Single policy processing failed: {e}")
            return {"error": str(e)}
    
    # New Repository Scanning Methods
    
    def scan_repository(self, repo_path: str, file_extensions: List[str] = None) -> Dict[str, Any]:
        """
        Scan repository for compliance violations using AI-generated rules
        
        Args:
            repo_path: Path to repository to scan
            file_extensions: File extensions to scan (optional)
            
        Returns:
            Comprehensive scan results
        """
        if not self.repository_scanner:
            logger.error("Repository scanner not available")
            return {"error": "Repository scanner not initialized"}
        
        try:
            logger.info(f"Scanning repository: {repo_path}")
            results = self.repository_scanner.scan_repository(repo_path, file_extensions)
            logger.info(f"Repository scan completed with {results.get('scan_summary', {}).get('total_violations', 0)} violations")
            return results
            
        except Exception as e:
            logger.error(f"Repository scan failed: {e}")
            return {"error": str(e)}
    
    def generate_scan_report(self, scan_results: Dict[str, Any]) -> str:
        """
        Generate human-readable compliance scan report
        
        Args:
            scan_results: Results from repository scan
            
        Returns:
            Formatted report string
        """
        if not self.repository_scanner:
            return "Repository scanner not available"
        
        return self.repository_scanner.get_scan_report(scan_results)
    
    async def scan_repository_async(self, repo_path: str, file_extensions: List[str] = None) -> Dict[str, Any]:
        """Async version of repository scanning"""
        if not self.repository_scanner:
            return {"error": "Repository scanner not initialized"}
        
        return await self.repository_scanner.scan_repository_async(repo_path, file_extensions)
    
    # Enhanced Analysis Methods
    
    def comprehensive_compliance_analysis(self, repo_path: str, policies_folder: str = None) -> Dict[str, Any]:
        """
        Perform comprehensive compliance analysis including policy import and repository scanning
        
        Args:
            repo_path: Path to repository to analyze
            policies_folder: Optional path to policies folder
            
        Returns:
            Complete compliance analysis results
        """
        analysis_start = datetime.now()
        
        results = {
            "analysis_type": "comprehensive_compliance",
            "repository_path": repo_path,
            "timestamp": analysis_start.isoformat(),
            "policy_import": {},
            "repository_scan": {},
            "compliance_summary": {},
            "recommendations": [],
            "analysis_duration": 0
        }
        
        try:
            # Import policies if folder provided
            if policies_folder:
                logger.info("Importing policies...")
                results["policy_import"] = self.import_policies(policies_folder)
            
            # Scan repository
            logger.info("Scanning repository...")
            results["repository_scan"] = self.scan_repository(repo_path)
            
            # Generate compliance summary
            results["compliance_summary"] = self._generate_compliance_summary(
                results["policy_import"],
                results["repository_scan"]
            )
            
            # Generate recommendations
            results["recommendations"] = self._generate_compliance_recommendations(
                results["repository_scan"]
            )
            
            # Calculate analysis duration
            analysis_end = datetime.now()
            results["analysis_duration"] = (analysis_end - analysis_start).total_seconds()
            
            logger.info(f"Comprehensive compliance analysis completed in {results['analysis_duration']:.2f}s")
            return results
            
        except Exception as e:
            logger.error(f"Comprehensive compliance analysis failed: {e}")
            results["error"] = str(e)
            results["analysis_duration"] = (datetime.now() - analysis_start).total_seconds()
            return results
    
    def _generate_compliance_summary(self, policy_import: Dict[str, Any], repository_scan: Dict[str, Any]) -> Dict[str, Any]:
        """Generate overall compliance summary"""
        try:
            scan_summary = repository_scan.get("scan_summary", {})
            
            return {
                "policies_processed": policy_import.get("processed_count", 0),
                "compliance_rules_generated": len(self.get_compliance_rules().get("rules", [])),
                "total_violations": scan_summary.get("total_violations", 0),
                "compliance_score": repository_scan.get("compliance_score", 0.0),
                "risk_level": self._determine_risk_level(scan_summary),
                "files_scanned": scan_summary.get("total_files_scanned", 0),
                "files_with_violations": scan_summary.get("files_with_violations", 0)
            }
            
        except Exception as e:
            logger.error(f"Compliance summary generation failed: {e}")
            return {"error": str(e)}
    
    def _determine_risk_level(self, scan_summary: Dict[str, Any]) -> str:
        """Determine overall risk level based on scan results"""
        severity_breakdown = scan_summary.get("severity_breakdown", {})
        high_violations = severity_breakdown.get("HIGH", 0)
        medium_violations = severity_breakdown.get("MEDIUM", 0)
        
        if high_violations > 5:
            return "CRITICAL"
        elif high_violations > 0 or medium_violations > 10:
            return "HIGH"
        elif medium_violations > 0:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _generate_compliance_recommendations(self, repository_scan: Dict[str, Any]) -> List[Dict[str, str]]:
        """Generate compliance recommendations based on scan results"""
        recommendations = []
        
        try:
            scan_summary = repository_scan.get("scan_summary", {})
            severity_breakdown = scan_summary.get("severity_breakdown", {})
            category_breakdown = scan_summary.get("category_breakdown", {})
            
            # High severity violations
            if severity_breakdown.get("HIGH", 0) > 0:
                recommendations.append({
                    "priority": "CRITICAL",
                    "category": "security",
                    "recommendation": f"Address {severity_breakdown['HIGH']} high-severity violations immediately",
                    "action": "Review and fix high-risk security and compliance issues"
                })
            
            # Category-specific recommendations
            for category, count in category_breakdown.items():
                if count > 5:
                    recommendations.append({
                        "priority": "HIGH",
                        "category": category,
                        "recommendation": f"Implement comprehensive {category} compliance measures",
                        "action": f"Review {count} violations in {category} category"
                    })
            
            # General recommendations
            compliance_score = repository_scan.get("compliance_score", 0.0)
            if compliance_score < 0.7:
                recommendations.append({
                    "priority": "MEDIUM",
                    "category": "general",
                    "recommendation": "Improve overall compliance posture",
                    "action": f"Current compliance score: {compliance_score:.1%}. Aim for >80%"
                })
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Recommendation generation failed: {e}")
            return [{"priority": "LOW", "category": "error", "recommendation": f"Error generating recommendations: {str(e)}"}]