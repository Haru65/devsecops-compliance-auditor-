# AI Compliance Auditor - Enhanced with Policy Processing

A powerful AI-driven compliance auditing system that can import legal policies, convert them to scannable rules using transformers, and scan code repositories for compliance violations.

## 🚀 New Features

### 1. **Policy Processing Engine**
- Import legal policies from folders (supports .txt, .md, .pdf, .doc, .docx)
- Convert policies to compliance rules using AI transformers
- Extract key requirements, categories, and enforcement actions
- Generate scannable patterns for code analysis

### 2. **Repository Scanner**
- Scan code repositories using AI-generated compliance rules
- Support multiple programming languages (Python, JavaScript, Java, C++, etc.)
- Pattern-based violation detection
- Function and import analysis
- Detailed compliance reporting

### 3. **Enhanced API Endpoints**
- `/policies/import` - Import policy documents
- `/policies/process` - Process individual policies
- `/policies/summary` - Get policy overview
- `/policies/rules` - Get generated compliance rules
- `/scan/repository` - Scan repositories with AI rules
- `/scan/comprehensive` - Complete compliance analysis

## 🛠️ Setup

### Quick Setup
```bash
chmod +x setup.sh
./setup.sh
```

### Manual Setup
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install PyTorch for transformers
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Download spaCy model
python3 -m spacy download en_core_web_sm

# Create directories
mkdir -p policies repos logs
```

## 📝 Usage

### 1. Import Legal Policies

```python
# Create your policies folder
mkdir -p /path/to/your/policies

# Add your policy documents (.txt, .md, .pdf, .doc, .docx)
# Example: data_protection_policy.md, security_policy.txt

# Use API to import
curl -X POST "http://localhost:8000/policies/import" \
  -H "Content-Type: application/json" \
  -d '{"policies_folder_path": "/path/to/your/policies"}'
```

### 2. Scan Repository for Compliance

```python
# Scan a repository
curl -X POST "http://localhost:8000/scan/repository" \
  -H "Content-Type: application/json" \
  -d '{"repository_path": "/path/to/your/repo"}'
```

### 3. Comprehensive Analysis

```python
# Import policies and scan repository in one step
curl -X POST "http://localhost:8000/scan/comprehensive" \
  -H "Content-Type: application/json" \
  -d '{
    "repository_path": "/path/to/your/repo",
    "policies_folder_path": "/path/to/your/policies"
  }'
```

### 4. Demo Script

```bash
# Run comprehensive demo
python3 demo_enhanced_ai.py
```

## 🔧 AI Components

### Policy Processor
- **Transformers**: Uses Hugging Face transformers for text analysis
- **Question-Answering**: Extracts specific requirements from policies
- **Summarization**: Condenses policy content
- **Classification**: Categorizes policies by type

### Repository Scanner
- **Pattern Matching**: Scans code for compliance violations
- **Multi-language Support**: Python, JavaScript, Java, C++, C#, PHP, Ruby, Go
- **Function Analysis**: Identifies functions needing compliance review
- **Import Analysis**: Checks for risky imports and dependencies

### Compliance Analyzer
- **Risk Assessment**: Calculates compliance scores and risk levels
- **Recommendation Engine**: Generates actionable compliance advice
- **Report Generation**: Creates detailed compliance reports

## 📊 Example Output

### Policy Import Results
```json
{
  "status": "success",
  "message": "Successfully imported 3 policies",
  "import_results": {
    "imported_count": 3,
    "processed_count": 3,
    "failed_count": 0,
    "policies": [...]
  },
  "compliance_rules_generated": 15
}
```

### Repository Scan Results
```json
{
  "status": "success",
  "scan_results": {
    "compliance_score": 0.75,
    "scan_summary": {
      "total_violations": 8,
      "severity_breakdown": {
        "HIGH": 2,
        "MEDIUM": 3,
        "LOW": 3
      },
      "total_files_scanned": 15
    },
    "violations": [
      {
        "rule_id": "security_001",
        "file_path": "app.py",
        "line_number": 23,
        "severity": "HIGH",
        "description": "Hardcoded password detected",
        "suggestion": "Use environment variables or secure credential management"
      }
    ]
  }
}
```

## 🎯 Use Cases

### 1. **GDPR Compliance**
- Import GDPR policies
- Scan for personal data handling
- Detect missing consent mechanisms
- Verify data protection measures

### 2. **Security Auditing**
- Import security policies
- Scan for hardcoded credentials
- Check encryption implementation
- Verify access controls

### 3. **Industry Standards**
- ISO 27001 compliance checking
- HIPAA privacy requirements
- PCI DSS security standards
- SOX financial controls

### 4. **Custom Policies**
- Import company-specific policies
- Generate custom compliance rules
- Scan for policy violations
- Track compliance metrics

## 🔍 Supported File Types

### Policy Documents
- **Text files**: .txt, .md
- **PDF files**: .pdf (requires PyPDF2)
- **Word documents**: .doc, .docx (requires python-docx)

### Code Files
- **Python**: .py
- **JavaScript/TypeScript**: .js, .ts
- **Java**: .java
- **C/C++**: .c, .cpp, .h
- **C#**: .cs
- **PHP**: .php
- **Ruby**: .rb
- **Go**: .go

## 🚨 Compliance Rules

The system generates various types of compliance rules:

### Security Rules
- Hardcoded credentials detection
- Weak encryption patterns
- Authentication bypasses
- SSL/TLS issues

### Data Protection Rules
- Personal data exposure
- Unencrypted data storage
- Missing consent mechanisms
- Data retention violations

### Audit Rules
- Missing logging mechanisms
- Insufficient audit trails
- Access control bypasses
- Change tracking issues

## 🔧 Configuration

### Environment Variables
```bash
# Optional: Configure AI models
export HUGGINGFACE_MODEL_PATH="/path/to/models"
export COMPLIANCE_RULES_PATH="/path/to/rules"

# Optional: Configure logging
export LOG_LEVEL="INFO"
export LOG_FILE="logs/compliance_auditor.log"
```

### Policy Directory Structure
```
policies/
├── data_protection/
│   ├── gdpr_policy.md
│   └── privacy_policy.txt
├── security/
│   ├── security_policy.txt
│   └── encryption_standards.md
└── compliance/
    ├── audit_policy.md
    └── reporting_requirements.txt
```

## 🧪 Testing

```bash
# Run basic tests
python3 -m pytest tests/

# Run integration tests
python3 test_ai_engine.py

# Run full demo
python3 demo_enhanced_ai.py
```

## 📈 Performance

- **Policy Processing**: ~2-5 seconds per policy document
- **Repository Scanning**: ~1-3 seconds per 100 files
- **Memory Usage**: ~500MB-2GB depending on model size
- **Supported Repository Size**: Up to 10,000 files

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your enhancements
4. Write tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
1. Check the API documentation at `/docs`
2. Run the demo script for examples
3. Review the log files in `logs/`
4. Create an issue in the repository

## 🔮 Future Enhancements

- [ ] Machine learning model training on custom policies
- [ ] Real-time compliance monitoring
- [ ] Integration with CI/CD pipelines
- [ ] Multi-language policy support
- [ ] Advanced visualization dashboards
- [ ] Automated compliance reporting
- [ ] Integration with legal databases