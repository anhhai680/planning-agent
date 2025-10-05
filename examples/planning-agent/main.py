"""
Rally Requirements Planning Agent
===================================
A comprehensive planning agent that takes Rally Epic/Feature numbers,
researches indexed GitHub repositories, analyzes requirements, and 
generates detailed planning documents.

Based on: https://github.com/langchain-ai/deepagents

This example demonstrates:
1. Using deepagents to create an AI planning agent
2. Defining custom tools for requirement gathering
3. Creating subagents for specialized tasks
4. Generating comprehensive planning documents
"""

import json
from typing import Literal, List, Dict, Any, Optional
from datetime import datetime
from dataclasses import dataclass
from deepagents import create_deep_agent
from langchain_core.tools import tool

# ============================================================================
# Step 1: Define Data Models (Input/Output Schema)
# ============================================================================

@dataclass
class RallyRequirement:
    """Rally Epic/Feature requirement structure"""
    epic_id: str
    feature_id: Optional[str]
    title: str
    description: str
    acceptance_criteria: List[str]
    business_value: str
    priority: Literal["Critical", "High", "Medium", "Low"]
    target_release: str

@dataclass
class RepositoryContext:
    """GitHub repository analysis context"""
    repo_name: str
    relevant_files: List[str]
    existing_implementations: List[str]
    dependencies: List[str]
    technical_constraints: List[str]

@dataclass
class PlanningOutput:
    """Comprehensive planning document structure"""
    epic_id: str
    feature_id: Optional[str]
    executive_summary: str
    requirements_analysis: Dict[str, Any]
    technical_approach: Dict[str, Any]
    repository_breakdown: List[Dict[str, Any]]
    development_phases: List[Dict[str, Any]]
    resource_allocation: Dict[str, Any]
    risk_assessment: Dict[str, Any]
    timeline: Dict[str, Any]
    clarifying_questions: List[str]
    dependencies: List[str]
    acceptance_criteria_mapping: Dict[str, Any]
    generated_at: str
    confidence_score: float

# ============================================================================
# Step 2: Tool Definitions (External Integrations)
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
    # In production, this would call Rally API
    # Mock implementation for demonstration
    mock_requirement = {
        "epic_id": epic_id,
        "feature_id": feature_id,
        "title": "Implement Multi-Factor Authentication",
        "description": "Add MFA capability to improve security across all user-facing applications",
        "acceptance_criteria": [
            "Users can enable MFA via SMS or authenticator app",
            "MFA is required for admin users",
            "Backup codes are generated and securely stored",
            "Integration with existing authentication service",
            "MFA can be disabled by admins for specific users"
        ],
        "business_value": "Reduce security incidents by 80% and meet SOC2 compliance requirements",
        "priority": "Critical",
        "target_release": "Q4 2025",
        "affected_systems": [
            "auth-service",
            "user-management-api", 
            "frontend-web-app",
            "mobile-app"
        ],
        "compliance_requirements": ["SOC2", "GDPR"],
        "stakeholders": ["Security Team", "Product Team", "Engineering"]
    }
    
    return json.dumps(mock_requirement, indent=2)


