"""
Demo Script - Planning Agent Showcase
=====================================

This script demonstrates the planning agent's capabilities with
a complete walkthrough of a planning session.

Run with: python demo.py
"""

import os
import json
from main_simple import (
    fetch_rally_requirements,
    search_codebase,
    analyze_technical_feasibility,
    get_team_resources,
    create_planning_agent,
)


def print_section(title: str):
    """Print a formatted section header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def print_subsection(title: str):
    """Print a formatted subsection header."""
    print(f"\n{title}")
    print("-" * 80)


def demo_tools():
    """Demonstrate each tool individually."""
    print_section("PART 1: Tool Demonstrations")
    
    print("The planning agent has access to several specialized tools.")
    print("Let's see each one in action:\n")
    
    # Tool 1: Fetch Requirements
    print_subsection("🎯 Tool 1: Fetch Rally Requirements")
    print("This tool retrieves epic/feature details from Rally (or other PM tools)")
    print("\nExample: fetch_rally_requirements('US12345')\n")
    
    result = fetch_rally_requirements.invoke({"epic_id": "US12345"})
    data = json.loads(result)
    
    print(f"Epic ID: {data['epic_id']}")
    print(f"Title: {data['title']}")
    print(f"Priority: {data['priority']}")
    print(f"Target Release: {data['target_release']}")
    print(f"\nAcceptance Criteria ({len(data['acceptance_criteria'])} items):")
    for i, criterion in enumerate(data['acceptance_criteria'][:3], 1):
        print(f"  {i}. {criterion}")
    if len(data['acceptance_criteria']) > 3:
        print(f"  ... and {len(data['acceptance_criteria']) - 3} more")
    
    # Tool 2: Search Codebase
    print_subsection("🔍 Tool 2: Search Codebase")
    print("This tool searches repositories for relevant code and implementations")
    print("\nExample: search_codebase('authentication', service_name='auth-service')\n")
    
    result = search_codebase.invoke({
        "query": "authentication",
        "service_name": "auth-service"
    })
    data = json.loads(result)
    
    print(f"Query: {data['query']}")
    print(f"Total Results: {data['total_results']}")
    print(f"\nSample Result:")
    if data['results']:
        sample = data['results'][0]
        print(f"  File: {sample['file']}")
        print(f"  Line: {sample['line']}")
        print(f"  Relevance: {sample['relevance']}")
        print(f"  Snippet: {sample['snippet'][:80]}...")
    
    # Tool 3: Analyze Feasibility
    print_subsection("⚡ Tool 3: Analyze Technical Feasibility")
    print("This tool evaluates complexity, estimates effort, and identifies risks")
    print("\nExample: analyze_technical_feasibility('MFA system', ['auth-service', 'frontend'])\n")
    
    result = analyze_technical_feasibility.invoke({
        "feature_description": "Multi-factor authentication system",
        "affected_services": ["auth-service", "frontend-web-app"]
    })
    data = json.loads(result)
    
    print(f"Verdict: {data['verdict']}")
    print(f"Feasibility Score: {data['feasibility_score']}")
    print(f"\nEstimated Effort:")
    effort = data['estimated_effort']
    print(f"  Development: {effort['development_hours']}h")
    print(f"  Testing: {effort['testing_hours']}h")
    print(f"  Total: {effort['total_hours']}h ({effort['story_points']} story points)")
    print(f"\nRisks Identified: {len(data['risks'])}")
    for risk in data['risks'][:2]:
        print(f"  • {risk['risk']} [{risk['impact']} impact]")
    
    # Tool 4: Team Resources
    print_subsection("👥 Tool 4: Get Team Resources")
    print("This tool retrieves team capacity and availability")
    print("\nExample: get_team_resources()\n")
    
    result = get_team_resources.invoke({})
    data = json.loads(result)
    
    print(f"Planning Period: {data['planning_period']}")
    print(f"\nTeam Availability:")
    for team_name, team_data in data['available_teams'].items():
        utilization = team_data['current_utilization']
        available = team_data['available_capacity']
        print(f"  {team_name:15} - {utilization:.0%} utilized, {available}h available")


def demo_agent_workflow():
    """Demonstrate the complete agent workflow."""
    print_section("PART 2: Complete Planning Workflow")
    
    print("Now let's see how the agent uses these tools together to create a plan.\n")
    print("When you ask the agent to 'Create a plan for Epic US12345', it will:")
    print("  1. Fetch the requirements from Rally")
    print("  2. Search the codebase for relevant implementations")
    print("  3. Analyze technical feasibility and complexity")
    print("  4. Check team resource availability")
    print("  5. Generate a comprehensive planning document")
    print("  6. Create actionable todos to track the planning process\n")
    
    api_key = os.getenv("ANTHROPIC_API_KEY") or os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("⚠️  Note: To see the full agent workflow, you need to set an API key:")
        print("   export ANTHROPIC_API_KEY='your-key-here'")
        print("\nFor now, we've demonstrated the individual tools above.")
    else:
        print("✅ API key detected - the agent is ready to run!")
        print("\nTo run the full planning workflow, execute:")
        print("   python main_simple.py US12345")


def demo_subagents():
    """Explain the sub-agent architecture."""
    print_section("PART 3: Specialized Sub-Agents")
    
    print("The planning agent can delegate work to specialized sub-agents:\n")
    
    print("1. 🎯 Requirements Analyst")
    print("   • Deeply analyzes requirements")
    print("   • Identifies gaps and ambiguities")
    print("   • Generates clarifying questions")
    print("   • Maps acceptance criteria to technical tasks\n")
    
    print("2. 🔬 Technical Researcher")
    print("   • Searches codebases systematically")
    print("   • Finds reusable components")
    print("   • Documents technical patterns")
    print("   • Provides specific recommendations\n")
    
    print("3. 🛡️  Risk Analyst")
    print("   • Identifies potential risks")
    print("   • Assesses impact and probability")
    print("   • Proposes mitigation strategies")
    print("   • Recommends phased rollout approaches\n")
    
    print("These sub-agents work together to provide comprehensive analysis.")


def demo_output_format():
    """Explain the output format."""
    print_section("PART 4: Output & Planning Documents")
    
    print("When the agent completes a planning session, it generates:\n")
    
    print("📄 Planning Document (Markdown)")
    print("   • Executive Summary")
    print("   • Requirements Overview")
    print("   • Technical Approach")
    print("   • Implementation Phases")
    print("   • Resource Allocation")
    print("   • Risk Assessment")
    print("   • Timeline & Milestones")
    print("   • Open Questions\n")
    
    print("📊 Planning Summary (JSON)")
    print("   • Key metrics and estimates")
    print("   • Resource requirements")
    print("   • Critical path items")
    print("   • Risk summary\n")
    
    print("✅ Todo List")
    print("   • Tracks the agent's planning process")
    print("   • Shows completed and pending tasks")
    print("   • Helps user understand progress\n")


def main():
    """Run the complete demo."""
    print("\n" + "█" * 80)
    print("█" + " " * 78 + "█")
    print("█" + " " * 20 + "PLANNING AGENT DEMONSTRATION" + " " * 30 + "█")
    print("█" + " " * 78 + "█")
    print("█" * 80)
    
    print("\nThis demo showcases a comprehensive AI planning agent built with deepagents.")
    print("The agent analyzes requirements, researches code, and generates detailed plans.\n")
    
    input("Press Enter to start the demonstration...")
    
    # Part 1: Tools
    demo_tools()
    input("\n\nPress Enter to continue to the workflow explanation...")
    
    # Part 2: Workflow
    demo_agent_workflow()
    input("\n\nPress Enter to learn about sub-agents...")
    
    # Part 3: Sub-agents
    demo_subagents()
    input("\n\nPress Enter to see the output format...")
    
    # Part 4: Output
    demo_output_format()
    
    # Conclusion
    print_section("NEXT STEPS")
    
    print("Ready to try the agent yourself?\n")
    
    print("1️⃣  Set your API key:")
    print("   export ANTHROPIC_API_KEY='your-anthropic-key'")
    print("   # or")
    print("   export OPENAI_API_KEY='your-openai-key'\n")
    
    print("2️⃣  Run the agent:")
    print("   python main_simple.py                  # Interactive mode")
    print("   python main_simple.py US12345          # Plan for epic")
    print("   langgraph dev                          # Visual debugging\n")
    
    print("3️⃣  Customize for your needs:")
    print("   • Update tool implementations with real APIs")
    print("   • Modify instructions for your workflow")
    print("   • Add custom sub-agents for specialized tasks")
    print("   • Integrate with your PM and source control systems\n")
    
    print("=" * 80)
    print("✨ Thank you for exploring the Planning Agent!")
    print("=" * 80 + "\n")
    
    print("For more information:")
    print("  • README.md - Full documentation")
    print("  • test_tools.py - Test without API key")
    print("  • main_simple.py - Source code\n")


if __name__ == "__main__":
    main()
