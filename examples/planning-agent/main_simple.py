"""
Simple Planning Agent Example
==============================
A streamlined planning agent that demonstrates the core capabilities
of deepagents for requirements analysis and development planning.

Usage:
    python main_simple.py

This will run the agent in an interactive mode where you can:
1. Ask it to plan for specific epic IDs
2. Get recommendations based on mock requirements
3. See the agent's planning process in action

Supports both Anthropic Claude and OpenAI GPT models.
Set ANTHROPIC_API_KEY or OPENAI_API_KEY environment variable.
"""

import os
import json
from typing import List, Optional, cast
from deepagents import create_deep_agent
from deepagents.types import SubAgent
from langchain_core.tools import tool


# ============================================================================
# Step 1: Define Planning Tools
# ============================================================================

@tool
def fetch_rally_requirements(epic_id: str, feature_id: Optional[str] = None) -> str:
    """
    Fetch requirements from Rally based on Epic/Feature ID.
    
    Args:
        epic_id: The Rally Epic ID (e.g., "US12345")
        feature_id: Optional Feature ID for more specific requirements
        
    Returns:
        JSON string containing requirement details
    """
    # Mock implementation - replace with actual Rally API call
    mock_requirement = {
        "epic_id": epic_id,
        "feature_id": feature_id,
        "title": "Implement Multi-Factor Authentication System",
        "description": "Add comprehensive MFA capability to improve security across all user-facing applications. This includes SMS-based OTP, authenticator app support (TOTP), and backup codes.",
        "acceptance_criteria": [
            "Users can enable MFA via SMS or authenticator app",
            "MFA is required for admin users by default",
            "Backup codes are generated and securely stored",
            "Integration with existing authentication service",
            "MFA can be disabled by admins for specific users",
            "Support for recovery flow when user loses access to MFA device"
        ],
        "business_value": "Reduce security incidents by 80% and meet SOC2 compliance requirements for Q4 2025 audit",
        "priority": "Critical",
        "target_release": "Q4 2025",
        "affected_systems": [
            "auth-service (backend API)",
            "user-management-api",
            "frontend-web-app",
            "mobile-app (iOS and Android)"
        ],
        "compliance_requirements": ["SOC2", "GDPR", "HIPAA"],
        "stakeholders": ["Security Team", "Product Team", "Engineering", "Compliance Officer"]
    }
    
    return json.dumps(mock_requirement, indent=2)


@tool
def search_codebase(
    query: str,
    service_name: Optional[str] = None,
    file_type: Optional[str] = None
) -> str:
    """
    Search the codebase for relevant implementations, patterns, and examples.
    
    Args:
        query: What to search for (e.g., "authentication", "MFA", "security")
        service_name: Optional service to focus search on
        file_type: Optional file extension filter (e.g., ".py", ".ts")
        
    Returns:
        JSON string with search results
    """
    # Mock implementation - in production, this would search actual repos
    mock_results = {
        "query": query,
        "service_filter": service_name,
        "total_results": 8,
        "results": [
            {
                "service": "auth-service",
                "file": "src/auth/providers/oauth.py",
                "line": 45,
                "snippet": "def verify_token(token: str) -> Optional[User]:\n    # Existing token verification logic\n    decoded = jwt.decode(token, SECRET_KEY)\n    return User.get(decoded['user_id'])",
                "relevance": "high",
                "notes": "Existing token verification can be extended for MFA tokens"
            },
            {
                "service": "auth-service",
                "file": "src/auth/models/user.py",
                "line": 23,
                "snippet": "class User(BaseModel):\n    id: UUID\n    email: str\n    password_hash: str\n    # TODO: Add MFA fields",
                "relevance": "high",
                "notes": "User model needs mfa_enabled, mfa_secret, backup_codes fields"
            },
            {
                "service": "frontend-web-app",
                "file": "src/components/Auth/LoginForm.tsx",
                "line": 67,
                "snippet": "const handleLogin = async (credentials) => {\n  const response = await authApi.login(credentials);\n  // TODO: Handle MFA flow\n  setToken(response.token);\n}",
                "relevance": "medium",
                "notes": "Login flow needs MFA challenge/response UI"
            }
        ],
        "similar_implementations": [
            {
                "feature": "Password Reset Flow",
                "location": "auth-service/src/auth/password_reset.py",
                "pattern": "Token-based verification with time expiry",
                "lessons_learned": "Need robust error handling and clear user feedback"
            }
        ],
        "technical_dependencies": [
            "pyotp (Python TOTP library)",
            "twilio (SMS provider)",
            "qrcode (for QR code generation)",
            "cryptography (for secure backup codes)"
        ]
    }
    
    return json.dumps(mock_results, indent=2)


