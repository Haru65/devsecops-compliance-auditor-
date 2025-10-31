from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from typing import Optional, List, Dict, Any
import uvicorn
import logging
import traceback
import sys
from pathlib import Path
from utils.git_utils import git_clone, analyze_repository_files

# Add AI engine to path
current_dir = Path(__file__).parent
ai_engine_path = current_dir / "ai engine"
sys.path.append(str(ai_engine_path))

# Try to import AI components
try:
    from compliance_analyzer import ComplianceAnalyzer
    # Initialize a lightweight analyzer for demonstration
    _global_analyzer = None
    AI_ENABLED = True
    print("✓ AI Engine available")
except ImportError as e:
    AI_ENABLED = False
    _global_analyzer = None
    print(f"⚠ AI Engine not available: {e}")
    print("  Falling back to basic analysis")

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Compliance Auditor API",
    description="A backend service for auditing Git repositories for compliance issues",
    version="1.0.0"
)

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://devsecops-compliance-auditor.vercel.app",
        "http://localhost:3000",
    ],  # Whitelist frontend origins (add more as needed)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response validation
class GitRepoRequest(BaseModel):
    git_repo_url: str
    branch: Optional[str] = "main"
    analysis_depth: Optional[str] = "basic"  # basic, detailed, full
    use_ai: Optional[bool] = True  # Enable AI-powered analysis

class ComplianceIssue(BaseModel):
    file: str
    issue: str
    severity: str
    line: Optional[int] = None
    description: Optional[str] = None
    ai_confidence: Optional[float] = None  # AI confidence score

class ScanResponse(BaseModel):
    status: str
    repo: str
    message: str
    clone_path: Optional[str] = None
    repo_info: Optional[Dict[str, Any]] = None
    files: Optional[List[str]] = None
    total_files: Optional[int] = None
    compliance_issues: Optional[List[Dict[str, Any]]] = None
    issues_count: Optional[int] = None
    scan_duration: Optional[float] = None
    error_details: Optional[str] = None
    ai_enabled: Optional[bool] = None  # Whether AI analysis was used
    analysis_summary: Optional[Dict[str, Any]] = None  # AI-generated summary

# Root endpoint
@app.get("/")
def read_root():
    return {
        "message": "Compliance Auditor API",
        "version": "1.0.0",
        "ai_enabled": AI_ENABLED,
        "endpoints": {
            "/git-scan": "GET - Scan a Git repository by URL",
            "/git-scan-detailed": "POST - Detailed repository scan with options",
            "/ai-scan": "POST - AI-powered repository analysis",
            "/health": "GET - Health check",
            "/docs": "GET - API documentation"
        }
    }

# Health check endpoint
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "compliance-auditor-backend",
        "version": "1.0.0",
        "ai_enabled": AI_ENABLED,
        "ai_components": {
            "legal_bert": AI_ENABLED,
            "spacy": AI_ENABLED,
            "policy_processor": AI_ENABLED,
            "repository_scanner": AI_ENABLED
        }
    }

def get_analyzer():
    """Get or create a lightweight analyzer instance"""
    global _global_analyzer
    if _global_analyzer is None and AI_ENABLED:
        try:
            # Initialize with lightweight settings
            _global_analyzer = ComplianceAnalyzer(
                use_legal_bert=False,  # Disable heavy models for demo
                use_spacy=True
            )
        except Exception as e:
            logger.error(f"Failed to initialize AI analyzer: {e}")
            _global_analyzer = None
    return _global_analyzer