@tool
def search_github_repositories(
    query: str,
    repositories: Optional[List[str]] = None,
    max_results: int = 10,
    search_type: Literal["code", "files", "commits", "issues"] = "code",
    file_extensions: Optional[List[str]] = None,
    case_sensitive: bool = False,
    clone_depth: Literal["shallow", "recent", "full"] = "recent"
) -> str:
    """
    Search GitHub repositories by cloning and using grep to search directly.
    Provides configurable depth for balancing speed vs context richness.
    
    Args:
        query: Search query (e.g., "authentication implementation", "MFA integration")
        repositories: List of repository URLs to search (e.g., ["https://github.com/org/repo"])
        max_results: Maximum number of results to return per repository
        search_type: Type of content to search (currently supports "code" and "files")
        file_extensions: Optional list of file extensions to search (e.g., [".py", ".js", ".java"])
        case_sensitive: Whether search should be case-sensitive
        clone_depth: Clone strategy - 'shallow' (latest commit only), 'recent' (last 100 commits, recommended), 'full' (entire history)
        
    Returns:
        JSON string with search results including file paths, code snippets, and historical context
    """
    import subprocess
    import tempfile
    import shutil
    import re
    from pathlib import Path
    from collections import defaultdict
    
    if not repositories:
        return json.dumps({
            "error": "No repositories specified. Please provide a list of GitHub repository URLs.",
            "example": ["https://github.com/org/auth-service", "https://github.com/org/user-api"]
        }, indent=2)
    
    # Configure clone depth based on strategy
    clone_config = {
        "shallow": {"depth": 1, "description": "Latest commit only (fastest)"},
        "recent": {"depth": 100, "description": "Last 100 commits (balanced - recommended)"},
        "full": {"depth": None, "description": "Full history (slowest, most context)"}
    }
    
    depth_setting = clone_config.get(clone_depth, clone_config["recent"])
    
    results = {
        "query": query,
        "repositories_searched": repositories,
        "search_type": search_type,
        "clone_strategy": {
            "type": clone_depth,
            "description": depth_setting["description"]
        },
        "total_results": 0,
        "results": [],
        "errors": []
    }
    
    # Create temporary directory for cloning repos
    temp_base_dir = tempfile.mkdtemp(prefix="repo_search_")
    
    try:
        for repo_url in repositories:
            try:
                # Extract repo name from URL
                repo_name = repo_url.rstrip('/').split('/')[-1].replace('.git', '')
                repo_path = Path(temp_base_dir) / repo_name
                
                print(f"📥 Cloning {repo_name} ({clone_depth} mode)...")
                
                # Build clone command based on depth strategy
                clone_cmd = ['git', 'clone', '--quiet']
                
                if depth_setting["depth"]:
                    clone_cmd.extend(['--depth', str(depth_setting["depth"])])
                
                clone_cmd.extend([repo_url, str(repo_path)])
                
                clone_result = subprocess.run(
                    clone_cmd,
                    capture_output=True,
                    text=True,
                    timeout=120  # Increased timeout for deeper clones
                )
                
                if clone_result.returncode != 0:
                    results["errors"].append({
                        "repository": repo_name,
                        "error": f"Failed to clone: {clone_result.stderr}"
                    })
                    continue
                
                print(f"🔍 Searching in {repo_name}...")
                
                # Get repository context and statistics
                repo_context = {
                    "repository": repo_name,
                    "clone_depth": clone_depth
                }
                
                # Analyze repository structure
                structure_cmd = ['find', str(repo_path), '-type', 'f', 
                               '!', '-path', '*/.*', 
                               '!', '-path', '*/node_modules/*',
                               '!', '-path', '*/venv/*']
                structure_result = subprocess.run(structure_cmd, capture_output=True, text=True, timeout=30)
                
                if structure_result.returncode == 0:
                    all_files = structure_result.stdout.strip().split('\n')
                    file_types = defaultdict(int)
                    for f in all_files:
                        ext = Path(f).suffix
                        if ext:
                            file_types[ext] += 1
                    
                    repo_context["statistics"] = {
                        "total_files": len(all_files),
                        "file_types": dict(file_types),
                        "primary_languages": sorted(file_types.items(), key=lambda x: x[1], reverse=True)[:5]
                    }
                
                # Get commit history context for better understanding
                if clone_depth != "shallow":
                    git_log_cmd = [
                        'git', '-C', str(repo_path), 'log',
                        '--oneline',
                        '--all',
                        '--graph',
                        f'--max-count={depth_setting["depth"] or 100}'
                    ]
                    log_result = subprocess.run(git_log_cmd, capture_output=True, text=True, timeout=30)
                    
                    if log_result.returncode == 0:
                        commits = log_result.stdout.strip().split('\n')
                        repo_context["recent_commits"] = {
                            "count": len(commits),
                            "sample": commits[:10]  # First 10 for context
                        }
                
                # Get branch information
                branches_cmd = ['git', '-C', str(repo_path), 'branch', '-a']
                branches_result = subprocess.run(branches_cmd, capture_output=True, text=True, timeout=10)
                if branches_result.returncode == 0:
                    branches = [b.strip().replace('* ', '') for b in branches_result.stdout.strip().split('\n')]
                    repo_context["branches"] = branches[:10]  # Limit to 10 branches
                
                # Get contributors for context
                contributors_cmd = ['git', '-C', str(repo_path), 'shortlog', '-sn', '--all']
                contributors_result = subprocess.run(contributors_cmd, capture_output=True, text=True, timeout=20)
                if contributors_result.returncode == 0:
                    contributors = contributors_result.stdout.strip().split('\n')[:10]  # Top 10
                    repo_context["top_contributors"] = contributors
                
                results["results"].append(repo_context)
                
                if search_type == "code":
                    # Use grep to search for code with extended context
                    grep_cmd = ['grep', '-r', '-n']  # recursive, line numbers
                    
                    # Case sensitivity
                    if not case_sensitive:
                        grep_cmd.append('-i')
                    
                    # Add more context lines for better understanding
                    grep_cmd.extend(['-B', '5', '-A', '5'])  # 5 lines before and after
                    
                    # Exclude common directories
                    grep_cmd.extend([
                        '--exclude-dir=.git',
                        '--exclude-dir=node_modules',
                        '--exclude-dir=venv',
                        '--exclude-dir=__pycache__',
                        '--exclude-dir=dist',
                        '--exclude-dir=build',
                        '--exclude-dir=.pytest_cache',
                        '--exclude-dir=coverage',
                        '--exclude-dir=.idea',
                        '--exclude-dir=.vscode'
                    ])
                    
                    # File extensions filter
                    if file_extensions:
                        for ext in file_extensions:
                            grep_cmd.append(f'--include=*{ext}')
                    
                    grep_cmd.extend([query, str(repo_path)])
                    
                    grep_result = subprocess.run(
                        grep_cmd,
                        capture_output=True,
                        text=True,
                        timeout=60
                    )
                    
                    # Parse grep output with enhanced context
                    if grep_result.stdout:
                        lines = grep_result.stdout.split('\n')
                        current_file = None
                        current_matches = []
                        match_context = []
                        
                        for line in lines:
                            if not line.strip():
                                continue
                            
                            # Check if this is a file:line_number: match
                            match = re.match(r'^(.+?):(\d+):(.*)', line)
                            if match:
                                file_path, line_num, content = match.groups()
                                
                                # Make path relative to repo
                                rel_path = Path(file_path).relative_to(repo_path)
                                
                                if current_file != str(rel_path):
                                    # Save previous file's results with enriched context
                                    if current_file and current_matches:
                                        # Get file metadata
                                        file_full_path = repo_path / current_file
                                        
                                        # Get file history if not shallow clone
                                        file_history = {}
                                        if clone_depth != "shallow":
                                            file_log_cmd = [
                                                'git', '-C', str(repo_path), 'log',
                                                '--follow', '--pretty=format:%H|%an|%ad|%s',
                                                '--date=short', '-n', '5', '--', current_file
                                            ]
                                            file_log_result = subprocess.run(
                                                file_log_cmd, capture_output=True, text=True, timeout=10
                                            )
                                            
                                            if file_log_result.returncode == 0 and file_log_result.stdout:
                                                history_lines = file_log_result.stdout.strip().split('\n')
                                                file_history = {
                                                    "recent_changes": []
                                                }
                                                for h_line in history_lines:
                                                    parts = h_line.split('|')
                                                    if len(parts) >= 4:
                                                        file_history["recent_changes"].append({
                                                            "hash": parts[0][:7],
                                                            "author": parts[1],
                                                            "date": parts[2],
                                                            "message": parts[3]
                                                        })
                                        
                                        results["results"].append({
                                            "repository": repo_name,
                                            "file_path": current_file,
                                            "matches": current_matches[:max_results],
                                            "total_matches": len(current_matches),
                                            "file_history": file_history,
                                            "file_size_bytes": file_full_path.stat().st_size if file_full_path.exists() else 0
                                        })
                                    
                                    # Start new file
                                    current_file = str(rel_path)
                                    current_matches = []
                                
                                current_matches.append({
                                    "line_number": int(line_num),
                                    "content": content.strip(),
                                    "full_context": match_context[-5:] if match_context else []
                                })
                                match_context.append(content.strip())
                        
                        # Save last file's results
                        if current_file and current_matches:
                            file_full_path = repo_path / current_file
                            file_history = {}
                            
                            if clone_depth != "shallow":
                                file_log_cmd = [
                                    'git', '-C', str(repo_path), 'log',
                                    '--follow', '--pretty=format:%H|%an|%ad|%s',
                                    '--date=short', '-n', '5', '--', current_file
                                ]
                                file_log_result = subprocess.run(
                                    file_log_cmd, capture_output=True, text=True, timeout=10
                                )
                                
                                if file_log_result.returncode == 0 and file_log_result.stdout:
                                    history_lines = file_log_result.stdout.strip().split('\n')
                                    file_history = {"recent_changes": []}
                                    for h_line in history_lines:
                                        parts = h_line.split('|')
                                        if len(parts) >= 4:
                                            file_history["recent_changes"].append({
                                                "hash": parts[0][:7],
                                                "author": parts[1],
                                                "date": parts[2],
                                                "message": parts[3]
                                            })
                            
                            results["results"].append({
                                "repository": repo_name,
                                "file_path": current_file,
                                "matches": current_matches[:max_results],
                                "total_matches": len(current_matches),
                                "file_history": file_history,
                                "file_size_bytes": file_full_path.stat().st_size if file_full_path.exists() else 0
                            })
                
                elif search_type == "files":
                    # Search for files by name
                    find_cmd = ['find', str(repo_path), '-type', 'f']
                    
                    if not case_sensitive:
                        find_cmd.append('-iname')
                    else:
                        find_cmd.append('-name')
                    
                    find_cmd.append(f'*{query}*')
                    
                    # Exclude common directories
                    find_cmd.extend([
                        '!', '-path', '*/.*',
                        '!', '-path', '*/node_modules/*',
                        '!', '-path', '*/venv/*',
                        '!', '-path', '*/__pycache__/*'
                    ])
                    
                    find_result = subprocess.run(
                        find_cmd,
                        capture_output=True,
                        text=True,
                        timeout=30
                    )
                    
                    if find_result.stdout:
                        files = find_result.stdout.strip().split('\n')
                        for file_path in files[:max_results]:
                            rel_path = Path(file_path).relative_to(repo_path)
                            
                            # Get file history if available
                            file_history = {}
                            if clone_depth != "shallow":
                                file_log_cmd = [
                                    'git', '-C', str(repo_path), 'log',
                                    '--follow', '--pretty=format:%H|%an|%ad|%s',
                                    '--date=short', '-n', '3', '--', str(rel_path)
                                ]
                                file_log_result = subprocess.run(
                                    file_log_cmd, capture_output=True, text=True, timeout=10
                                )
                                
                                if file_log_result.returncode == 0 and file_log_result.stdout:
                                    history_lines = file_log_result.stdout.strip().split('\n')
                                    file_history = {"recent_changes": []}
                                    for h_line in history_lines:
                                        parts = h_line.split('|')
                                        if len(parts) >= 4:
                                            file_history["recent_changes"].append({
                                                "hash": parts[0][:7],
                                                "author": parts[1],
                                                "date": parts[2],
                                                "message": parts[3]
                                            })
                            
                            results["results"].append({
                                "repository": repo_name,
                                "file_path": str(rel_path),
                                "type": "file",
                                "file_history": file_history
                            })
                
            except subprocess.TimeoutExpired:
                results["errors"].append({
                    "repository": repo_name,
                    "error": "Operation timed out"
                })
            except Exception as e:
                results["errors"].append({
                    "repository": repo_name,
                    "error": str(e)
                })
    
    finally:
        # Clean up temporary directory
        try:
            shutil.rmtree(temp_base_dir)
            print(f"🧹 Cleaned up temporary repos from {temp_base_dir}")
        except Exception as e:
            print(f"⚠️  Warning: Could not clean up temp directory: {e}")
    
    results["total_results"] = len([r for r in results["results"] if "file_path" in r])
    return json.dumps(results, indent=2)


