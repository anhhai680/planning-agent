"""
Test script for the Planning Agent
===================================

This script runs basic tests to verify the planning agent is working correctly.

Usage:
    python test_agent.py
"""

import os
import sys
from pathlib import Path

# Add parent directory to path to import main_simple
sys.path.insert(0, str(Path(__file__).parent))

from main_simple import (
    create_planning_agent,
    fetch_rally_requirements,
    search_codebase,
    analyze_technical_feasibility,
    get_team_resources,
)


def test_tools():
    """Test that all tools work correctly."""
    print("\n" + "=" * 80)
    print("Testing Individual Tools")
    print("=" * 80 + "\n")
    
    # Test 1: Fetch Rally Requirements
    print("1. Testing fetch_rally_requirements...")
    result = fetch_rally_requirements.invoke({"epic_id": "US12345"})
    assert "epic_id" in result
    assert "US12345" in result
    print("   ✅ fetch_rally_requirements works!\n")
    
    # Test 2: Search Codebase
    print("2. Testing search_codebase...")
    result = search_codebase.invoke({"query": "authentication"})
    assert "query" in result
    assert "authentication" in result
    print("   ✅ search_codebase works!\n")
    
    # Test 3: Analyze Feasibility
    print("3. Testing analyze_technical_feasibility...")
    result = analyze_technical_feasibility.invoke({
        "feature_description": "MFA implementation",
        "affected_services": ["auth-service", "frontend"]
    })
    assert "feasibility_score" in result
    print("   ✅ analyze_technical_feasibility works!\n")
    
    # Test 4: Get Team Resources
    print("4. Testing get_team_resources...")
    result = get_team_resources.invoke({})
    assert "available_teams" in result
    print("   ✅ get_team_resources works!\n")
    
    print("✅ All tools passed!\n")


def test_agent_creation():
    """Test that the agent can be created successfully."""
    print("\n" + "=" * 80)
    print("Testing Agent Creation")
    print("=" * 80 + "\n")
    
    try:
        agent = create_planning_agent()
        print("✅ Agent created successfully!")
        print(f"   Agent type: {type(agent)}")
        return agent
    except Exception as e:
        print(f"❌ Failed to create agent: {e}")
        raise


def test_simple_invoke(agent):
    """Test a simple agent invocation."""
    print("\n" + "=" * 80)
    print("Testing Simple Agent Invocation")
    print("=" * 80 + "\n")
    
    try:
        print("Sending message: 'What tools do you have available?'")
        result = agent.invoke({
            "messages": [{"role": "user", "content": "What tools do you have available?"}]
        })
        
        print("\n✅ Agent invoked successfully!")
        
        # Check response structure
        assert "messages" in result, "Result should have 'messages' key"
        messages = result["messages"]
        print(f"   Received {len(messages)} message(s)")
        
        if messages:
            last_message = messages[-1]
            print(f"   Last message type: {last_message.type}")
            print(f"   Response preview: {str(last_message.content)[:200]}...")
        
        return result
    except Exception as e:
        print(f"❌ Failed to invoke agent: {e}")
        import traceback
        traceback.print_exc()
        raise


def test_planning_request(agent):
    """Test a full planning request."""
    print("\n" + "=" * 80)
    print("Testing Full Planning Request")
    print("=" * 80 + "\n")
    
    try:
        print("Requesting plan for Epic US12345...")
        result = agent.invoke({
            "messages": [{
                "role": "user",
                "content": "Create a brief plan for Epic US12345. Just give me a high-level overview."
            }]
        })
        
        print("\n✅ Planning request completed!")
        
        # Check for various outputs
        if "messages" in result:
            print(f"   Messages: {len(result['messages'])}")
        
        if "files" in result:
            files = result["files"]
            print(f"   Files created: {len(files)}")
            for filename in files.keys():
                print(f"     - {filename}")
        
        if "todos" in result:
            todos = result["todos"]
            print(f"   Todo items: {len(todos)}")
            for todo in todos[:3]:  # Show first 3
                print(f"     - {todo.get('content', 'N/A')} [{todo.get('status', 'N/A')}]")
        
        return result
    except Exception as e:
        print(f"❌ Failed planning request: {e}")
        import traceback
        traceback.print_exc()
        raise


def main():
    """Run all tests."""
    print("\n" + "=" * 80)
    print("🧪 Planning Agent Test Suite")
    print("=" * 80)
    
    # Check environment
    print("\n📋 Environment Check:")
    api_key = os.getenv("ANTHROPIC_API_KEY") or os.getenv("OPENAI_API_KEY")
    if api_key:
        print("   ✅ API key found")
    else:
        print("   ⚠️  No API key found (ANTHROPIC_API_KEY or OPENAI_API_KEY)")
        print("   Tests may fail without a valid API key.")
    
    try:
        # Test 1: Individual tools
        test_tools()
        
        # Test 2: Agent creation
        agent = test_agent_creation()
        
        # Test 3: Simple invocation
        test_simple_invoke(agent)
        
        # Test 4: Full planning request
        test_planning_request(agent)
        
        # Success!
        print("\n" + "=" * 80)
        print("✅ ALL TESTS PASSED!")
        print("=" * 80 + "\n")
        print("The planning agent is working correctly!")
        print("You can now run:")
        print("  - python main_simple.py                (interactive mode)")
        print("  - python main_simple.py US12345        (plan for epic)")
        print("  - langgraph dev                         (LangGraph Studio)")
        print("\n")
        
    except Exception as e:
        print("\n" + "=" * 80)
        print("❌ TESTS FAILED")
        print("=" * 80 + "\n")
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