# AI-powered repository scan endpoint
@app.post("/ai-scan", response_model=ScanResponse)
def ai_scan_repository(request: GitRepoRequest):
    """
    Perform AI-powered compliance analysis of a Git repository.
    
    Args:
        request: GitRepoRequest containing repository URL and analysis options
        
    Returns:
        ScanResponse: AI-enhanced compliance analysis results
    """
    logger.info(f"Received AI scan request for: {request.git_repo_url}")
    
    try:
        import time
        start_time = time.time()
        
        # Validate URL format
        if not request.git_repo_url.startswith(('http://', 'https://', 'git@')):
            logger.warning(f"Invalid URL format: {request.git_repo_url}")
            raise HTTPException(
                status_code=400, 
                detail="Invalid git URL format. Must start with http://, https://, or git@"
            )
        
        logger.info("Starting repository clone...")
        # Clone repository
        result = git_clone(request.git_repo_url)
        logger.info(f"Clone result status: {result.get('status', 'unknown')}")
        
        if result["status"] == "error":
            logger.error(f"Clone failed: {result['message']}")
            raise HTTPException(status_code=400, detail=result["message"])
        
        result["ai_enabled"] = AI_ENABLED
        
        # Perform analysis
        if result["status"] == "success" and "clone_path" in result:
            logger.info("Starting compliance analysis...")
            
            if AI_ENABLED and request.use_ai:
                try:
                    # Use AI-powered analysis
                    logger.info("Using AI-powered analysis...")
                    analyzer = get_analyzer()
                    
                    if analyzer is not None:
                        # Perform repository scanning
                        ai_results = analyzer.scan_repository(
                            result["clone_path"], 
                            file_extensions=['.py', '.js', '.java', '.cpp', '.c', '.php', '.rb', '.go', '.rs', '.ts', '.jsx', '.tsx']
                        )
                        
                        if ai_results.get("status") == "success":
                            result["compliance_issues"] = ai_results.get("compliance_issues", [])
                            result["issues_count"] = len([issue for issue in result["compliance_issues"] if "error" not in issue])
                            result["analysis_summary"] = ai_results.get("summary", {})
                            logger.info(f"AI analysis found {result['issues_count']} compliance issues")
                        else:
                            logger.warning("AI analysis failed, falling back to basic analysis")
                            # Fallback to basic analysis
                            compliance_issues = analyze_repository_files(result["clone_path"], analysis_depth=request.analysis_depth)
                            result["compliance_issues"] = compliance_issues
                            result["issues_count"] = len([issue for issue in compliance_issues if "error" not in issue])
                    else:
                        logger.warning("AI analyzer not available, falling back to basic analysis")
                        # Fallback to basic analysis
                        compliance_issues = analyze_repository_files(result["clone_path"], analysis_depth=request.analysis_depth)
                        result["compliance_issues"] = compliance_issues
                        result["issues_count"] = len([issue for issue in compliance_issues if "error" not in issue])
                        
                except Exception as ai_error:
                    logger.error(f"AI analysis failed: {ai_error}")
                    # Fallback to basic analysis
                    compliance_issues = analyze_repository_files(result["clone_path"], analysis_depth=request.analysis_depth)
                    result["compliance_issues"] = compliance_issues
                    result["issues_count"] = len([issue for issue in compliance_issues if "error" not in issue])
                    result["error_details"] = f"AI analysis failed, used fallback: {str(ai_error)}"
            else:
                # Use basic analysis
                logger.info("Using basic analysis...")
                compliance_issues = analyze_repository_files(result["clone_path"], analysis_depth=request.analysis_depth)
                result["compliance_issues"] = compliance_issues
                result["issues_count"] = len([issue for issue in compliance_issues if "error" not in issue])
        
        # Add scan duration
        end_time = time.time()
        result["scan_duration"] = round(end_time - start_time, 2)
        
        logger.info("AI scan completed successfully")
        return ScanResponse(**result)
        
    except HTTPException:
        logger.error("HTTPException raised")
        raise
    except Exception as e:
        error_msg = f"Internal server error: {str(e)}"
        error_traceback = traceback.format_exc()
        logger.error(f"Unexpected error: {error_msg}")
        logger.error(f"Traceback: {error_traceback}")
        
        # Return detailed error for debugging
        return {
            "status": "error",
            "message": error_msg,
            "error_details": error_traceback,
            "repo": request.git_repo_url,
            "ai_enabled": AI_ENABLED
        }