@tool
def analyze_repository_dependencies(repository_name: str) -> str:
    """
    Analyze dependencies, architecture, and technical constraints of a repository.
    
    Args:
        repository_name: Name of the GitHub repository
        
    Returns:
        JSON string with dependency analysis, tech stack, and constraints
    """
    # Mock implementation
    mock_analysis = {
        "repository": repository_name,
        "tech_stack": {
            "language": "Python 3.11",
            "framework": "FastAPI 0.104.0",
            "database": "PostgreSQL 15",
            "cache": "Redis 7.2",
            "message_queue": "RabbitMQ 3.12"
        },
        "dependencies": {
            "internal": [
                "shared-utils-lib",
                "common-models",
                "logging-service"
            ],
            "external": [
                "fastapi==0.104.0",
                "sqlalchemy==2.0.23",
                "pydantic==2.5.0",
                "pyotp==2.9.0",
                "twilio==8.10.0"
            ]
        },
        "architecture": {
            "pattern": "Microservices with API Gateway",
            "communication": "REST + gRPC for internal services",
            "authentication": "JWT with refresh tokens",
            "deployment": "Kubernetes on AWS EKS"
        },
        "technical_constraints": [
            "Must maintain backward compatibility with v1 API",
            "Response time must be under 200ms for auth endpoints",
            "Must support 10,000 concurrent users",
            "Zero downtime deployment required"
        ],
        "existing_mfa_implementations": {
            "found": True,
            "location": "src/auth/mfa/",
            "coverage": "partial",
            "notes": "TOTP implemented, SMS in progress, no backup codes"
        }
    }
    
    return json.dumps(mock_analysis, indent=2)


