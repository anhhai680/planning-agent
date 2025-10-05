"""
Tool-only test script (no API key required)
==========================================

This script tests the planning agent's tools without invoking the LLM,
so it can run without an API key.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from main_simple import (
    create_planning_agent,
    fetch_rally_requirements,
    search_codebase,
    analyze_technical_feasibility,
    get_team_resources,
)


def test_all_tools():
    """Test all tools comprehensively."""
    print("\n" + "=" * 80)
    print("🧪 Planning Agent - Tool Testing Suite (No API Key Required)")
    print("=" * 80 + "\n")
    
    all_passed = True
    
    # Test 1: Fetch Rally Requirements
    print("1️⃣  Testing fetch_rally_requirements")
    print("-" * 80)
    try:
        result = fetch_rally_requirements.invoke({"epic_id": "US12345", "feature_id": "F67890"})
        data = eval(result)  # Parse JSON string
        assert "epic_id" in data
        assert data["epic_id"] == "US12345"
        assert "title" in data
        assert "acceptance_criteria" in data
        print("✅ PASSED - Requirements fetched successfully")
        print(f"   Epic: {data['title']}")
        print(f"   Acceptance Criteria: {len(data['acceptance_criteria'])} items")
        print(f"   Priority: {data['priority']}")
    except Exception as e:
        print(f"❌ FAILED - {e}")
        all_passed = False
    print()
    
    # Test 2: Search Codebase
    print("2️⃣  Testing search_codebase")
    print("-" * 80)
    try:
        result = search_codebase.invoke({
            "query": "authentication",
            "service_name": "auth-service",
            "file_type": ".py"
        })
        data = eval(result)
        assert "query" in data
        assert data["query"] == "authentication"
        assert "results" in data
        assert len(data["results"]) > 0
        print("✅ PASSED - Codebase search working")
        print(f"   Query: {data['query']}")
        print(f"   Results found: {data['total_results']}")
        print(f"   Services: {', '.join(set(r['service'] for r in data['results']))}")
    except Exception as e:
        print(f"❌ FAILED - {e}")
        all_passed = False
    print()
    
    # Test 3: Analyze Technical Feasibility
    print("3️⃣  Testing analyze_technical_feasibility")
    print("-" * 80)
    try:
        result = analyze_technical_feasibility.invoke({
            "feature_description": "Multi-factor authentication system",
            "affected_services": ["auth-service", "frontend-web-app", "mobile-app"]
        })
        data = eval(result)
        assert "feasibility_score" in data
        assert "verdict" in data
        assert "estimated_effort" in data
        assert 0 <= data["feasibility_score"] <= 1
        print("✅ PASSED - Feasibility analysis working")
        print(f"   Verdict: {data['verdict']}")
        print(f"   Feasibility Score: {data['feasibility_score']}")
        print(f"   Estimated Hours: {data['estimated_effort']['total_hours']}")
        print(f"   Story Points: {data['estimated_effort']['story_points']}")
    except Exception as e:
        print(f"❌ FAILED - {e}")
        all_passed = False
    print()
    
    # Test 4: Get Team Resources
    print("4️⃣  Testing get_team_resources")
    print("-" * 80)
    try:
        result = get_team_resources.invoke({})
        data = eval(result)
        assert "planning_period" in data
        assert "available_teams" in data
        teams = data["available_teams"]
        total_capacity = sum(t.get("available_capacity", 0) for t in teams.values())
        print("✅ PASSED - Team resources retrieved")
        print(f"   Planning Period: {data['planning_period']}")
        print(f"   Teams: {len(teams)}")
        print(f"   Total Available Capacity: {total_capacity} hours")
        for team_name, team_data in teams.items():
            print(f"   - {team_name}: {team_data['available_capacity']}h available")
    except Exception as e:
        print(f"❌ FAILED - {e}")
        all_passed = False
    print()
    
    # Test 5: Agent Creation
    print("5️⃣  Testing agent creation")
    print("-" * 80)
    try:
        agent = create_planning_agent()
        assert agent is not None
        print("✅ PASSED - Agent created successfully")
        print(f"   Agent Type: {type(agent).__name__}")
        print(f"   Has invoke method: {hasattr(agent, 'invoke')}")
        print(f"   Has stream method: {hasattr(agent, 'stream')}")
    except Exception as e:
        print(f"❌ FAILED - {e}")
        all_passed = False
    print()
    
    # Summary
    print("=" * 80)
    if all_passed:
        print("✅ ALL TESTS PASSED!")
        print("=" * 80)
        print("\nThe planning agent tools are working correctly.")
        print("\nTo test the full agent (requires API key):")
        print("  1. Set your API key:")
        print("     export ANTHROPIC_API_KEY='your-key-here'")
        print("  2. Run: python test_agent.py")
        print("\nOr try the agent interactively:")
        print("  python main_simple.py")
    else:
        print("❌ SOME TESTS FAILED")
        print("=" * 80)
        sys.exit(1)


if __name__ == "__main__":
    test_all_tools()