# Simple git scan endpoint (GET with query parameter)
@app.get("/git-scan", response_model=ScanResponse)
def scan_git_repo(git_repo_url: str):
    """
    Scan a Git repository for compliance issues.
    
    Args:
        git_repo_url: The URL of the Git repository to scan
        
    Returns:
        ScanResponse: Results of the compliance scan
    """
    logger.info(f"Received scan request for: {git_repo_url}")
    
    try:
        # Validate URL format
        if not git_repo_url.startswith(('http://', 'https://', 'git@')):
            logger.warning(f"Invalid URL format: {git_repo_url}")
            raise HTTPException(
                status_code=400, 
                detail="Invalid git URL format. Must start with http://, https://, or git@"
            )
        
        logger.info("Starting repository clone...")
        # Clone and get basic info
        result = git_clone(git_repo_url)
        logger.info(f"Clone result status: {result.get('status', 'unknown')}")
        
        if result["status"] == "error":
            logger.error(f"Clone failed: {result['message']}")
            raise HTTPException(status_code=400, detail=result["message"])
        
        # Analyze for compliance issues
        if result["status"] == "success" and "clone_path" in result:
            logger.info("Starting compliance analysis...")
            try:
                # Use basic analysis for simple scan endpoint
                compliance_issues = analyze_repository_files(result["clone_path"], analysis_depth="basic")
                result["compliance_issues"] = compliance_issues
                result["issues_count"] = len([issue for issue in compliance_issues if "error" not in issue])
                logger.info(f"Found {result['issues_count']} compliance issues")
            except Exception as analysis_error:
                logger.error(f"Analysis failed: {analysis_error}")
                result["compliance_issues"] = []
                result["issues_count"] = 0
                result["error_details"] = f"Analysis failed: {str(analysis_error)}"
        
        logger.info("Scan completed successfully")
        return ScanResponse(**result)
        
    except HTTPException:
        logger.error("HTTPException raised")
        raise
    except Exception as e:
        error_msg = f"Internal server error: {str(e)}"
        error_traceback = traceback.format_exc()
        logger.error(f"Unexpected error: {error_msg}")
        logger.error(f"Traceback: {error_traceback}")
        
        # Return detailed error for debugging
        return {
            "status": "error",
            "message": error_msg,
            "error_details": error_traceback,
            "repo": git_repo_url
        }

# Detailed git scan endpoint (POST with request body)
@app.post("/git-scan-detailed", response_model=ScanResponse)
def scan_git_repo_detailed(request: GitRepoRequest):
    """
    Perform a detailed scan of a Git repository with additional options.
    
    Args:
        request: GitRepoRequest containing repository URL and scan options
        
    Returns:
        ScanResponse: Detailed results of the compliance scan
    """
    try:
        import time
        start_time = time.time()
        
        # Clone and get basic info
        result = git_clone(request.git_repo_url)
        
        if result["status"] == "error":
            raise HTTPException(status_code=400, detail=result["message"])
        
        # Analyze for compliance issues based on analysis depth
        if result["status"] == "success" and "clone_path" in result:
            compliance_issues = analyze_repository_files(
                result["clone_path"], 
                analysis_depth=request.analysis_depth
            )
            result["compliance_issues"] = compliance_issues
            result["issues_count"] = len([issue for issue in compliance_issues if "error" not in issue])
        
        # Add scan duration
        end_time = time.time()
        result["scan_duration"] = round(end_time - start_time, 2)
        
        return ScanResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# Get scan history (placeholder for future implementation)
@app.get("/scan-history")
def get_scan_history(limit: int = 10):
    """
    Get the history of previous scans.
    
    Args:
        limit: Number of recent scans to return
        
    Returns:
        List of recent scan results
    """
    return {
        "message": "Scan history feature coming soon",
        "limit": limit,
        "history": []
    }

# Get compliance rules (placeholder for future implementation)
@app.get("/compliance-rules")
def get_compliance_rules():
    """
    Get the list of compliance rules being checked.
    
    Returns:
        List of compliance rules and their descriptions
    """
    return {
        "rules": [
            {
                "id": "hardcoded-secrets",
                "name": "Hardcoded Secrets Detection",
                "description": "Detects potential hardcoded passwords, API keys, and secrets"
            },
            {
                "id": "license-compliance",
                "name": "License Compliance",
                "description": "Checks for proper license files and headers"
            },
            {
                "id": "security-vulnerabilities",
                "name": "Security Vulnerabilities",
                "description": "Scans for known security vulnerabilities in dependencies"
            }
        ]
    }

# Exception handlers
@app.exception_handler(404)
def not_found_handler(request, exc):
    return {
        "status": "error",
        "message": "Endpoint not found",
        "available_endpoints": [
            "/",
            "/health",
            "/git-scan",
            "/git-scan-detailed",
            "/scan-history",
            "/compliance-rules",
            "/docs"
        ]
    }

@app.exception_handler(500)
def internal_error_handler(request, exc):
    return {
        "status": "error",
        "message": "Internal server error",
        "detail": "Please try again later or contact support"
    }

# Run the application
if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8001,  # Changed to port 8001
        reload=True,
        log_level="info"
    )