@tool
def get_team_capacity(team_name: Optional[str] = None) -> str:
    """
    Get team capacity, skills, and availability for planning.
    
    Args:
        team_name: Optional specific team name, otherwise returns all teams
        
    Returns:
        JSON string with team capacity information
    """
    # Mock implementation
    mock_capacity = {
        "planning_period": "Q4 2025",
        "teams": {
            "backend_team": {
                "members": 5,
                "available_hours_per_sprint": 400,
                "current_utilization": 0.75,
                "skills": ["Python", "FastAPI", "PostgreSQL", "Redis", "Kubernetes"],
                "expertise_level": {
                    "authentication": "expert",
                    "microservices": "expert",
                    "security": "intermediate"
                }
            },
            "frontend_team": {
                "members": 4,
                "available_hours_per_sprint": 320,
                "current_utilization": 0.80,
                "skills": ["React", "TypeScript", "Redux", "Material-UI"],
                "expertise_level": {
                    "authentication_ui": "expert",
                    "mobile": "intermediate"
                }
            },
            "mobile_team": {
                "members": 3,
                "available_hours_per_sprint": 240,
                "current_utilization": 0.70,
                "skills": ["React Native", "Swift", "Kotlin"],
                "expertise_level": {
                    "authentication": "intermediate",
                    "native_features": "expert"
                }
            },
            "qa_team": {
                "members": 3,
                "available_hours_per_sprint": 240,
                "current_utilization": 0.85,
                "skills": ["Test Automation", "Security Testing", "Performance Testing"]
            }
        }
    }
    
    return json.dumps(mock_capacity, indent=2)


