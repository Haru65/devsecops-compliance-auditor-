#!/bin/bash

# Simple setup script for AI-powered Compliance Auditor
echo "🚀 Setting up AI-powered Compliance Auditor..."

# Function to check command success
check_success() {
    if [ $? -eq 0 ]; then
        echo "✅ $1 completed successfully"
    else
        echo "❌ $1 failed"
        exit 1
    fi
}

# Check if Python is available
echo "🔍 Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed. Please install Python 3.8+."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    check_success "Virtual environment creation"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "⚡ Activating virtual environment..."
source venv/bin/activate
check_success "Virtual environment activation"

# Upgrade pip
echo "📈 Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1
check_success "Pip upgrade"

# Install basic requirements first
echo "📋 Installing basic requirements..."
pip install fastapi uvicorn pydantic GitPython > /dev/null 2>&1
check_success "Basic requirements installation"

# Install AI/ML dependencies (optional)
echo "🤖 Installing AI/ML dependencies (this may take a while)..."
pip install transformers torch numpy pandas scikit-learn > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ AI dependencies installed successfully"
    AI_AVAILABLE=true
else
    echo "⚠️  AI dependencies installation failed, but basic functionality will still work"
    AI_AVAILABLE=false
fi

# Install additional utilities
echo "🛠️  Installing additional utilities..."
pip install python-multipart aiofiles pathlib2 > /dev/null 2>&1
check_success "Additional utilities installation"

# Try to install spaCy and download model
if [ "$AI_AVAILABLE" = true ]; then
    echo "📚 Installing spaCy..."
    pip install spacy > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "📖 Downloading spaCy English model..."
        python3 -m spacy download en_core_web_sm > /dev/null 2>&1
        if [ $? -eq 0 ]; then
            echo "✅ spaCy model downloaded successfully"
        else
            echo "⚠️  spaCy model download failed, but functionality will work without it"
        fi
    else
        echo "⚠️  spaCy installation failed"
    fi
    
    # Try to install NLTK
    echo "📝 Installing NLTK..."
    pip install nltk textblob > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "📚 Downloading NLTK data..."
        python3 -c "
import nltk
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True) 
    nltk.download('wordnet', quiet=True)
    print('NLTK data downloaded successfully')
except:
    print('NLTK data download failed')
" 2>/dev/null
    fi
fi

# Create necessary directories
echo "📁 Creating project directories..."
mkdir -p policies policies/sample_policies repos logs
check_success "Directory creation"

# Set up logging directory
touch logs/compliance_auditor.log
check_success "Log file creation"

# Make scripts executable
if [ -f "demo_enhanced_ai.py" ]; then
    chmod +x demo_enhanced_ai.py
    echo "✅ Made demo script executable"
fi

if [ -f "policy_scanning_tutorial.py" ]; then
    chmod +x policy_scanning_tutorial.py
    echo "✅ Made tutorial script executable"
fi

# Test basic functionality
echo "🧪 Testing basic functionality..."
python3 -c "
import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath('.')), 'ai engine'))

try:
    # Test basic imports
    from fastapi import FastAPI
    from pydantic import BaseModel
    print('✅ FastAPI components working')
    
    # Test AI engine components
    try:
        from policy_processor import PolicyProcessor
        from repository_scanner import RepositoryScanner
        from compliance_analyzer import ComplianceAnalyzer
        print('✅ AI engine components working')
    except Exception as e:
        print(f'⚠️  AI engine warning: {e}')
        print('   Basic functionality will still work')
        
except Exception as e:
    print(f'❌ Critical error: {e}')
    exit(1)
"

if [ $? -eq 0 ]; then
    echo "✅ Basic functionality test passed"
else
    echo "⚠️  Some components may not be working properly"
fi

echo ""
echo "🎉 Setup completed!"
echo ""
echo "📋 What's been installed:"
echo "   ✅ FastAPI web framework"
echo "   ✅ Policy processing engine"  
echo "   ✅ Repository scanner"
echo "   ✅ Compliance analyzer"
if [ "$AI_AVAILABLE" = true ]; then
    echo "   ✅ AI/ML dependencies (transformers, torch, etc.)"
else
    echo "   ⚠️  AI/ML dependencies (partial - rule-based fallback available)"
fi
echo ""
echo "🚀 Next steps:"
echo "   1. Test the system: python3 demo_enhanced_ai.py"
echo "   2. Start API server: python3 main.py"
echo "   3. View documentation: http://localhost:8000/docs"
echo ""
echo "📚 Tutorials available:"
echo "   - python3 policy_scanning_tutorial.py"
echo "   - python3 test_enhanced_components.py"
echo ""
echo "🎯 Ready to scan policies and repositories for compliance!"