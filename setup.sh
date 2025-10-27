#!/bin/bash

# AI Debate Application Setup Script
# This script helps you set up the application quickly

echo "========================================"
echo "🎭 AI Debate Application Setup"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment found"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Check if .env file exists
echo ""
if [ -f ".env" ]; then
    echo "✅ .env file already exists"
    echo ""
    echo "Current API keys configured:"
    if grep -q "OPENAI_API_KEY=sk-" .env; then
        echo "  ✅ OpenAI API Key"
    else
        echo "  ⚠️  OpenAI API Key not set"
    fi
    
    if grep -q "OPENROUTER_API_KEY=sk-" .env; then
        echo "  ✅ OpenRouter API Key"
    else
        echo "  ⚠️  OpenRouter API Key not set"
    fi
    
    echo ""
    read -p "Do you want to update your .env file? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Skipping .env update"
    else
        rm .env
        create_env=true
    fi
else
    create_env=true
fi

# Create .env file if needed
if [ "$create_env" = true ]; then
    echo ""
    echo "Setting up .env file..."
    echo ""
    
    echo "Enter your OpenAI API Key (press Enter to skip):"
    read -p "OPENAI_API_KEY: " openai_key
    
    echo ""
    echo "Enter your OpenRouter API Key (press Enter to skip):"
    read -p "OPENROUTER_API_KEY: " openrouter_key
    
    # Create .env file
    cat > .env << EOF
# OpenAI API Key
# Get your key from: https://platform.openai.com/api-keys
OPENAI_API_KEY=${openai_key:-your-openai-api-key-here}

# OpenRouter API Key
# Get your key from: https://openrouter.ai/keys
OPENROUTER_API_KEY=${openrouter_key:-your-openrouter-api-key-here}
EOF
    
    echo ""
    echo "✅ .env file created!"
    
    if [ -z "$openai_key" ] && [ -z "$openrouter_key" ]; then
        echo ""
        echo "⚠️  No API keys were entered."
        echo "Please edit the .env file and add your API keys before running the debate."
    fi
fi

echo ""
echo "========================================"
echo "✅ Setup Complete!"
echo "========================================"
echo ""
echo "To run the debate application:"
echo "  1. Make sure you've added API keys to .env file"
echo "  2. Run: python debate.py"
echo ""
echo "Configuration options:"
echo "  - .env file: API keys (required)"
echo "  - JSON config files: Debate settings (optional)"
echo "    Example: python debate.py --config example_debate_config.json"
echo "  - Command-line arguments: Override any setting"
echo "    Example: python debate.py --rounds 3 --topic 'AI safety'"
echo ""
echo "For more options, run: python debate.py --help"
echo ""
echo "Documentation:"
echo "  - README.md for full documentation"
echo "  - docs/QUICK_START.md for quick start guide"
echo "  - docs/JSON_CONFIG_GUIDE.md for JSON configuration"
echo "  - docs/MCP_GUIDE.md for enabling web search tools"
echo ""