@tool
def estimate_complexity(
    feature_description: str,
    affected_repositories: List[str]
) -> str:
    """
    Estimate complexity and effort for a feature based on historical data.
    
    Args:
        feature_description: Description of the feature to implement
        affected_repositories: List of repositories that will be modified
        
    Returns:
        JSON string with complexity analysis and effort estimates
    """
    # Mock implementation with ML-based prediction
    mock_estimate = {
        "feature": feature_description,
        "complexity_score": 7.5,
        "complexity_level": "High",
        "estimated_story_points": 34,
        "estimated_hours": {
            "development": 180,
            "testing": 60,
            "code_review": 30,
            "documentation": 20,
            "deployment": 10,
            "total": 300
        },
        "estimated_duration": "4-5 sprints (8-10 weeks)",
        "risk_factors": [
            "Integration across 4 repositories increases complexity",
            "Security-critical feature requires extensive testing",
            "Mobile integration adds platform-specific challenges",
            "Compliance requirements need legal review"
        ],
        "similar_past_features": [
            {
                "name": "SSO Integration",
                "estimated_hours": 250,
                "actual_hours": 280,
                "variance": "+12%"
            }
        ],
        "confidence_interval": "70-85%"
    }
    
    return json.dumps(mock_estimate, indent=2)


@tool
def analyze_git_history(
    repository_url: str,
    file_path: Optional[str] = None,
    author: Optional[str] = None,
    days: int = 90
) -> str:
    """
    Analyze git commit history to understand development patterns and velocity.
    
    Args:
        repository_url: GitHub repository URL
        file_path: Optional specific file to analyze history for
        author: Optional filter by author
        days: Number of days of history to analyze (default: 90)
        
    Returns:
        JSON string with commit history analysis
    """
    import subprocess
    import tempfile
    import shutil
    from pathlib import Path
    from datetime import datetime, timedelta
    
    results = {
        "repository": repository_url,
        "analysis_period_days": days,
        "commits": [],
        "statistics": {},
        "error": None
    }
    
    temp_dir = tempfile.mkdtemp(prefix="git_history_")
    
    try:
        repo_name = repository_url.rstrip('/').split('/')[-1].replace('.git', '')
        repo_path = Path(temp_dir) / repo_name
        
        # Clone repository
        clone_cmd = ['git', 'clone', '--quiet', repository_url, str(repo_path)]
        subprocess.run(clone_cmd, capture_output=True, text=True, timeout=60)
        
        # Get commit history
        since_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        git_log_cmd = [
            'git', '-C', str(repo_path), 'log',
            f'--since={since_date}',
            '--pretty=format:%H|%an|%ae|%ad|%s',
            '--date=short'
        ]
        
        if file_path:
            git_log_cmd.append('--')
            git_log_cmd.append(file_path)
        
        if author:
            git_log_cmd.insert(4, f'--author={author}')
        
        log_result = subprocess.run(git_log_cmd, capture_output=True, text=True, timeout=30)
        
        if log_result.stdout:
            commits_data = []
            for line in log_result.stdout.strip().split('\n'):
                if line:
                    parts = line.split('|')
                    if len(parts) >= 5:
                        commits_data.append({
                            "hash": parts[0],
                            "author": parts[1],
                            "email": parts[2],
                            "date": parts[3],
                            "message": parts[4]
                        })
            
            results["commits"] = commits_data
            results["statistics"] = {
                "total_commits": len(commits_data),
                "unique_authors": len(set(c["author"] for c in commits_data)),
                "commits_per_week": round(len(commits_data) / (days / 7), 2),
                "most_active_author": max(set(c["author"] for c in commits_data), 
                                         key=lambda x: sum(1 for c in commits_data if c["author"] == x)) if commits_data else None
            }
        
    except subprocess.TimeoutExpired:
        results["error"] = "Git operation timed out"
    except Exception as e:
        results["error"] = str(e)
    finally:
        try:
            shutil.rmtree(temp_dir)
        except:
            pass
    
    return json.dumps(results, indent=2)


@tool  
def check_technical_feasibility(
    requirement_description: str,
    technical_constraints: List[str]
) -> str:
    """
    Check technical feasibility and identify potential blockers.
    
    Args:
        requirement_description: The requirement to validate
        technical_constraints: Known technical constraints
        
    Returns:
        JSON string with feasibility analysis
    """
    mock_feasibility = {
        "requirement": requirement_description,
        "feasibility_score": 0.85,
        "verdict": "Feasible with minor challenges",
        "analysis": {
            "technical_feasibility": "High - existing auth infrastructure supports extension",
            "resource_feasibility": "Medium - requires coordination across multiple teams",
            "timeline_feasibility": "Medium - ambitious but achievable with proper planning"
        },
        "potential_blockers": [
            {
                "blocker": "SMS provider integration limits",
                "severity": "Medium",
                "mitigation": "Consider multiple SMS providers or fallback mechanisms"
            },
            {
                "blocker": "Mobile app store review time", 
                "severity": "Low",
                "mitigation": "Submit early, plan for 1-2 week review period"
            }
        ],
        "prerequisites": [
            "Security audit of MFA implementation approach",
            "Legal review for SMS/phone number storage compliance",
            "Infrastructure team approval for additional Redis capacity"
        ],
        "recommendations": [
            "Start with TOTP implementation as it has fewer dependencies",
            "Plan SMS integration for sprint 2 after TOTP is stable",
            "Consider using feature flags for gradual rollout"
        ]
    }
    
    return json.dumps(mock_feasibility, indent=2)