@tool
def analyze_technical_feasibility(
    feature_description: str,
    affected_services: List[str]
) -> str:
    """
    Analyze technical feasibility, identify risks, and estimate complexity.
    
    Args:
        feature_description: Description of the feature
        affected_services: List of services that will be modified
        
    Returns:
        JSON string with feasibility analysis
    """
    mock_analysis = {
        "feature": feature_description,
        "affected_services": affected_services,
        "feasibility_score": 0.85,
        "verdict": "Feasible with moderate complexity",
        "technical_assessment": {
            "backend_complexity": "Medium - existing auth infrastructure can be extended",
            "frontend_complexity": "Medium - new UI flows needed for MFA setup and verification",
            "mobile_complexity": "High - platform-specific integrations for biometrics",
            "integration_complexity": "Low - well-documented SMS/TOTP libraries available"
        },
        "estimated_effort": {
            "development_hours": 240,
            "testing_hours": 80,
            "documentation_hours": 24,
            "total_hours": 344,
            "story_points": 34,
            "sprints": "3-4 (6-8 weeks)"
        },
        "risks": [
            {
                "risk": "SMS delivery reliability varies by region",
                "impact": "High",
                "probability": "Medium",
                "mitigation": "Implement fallback to email OTP, consider multiple SMS providers"
            },
            {
                "risk": "User lockout scenarios if MFA device is lost",
                "impact": "High",
                "probability": "High",
                "mitigation": "Robust backup codes system and admin override capability"
            },
            {
                "risk": "Increased support burden during rollout",
                "impact": "Medium",
                "probability": "High",
                "mitigation": "Comprehensive user documentation, gradual rollout, support team training"
            }
        ],
        "prerequisites": [
            "Security architecture review and approval",
            "SMS provider contract negotiation and setup",
            "Compliance review for phone number storage",
            "Load testing for increased auth traffic"
        ],
        "recommendations": [
            "Phase 1: TOTP (authenticator apps) - least dependencies",
            "Phase 2: SMS OTP - requires provider integration",
            "Phase 3: Backup codes and recovery flows",
            "Use feature flags for gradual rollout",
            "Start with optional MFA, then mandate for admins"
        ]
    }
    
    return json.dumps(mock_analysis, indent=2)


@tool
def get_team_resources() -> str:
    """
    Get current team capacity and skill availability.
    
    Returns:
        JSON string with team resource information
    """
    mock_resources = {
        "planning_period": "Q4 2025",
        "available_teams": {
            "backend": {
                "capacity_hours_per_sprint": 400,
                "current_utilization": 0.75,
                "key_skills": ["Python", "FastAPI", "PostgreSQL", "Security"],
                "available_capacity": 100
            },
            "frontend": {
                "capacity_hours_per_sprint": 320,
                "current_utilization": 0.80,
                "key_skills": ["React", "TypeScript", "UI/UX"],
                "available_capacity": 64
            },
            "mobile": {
                "capacity_hours_per_sprint": 240,
                "current_utilization": 0.70,
                "key_skills": ["React Native", "iOS", "Android"],
                "available_capacity": 72
            },
            "qa": {
                "capacity_hours_per_sprint": 240,
                "current_utilization": 0.85,
                "key_skills": ["Test Automation", "Security Testing"],
                "available_capacity": 36
            }
        },
        "recommended_allocation": {
            "backend": 120,
            "frontend": 60,
            "mobile": 60,
            "qa": 40,
            "total": 280
        }
    }
    
    return json.dumps(mock_resources, indent=2)


# ============================================================================
# Step 2: Define Planning Agent Instructions
# ============================================================================

