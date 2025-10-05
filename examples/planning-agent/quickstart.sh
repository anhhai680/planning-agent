#!/bin/bash
# Quick start script for the planning agent

echo "========================================"
echo "Planning Agent - Quick Start"
echo "========================================"
echo ""

# Check if API key is set
if [ -z "$ANTHROPIC_API_KEY" ] && [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  Warning: No API key found"
    echo ""
    echo "To use this agent, you need to set an API key:"
    echo ""
    echo "For Claude (recommended):"
    echo "  export ANTHROPIC_API_KEY='your-key-here'"
    echo ""
    echo "For OpenAI:"
    echo "  export OPENAI_API_KEY='your-key-here'"
    echo ""
    echo "Get your API key from:"
    echo "  - Anthropic: https://console.anthropic.com/settings/keys"
    echo "  - OpenAI: https://platform.openai.com/api-keys"
    echo ""
    read -p "Do you want to continue with tool testing only? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
    echo ""
    echo "Running tool tests only (no LLM required)..."
    python test_agent.py
else
    echo "✅ API key found"
    echo ""
    echo "Running full test suite..."
    python test_agent.py
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "========================================"
        echo "✅ Tests Passed! Agent is ready to use"
        echo "========================================"
        echo ""
        echo "Try these commands:"
        echo ""
        echo "1. Interactive mode:"
        echo "   python main_simple.py"
        echo ""
        echo "2. Plan for a specific epic:"
        echo "   python main_simple.py US12345"
        echo ""
        echo "3. With additional context:"
        echo "   python main_simple.py US12345 'Focus on security'"
        echo ""
        echo "4. LangGraph Studio (visual debugging):"
        echo "   langgraph dev"
        echo ""
    fi
fi