# ============================================================================
# Step 3: Planning Agent Instructions (Detailed Prompt)
# ============================================================================

PLANNING_AGENT_INSTRUCTIONS = """You are an expert Software Development Planning Agent specializing in analyzing requirements from Rally and creating comprehensive development plans by researching multiple GitHub repositories.

## Your Core Responsibilities:

1. **Requirements Analysis**
   - Fetch and thoroughly understand Rally Epic/Feature requirements
   - Break down high-level requirements into detailed technical tasks
   - Identify implicit requirements and edge cases
   - Map acceptance criteria to technical implementation details

2. **Repository Research**
   - Search indexed GitHub repositories for relevant code and documentation
   - Identify existing implementations that can be leveraged or extended
   - Analyze dependencies, architectural patterns, and technical constraints
   - Find similar past implementations to inform estimates

3. **Clarification & Validation**
   - Identify ambiguities or gaps in requirements
   - Generate specific, actionable clarifying questions
   - Validate technical feasibility against repository constraints
   - Flag potential conflicts or incompatibilities

4. **Comprehensive Planning**
   - Create detailed development phases with clear milestones
   - Break down work across affected repositories
   - Allocate resources based on team capacity and expertise
   - Identify dependencies and critical path
   - Assess risks and propose mitigation strategies
   - Generate realistic timelines with confidence intervals

## Your Approach:

### Phase 1: Requirements Gathering (Use planning tool first)
1. Use `fetch_rally_requirements` to get the Epic/Feature details
2. Create a high-level plan using the planning tool
3. Identify all affected systems and repositories

### Phase 2: Repository Research
1. Use `search_github_repositories` to find relevant code for each affected repository
2. Use `analyze_repository_dependencies` for each repository to understand constraints
3. Use `check_technical_feasibility` to validate the approach
4. Document existing implementations and reusable components

### Phase 3: Analysis & Estimation
1. Use `estimate_complexity` to get effort estimates
2. Use `get_team_capacity` to understand resource availability
3. Identify technical debt or architectural changes needed
4. Generate clarifying questions for ambiguous requirements

### Phase 4: Planning Document Generation
Create a comprehensive planning document in the file system with these sections:
- Executive Summary
- Requirements Analysis
- Technical Approach
- Repository Breakdown (work per repository)
- Development Phases & Timeline
- Resource Allocation
- Risk Assessment & Mitigation
- Dependencies & Prerequisites
- Clarifying Questions
- Acceptance Criteria Mapping

## Output Format:

Generate a markdown file named `planning_document_[EPIC_ID].md` with the complete plan.
Also generate a JSON summary file named `planning_summary_[EPIC_ID].json` with key metrics.

## Important Guidelines:

- Always fetch Rally requirements first before planning
- Search repositories thoroughly - don't make assumptions about existing code
- Be specific in your questions - avoid generic "clarifying questions"
- Provide realistic estimates with ranges and confidence levels
- Identify risks proactively and suggest concrete mitigations
- Consider cross-team dependencies and coordination overhead
- Think about deployment, testing, and rollback strategies
- Account for non-development time (reviews, testing, documentation)

## Example Workflow:

1. User: "Create a plan for Epic US12345"
2. You: Fetch requirements → Research repositories → Analyze feasibility → Generate plan
3. Output: Detailed planning document with specific recommendations and questions
"""

# ============================================================================
# Step 4: Sub-Agent Definitions
# ============================================================================

REQUIREMENTS_ANALYST_SUBAGENT = {
    "name": "requirements-analyst",
    "description": "Deep analysis of Rally requirements, breaking down into technical tasks and identifying gaps",
    "prompt": """You are a Requirements Analysis Specialist. Your job is to:
    
1. Parse and deeply understand Rally requirements
2. Break down high-level features into detailed technical tasks
3. Identify hidden requirements and edge cases
4. Generate specific, actionable clarifying questions
5. Map acceptance criteria to testable conditions

Be thorough and specific. Don't make assumptions - ask questions when requirements are ambiguous.
Output your analysis in a structured format with clear sections."""
}

TECHNICAL_RESEARCHER_SUBAGENT = {
    "name": "technical-researcher",
    "description": "Research GitHub repositories to find existing implementations, dependencies, and constraints",
    "prompt": """You are a Technical Research Specialist. Your job is to:

1. Search GitHub repositories systematically for relevant code
2. Analyze existing implementations and identify reusable components
3. Map dependencies between repositories and external services
4. Identify technical constraints and architectural patterns
5. Find similar past implementations for reference

Be comprehensive in your research. Document all findings with file paths and code snippets.
Provide specific recommendations based on what you find in the codebase."""
}