PLANNING_AGENT_INSTRUCTIONS = """You are an expert Software Development Planning Agent. Your role is to analyze requirements and create comprehensive development plans.

## Your Process:

1. **Understand Requirements**
   - Use fetch_rally_requirements to get the epic/feature details
   - Analyze acceptance criteria, business value, and affected systems
   - Identify all stakeholders and compliance requirements

2. **Research Existing Code**
   - Use search_codebase to find relevant existing implementations
   - Identify patterns that can be reused or extended
   - Note technical dependencies and constraints

3. **Assess Feasibility**
   - Use analyze_technical_feasibility to evaluate complexity and risks
   - Get team capacity with get_team_resources
   - Identify potential blockers and prerequisites

4. **Create Comprehensive Plan**
   - Break down the work into phases
   - Map work to specific services and teams
   - Provide realistic timelines and resource allocation
   - Document risks and mitigation strategies
   - Generate clarifying questions for ambiguous requirements

5. **Generate Planning Documents**
   - Create a detailed markdown planning document
   - Include all sections: summary, approach, phases, risks, timeline
   - Use the file system tools to save your plan

## Output Format:

Create a planning document with these sections:
- Executive Summary
- Requirements Overview
- Technical Approach
- Implementation Phases
- Resource Allocation
- Risk Assessment
- Timeline & Milestones
- Open Questions & Clarifications

Be specific, realistic, and thorough in your planning."""


# ============================================================================
# Step 3: Define Specialized Sub-Agents
# ============================================================================

REQUIREMENTS_ANALYST: SubAgent = {
    "name": "requirements-analyst",
    "description": "Specializes in analyzing requirements, identifying gaps, and generating clarifying questions",
    "prompt": """You are a Requirements Analysis Specialist. Your job is to:

1. Parse requirements thoroughly and identify all explicit and implicit needs
2. Break down high-level features into detailed technical tasks
3. Identify edge cases and potential gaps in requirements
4. Generate specific, actionable clarifying questions
5. Map acceptance criteria to testable conditions

Be thorough and don't make assumptions. Ask specific questions when requirements are unclear."""
}

TECHNICAL_RESEARCHER: SubAgent = {
    "name": "technical-researcher",
    "description": "Searches codebases, analyzes existing implementations, and identifies technical patterns",
    "prompt": """You are a Technical Research Specialist. Your job is to:

1. Search codebases systematically for relevant implementations
2. Identify reusable components and patterns
3. Document technical dependencies and constraints
4. Find similar past implementations for reference
5. Provide specific recommendations based on existing code

Be comprehensive in your research and provide specific file paths and code examples."""
}

RISK_ANALYST: SubAgent = {
    "name": "risk-analyst",
    "description": "Identifies technical and project risks and proposes mitigation strategies",
    "prompt": """You are a Risk Analysis Specialist. Your job is to:

1. Identify technical, operational, and project risks
2. Assess impact and probability of each risk
3. Propose concrete mitigation strategies
4. Flag dependencies and potential blockers
5. Recommend phased rollout strategies to minimize risk

Focus on actionable mitigations, not just identifying risks."""
}


# ============================================================================
# Step 4: Create and Configure the Planning Agent
# ============================================================================

def create_planning_agent():
    """
    Create the planning agent with all tools and subagents configured.
    
    Automatically detects which API key is available and uses the appropriate model:
    - ANTHROPIC_API_KEY -> Claude Sonnet 4 (default)
    - OPENAI_API_KEY -> GPT-4o
    
    Returns:
        Configured deepagent ready for planning tasks
    """
    tools = [
        fetch_rally_requirements,
        search_codebase,
        analyze_technical_feasibility,
        get_team_resources,
    ]
    
    # Type cast to satisfy the type checker
    subagents: List[SubAgent] = [
        cast(SubAgent, REQUIREMENTS_ANALYST),
        cast(SubAgent, TECHNICAL_RESEARCHER),
        cast(SubAgent, RISK_ANALYST),
    ]
    
    # Auto-detect which model to use based on available API keys
    model = None
    if os.getenv("OPENAI_API_KEY"):
        try:
            from langchain_openai import ChatOpenAI
            model = ChatOpenAI(model="gpt-4.1-mini", temperature=0)
            print("🤖 Using OpenAI GPT-4.1-mini")
        except ImportError:
            print("⚠️  OpenAI key found but langchain-openai not installed")
            print("   Install with: pip install langchain-openai")
    elif os.getenv("ANTHROPIC_API_KEY"):
        print("🤖 Using Anthropic Claude Sonnet 4 (default)")
    else:
        print("⚠️  No API key found. Set ANTHROPIC_API_KEY or OPENAI_API_KEY")
    
    agent = create_deep_agent(
        tools=tools,
        instructions=PLANNING_AGENT_INSTRUCTIONS,
        subagents=subagents,  # type: ignore
        model=model,  # None means use default (Claude)
    )
    
    return agent