ESTIMATION_SPECIALIST_SUBAGENT = {
    "name": "estimation-specialist", 
    "description": "Provide accurate effort estimates and timeline predictions based on complexity analysis",
    "prompt": """You are an Estimation Specialist. Your job is to:

1. Analyze feature complexity across multiple dimensions
2. Generate effort estimates with confidence intervals
3. Consider team capacity and skill matching
4. Account for non-development time (testing, reviews, deployment)
5. Identify estimation risks and uncertainties

Provide ranges rather than single numbers. Explain your reasoning.
Reference historical data when available."""
}

# ============================================================================
# Step 5: Create the Planning Agent
# ============================================================================

def create_planning_agent():
    """
    Create the comprehensive planning agent with all tools and subagents.
    
    Returns:
        LangGraph agent ready to process planning requests
    """
    
    # Define all tools available to the agent
    tools = [
        fetch_rally_requirements,
        search_github_repositories,
        analyze_repository_dependencies,
        get_team_capacity,
        estimate_complexity,
        check_technical_feasibility
    ]
    
    # Define subagents for specialized tasks
    subagents = [
        REQUIREMENTS_ANALYST_SUBAGENT,
        TECHNICAL_RESEARCHER_SUBAGENT,
        ESTIMATION_SPECIALIST_SUBAGENT
    ]
    
    # Use Claude Sonnet 4 for high-quality reasoning (default in deepagents)
    # Or specify custom model:
    # model = ChatOpenAI(model="gpt-4o", temperature=0)
    
    # Create the deep agent
    agent = create_deep_agent(
        tools=tools,
        instructions=PLANNING_AGENT_INSTRUCTIONS,
        subagents=subagents,
        # model=model  # Optional: use custom model
    )
    
    return agent

# ============================================================================
# Step 6: Agent Execution & Output Processing
# ============================================================================

def process_planning_request(
    epic_id: str,
    feature_id: Optional[str] = None,
    additional_context: Optional[str] = None
) -> Dict[str, Any]:
    """
    Process a planning request and return comprehensive planning document.
    
    Args:
        epic_id: Rally Epic ID
        feature_id: Optional Rally Feature ID  
        additional_context: Any additional context or constraints
        
    Returns:
        Dictionary containing the planning document and metadata
    """
    
    # Create the agent
    agent = create_planning_agent()
    
    # Construct the user message
    user_message = f"Create a comprehensive development plan for Rally Epic {epic_id}"
    if feature_id:
        user_message += f", Feature {feature_id}"
    if additional_context:
        user_message += f"\n\nAdditional Context: {additional_context}"
    
    # Invoke the agent
    print(f"🚀 Starting planning for Epic {epic_id}...")
    print("=" * 80)
    
    result = agent.invoke({
        "messages": [{"role": "user", "content": user_message}]
    })
    
    # Extract the planning documents from the file system
    files = result.get("files", {})
    
    # Get the planning document
    planning_doc_key = f"planning_document_{epic_id}.md"
    planning_summary_key = f"planning_summary_{epic_id}.json"
    
    planning_document = files.get(planning_doc_key, "")
    planning_summary = files.get(planning_summary_key, "{}")
    
    # Parse the summary
    try:
        summary_data = json.loads(planning_summary)
    except json.JSONDecodeError:
        summary_data = {}
    
    # Extract final messages
    messages = result.get("messages", [])
    final_response = messages[-1].content if messages else ""
    
    return {
        "epic_id": epic_id,
        "feature_id": feature_id,
        "planning_document": planning_document,
        "planning_summary": summary_data,
        "agent_response": final_response,
        "all_files": files,
        "generated_at": datetime.now().isoformat(),
        "success": bool(planning_document or final_response)
    }


def stream_planning_request(
    epic_id: str,
    feature_id: Optional[str] = None,
    additional_context: Optional[str] = None
):
    """
    Stream the planning process in real-time (for interactive UIs).
    
    Args:
        epic_id: Rally Epic ID
        feature_id: Optional Rally Feature ID
        additional_context: Any additional context or constraints
    """
    
    agent = create_planning_agent()
    
    user_message = f"Create a comprehensive development plan for Rally Epic {epic_id}"
    if feature_id:
        user_message += f", Feature {feature_id}"
    if additional_context:
        user_message += f"\n\nAdditional Context: {additional_context}"
    
    print(f"🚀 Starting planning stream for Epic {epic_id}...")
    print("=" * 80)
    
    # Stream the agent's work
    for chunk in agent.stream(
        {"messages": [{"role": "user", "content": user_message}]},
        stream_mode="values"
    ):
        if "messages" in chunk:
            last_message = chunk["messages"][-1]
            print(f"\n[{last_message.type}]: {last_message.content[:200]}...")

# ============================================================================
# Step 7: Main Execution Examples
# ============================================================================

if __name__ == "__main__":
    
    # Example 1: Direct Git-based repository search
    print("\n" + "=" * 80)
    print("EXAMPLE 1: Git-based Repository Search")
    print("=" * 80 + "\n")
    
    # Example of searching repositories directly with git + grep
    print("Demonstrating direct git clone + grep search:")
    
    # Create a simple test to show the tool works
    from langchain_core.tools import tool
    
    # Test the search tool directly
    repositories_to_search = [
        "https://github.com/yourusername/auth-service",
        "https://github.com/yourusername/user-api"
    ]
    
    print(f"\n🔍 Searching for 'authentication' across repositories:")
    print(f"   Repositories: {repositories_to_search}")
    
    # This would actually clone and search in production:
    # search_result = search_github_repositories(
    #     query="authentication",
    #     repositories=repositories_to_search,
    #     file_extensions=[".py", ".js"],
    #     case_sensitive=False
    # )
    # print(search_result)
    
    print("\n📝 How it works:")
    print("   1. Clones each repo to temporary directory")
    print("   2. Uses grep -r -n to search all code files")
    print("   3. Returns matches with file paths and line numbers")
    print("   4. Cleans up temporary directories automatically")
    
    # Example 2: Complete planning with git-based search
    print("\n\n" + "=" * 80)
    print("EXAMPLE 2: Complete Planning with Real Repository Search")
    print("=" * 80 + "\n")
    
    # In production, this would:
    # 1. Fetch requirements from Rally API
    # 2. Clone relevant repos and search with grep
    # 3. Analyze dependencies and history
    # 4. Generate comprehensive plan
    
    result = process_planning_request(
        epic_id="US12345",
        additional_context="Search the following repositories: auth-service, user-api, frontend-app"
    )
    
    print("\n✅ Planning Complete!")
    print(f"\nGenerated Files:")
    for filename in result["all_files"].keys():
        print(f"  - {filename}")
    
    # Example 3: Git history analysis
    print("\n\n" + "=" * 80)
    print("EXAMPLE 3: Git History Analysis for Velocity Estimation")
    print("=" * 80 + "\n")
    
    print("Analyzing git history to estimate development velocity:")
    # history_result = analyze_git_history(
    #     repository_url="https://github.com/yourusername/auth-service",
    #     days=90
    # )
    # print(history_result)
    
    print("\n📊 History analysis provides:")
    print("   - Commit frequency and patterns")
    print("   - Developer velocity by author")
    print("   - File change patterns")
    print("   - Estimated development speed")
    
    # Example 4: Advanced grep patterns
    print("\n\n" + "=" * 80)
    print("EXAMPLE 4: Advanced Search Patterns")
    print("=" * 80 + "\n")
    
    print("Examples of powerful searches:")
    print("\n1. Find all authentication-related functions:")
    print("   query='def.*auth.*\\(', file_extensions=['.py']")
    
    print("\n2. Find configuration files:")
    print("   query='config', search_type='files'")
    
    print("\n3. Find TODO comments:")
    print("   query='TODO:|FIXME:', case_sensitive=False")
    
    print("\n4. Find security-related code:")
    print("   query='password|token|secret|key', case_sensitive=False")
    
    # Example 5: Configuration for your environment
    print("\n\n" + "=" * 80)
    print("SETUP INSTRUCTIONS FOR YOUR ENVIRONMENT")
    print("=" * 80 + "\n")
    
    print("1. Install required dependencies:")
    print("   pip install deepagents langchain-openai")
    
    print("\n2. Set environment variables:")
    print("   export OPENAI_API_KEY='your-api-key'")
    print("   export GITHUB_TOKEN='your-github-token'  # For private repos")
    
    print("\n3. Configure repository access:")
    print("   - Ensure git is installed: git --version")
    print("   - Set up SSH keys or HTTPS tokens for private repos")
    print("   - Test: git clone https://github.com/your/repo")
    
    print("\n4. Customize the agent:")
    print("   - Update PLANNING_AGENT_INSTRUCTIONS for your workflow")
    print("   - Modify fetch_rally_requirements with your Rally API")
    print("   - Add your repository URLs to search")
    
    print("\n5. Usage examples:")
    print("""
    # Search specific repositories
    result = search_github_repositories(
        query="MFA implementation",
        repositories=[
            "https://github.com/myorg/auth-service",
            "https://github.com/myorg/user-api"
        ],
        file_extensions=[".py", ".js", ".java"],
        case_sensitive=False
    )
    
    # Run complete planning
    planning = process_planning_request(
        epic_id="US12345",
        additional_context="Focus on backend services"
    )
    """)
    
    print("\n\n✨ All examples complete!")
    print("\n" + "=" * 80)
    print("ADVANTAGES OF GIT + GREP APPROACH:")
    print("=" * 80)
    print("✅ Always searches latest code (no stale indexes)")
    print("✅ No need to maintain vector database")
    print("✅ Works with private repositories (with proper auth)")
    print("✅ Exact pattern matching with grep's powerful regex")
    print("✅ Can search by file type, author, commit history")
    print("✅ Lower infrastructure costs (no vector DB hosting)")
    print("✅ Simple and transparent (standard git/grep commands)")
    print("\n⚠️  CONSIDERATIONS:")
    print("   - Slower for very large repositories (use --depth 1)")
    print("   - Requires git installed on system")
    print("   - Network dependent (cloning repos)")
    print("   - Temp disk space needed (cleaned up automatically)")
    print("=" * 80)