# ============================================================================
# Step 5: Agent Interface & Execution
# ============================================================================

def run_planning_session(epic_id: str, additional_context: Optional[str] = None):
    """
    Run a planning session for a given epic.
    
    Args:
        epic_id: Rally Epic ID to plan for
        additional_context: Optional additional context or constraints
    """
    print("\n" + "=" * 80)
    print(f"🚀 Starting Planning Session for Epic: {epic_id}")
    print("=" * 80 + "\n")
    
    agent = create_planning_agent()
    
    # Construct the planning request
    user_message = f"Create a comprehensive development plan for Rally Epic {epic_id}."
    if additional_context:
        user_message += f"\n\nAdditional Context: {additional_context}"
    
    # Run the agent
    print(f"📋 Request: {user_message}\n")
    print("🤖 Agent working...\n")
    
    result = agent.invoke({
        "messages": [{"role": "user", "content": user_message}]
    })
    
    # Display results
    print("\n" + "=" * 80)
    print("✅ Planning Complete!")
    print("=" * 80 + "\n")
    
    # Show files created
    files = result.get("files", {})
    if files:
        print("📁 Generated Files:")
        for filename, content in files.items():
            print(f"\n  📄 {filename}")
            print(f"     Size: {len(content)} characters")
            print(f"     Preview: {content[:200]}...")
    
    # Show final response
    messages = result.get("messages", [])
    if messages:
        final_message = messages[-1]
        print(f"\n💬 Final Response:\n{final_message.content}\n")
    
    # Show todos if any
    todos = result.get("todos", [])
    if todos:
        print("\n✓ Tasks Completed:")
        for i, todo in enumerate(todos, 1):
            status_emoji = "✅" if todo.get("status") == "completed" else "🔄"
            print(f"  {status_emoji} {i}. {todo.get('content')}")
    
    return result


def interactive_mode():
    """
    Run the agent in interactive mode for testing.
    """
    print("\n" + "=" * 80)
    print("🤖 Planning Agent - Interactive Mode")
    print("=" * 80)
    print("\nThis is a demonstration of the deepagents planning agent.")
    print("The agent will analyze requirements, research code, and create plans.\n")
    print("Available commands:")
    print("  - Enter an Epic ID (e.g., 'US12345') to create a plan")
    print("  - Type 'demo' to run a demo planning session")
    print("  - Type 'quit' to exit")
    print("=" * 80 + "\n")
    
    agent = create_planning_agent()
    
    while True:
        user_input = input("\n💬 You: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Goodbye!\n")
            break
        
        if user_input.lower() == 'demo':
            user_input = "Create a comprehensive plan for Epic US12345"
        
        if not user_input:
            continue
        
        print("\n🤖 Agent working...\n")
        
        try:
            result = agent.invoke({
                "messages": [{"role": "user", "content": user_input}]
            })
            
            # Show response
            messages = result.get("messages", [])
            if messages:
                final_message = messages[-1]
                print(f"\n🤖 Agent: {final_message.content}\n")
            
            # Show files if created
            files = result.get("files", {})
            if files:
                print(f"\n📁 Created {len(files)} file(s):")
                for filename in files.keys():
                    print(f"  - {filename}")
        
        except Exception as e:
            print(f"\n❌ Error: {e}\n")


# ============================================================================
# Step 6: Main Entry Point
# ============================================================================

# Export the agent for LangGraph CLI
agent = create_planning_agent()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Command line mode with epic ID
        epic_id = sys.argv[1]
        additional_context = sys.argv[2] if len(sys.argv) > 2 else None
        run_planning_session(epic_id, additional_context)
    else:
        # Interactive mode
        interactive_mode()
