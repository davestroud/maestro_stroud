#!/usr/bin/env python3
"""
Branch Manager MCP Server
Helps manage context and notes across different git branches
"""

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base
from pydantic import Field
import json
import os
import subprocess
from pathlib import Path

mcp = FastMCP("BranchManager")

# Storage directory for branch-specific data
BRANCH_DATA_DIR = Path(".branch_data")
BRANCH_DATA_DIR.mkdir(exist_ok=True)

def get_current_branch():
    """Get the current git branch name"""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return "unknown"

def get_branch_file(branch_name, filename):
    """Get path to a branch-specific file"""
    branch_dir = BRANCH_DATA_DIR / branch_name
    branch_dir.mkdir(exist_ok=True)
    return branch_dir / filename

# ============================================================================
# TOOLS - Actions for managing branch context
# ============================================================================

@mcp.tool(
    name="save_branch_note",
    description="Save a note specific to the current branch (context, TODOs, decisions)"
)
def save_branch_note(
    note: str = Field(description="Note content to save"),
    category: str = Field(default="general", description="Category: general, todo, decision, issue")
):
    branch = get_current_branch()
    notes_file = get_branch_file(branch, "notes.json")

    # Load existing notes
    notes = []
    if notes_file.exists():
        with open(notes_file) as f:
            notes = json.load(f)

    # Add new note
    notes.append({
        "category": category,
        "note": note,
        "timestamp": __import__("datetime").datetime.now().isoformat()
    })

    # Save
    with open(notes_file, "w") as f:
        json.dump(notes, f, indent=2)

    return f"✓ Saved {category} note to branch '{branch}'\n{note}"

@mcp.tool(
    name="list_branch_notes",
    description="List all notes for the current branch or a specific branch"
)
def list_branch_notes(
    branch_name: str = Field(default="", description="Branch name (empty = current branch)")
):
    branch = branch_name or get_current_branch()
    notes_file = get_branch_file(branch, "notes.json")

    if not notes_file.exists():
        return f"No notes found for branch '{branch}'"

    with open(notes_file) as f:
        notes = json.load(f)

    if not notes:
        return f"No notes found for branch '{branch}'"

    # Format output
    output = [f"📋 Notes for branch '{branch}':\n"]

    categories = {}
    for note in notes:
        cat = note["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(note)

    for category, cat_notes in categories.items():
        output.append(f"\n{'='*60}")
        output.append(f"  {category.upper()}")
        output.append(f"{'='*60}")
        for i, note in enumerate(cat_notes, 1):
            timestamp = note["timestamp"][:19]  # Remove milliseconds
            output.append(f"\n{i}. [{timestamp}]")
            output.append(f"   {note['note']}")

    return "\n".join(output)

@mcp.tool(
    name="clear_branch_notes",
    description="Clear all notes for the current branch"
)
def clear_branch_notes():
    branch = get_current_branch()
    notes_file = get_branch_file(branch, "notes.json")

    if notes_file.exists():
        notes_file.unlink()
        return f"✓ Cleared all notes for branch '{branch}'"

    return f"No notes to clear for branch '{branch}'"

@mcp.tool(
    name="save_branch_context",
    description="Save important context about what you're working on in this branch"
)
def save_branch_context(
    context: str = Field(description="Context description (purpose, status, blockers, etc.)")
):
    branch = get_current_branch()
    context_file = get_branch_file(branch, "context.txt")

    with open(context_file, "w") as f:
        f.write(context)

    return f"✓ Saved context for branch '{branch}'"

@mcp.tool(
    name="compare_branches",
    description="Compare two branches to see what's different"
)
def compare_branches(
    branch1: str = Field(description="First branch name"),
    branch2: str = Field(description="Second branch name")
):
    try:
        result = subprocess.run(
            ["git", "diff", "--stat", f"{branch1}..{branch2}"],
            capture_output=True,
            text=True,
            check=True
        )

        if not result.stdout.strip():
            return f"No differences between {branch1} and {branch2}"

        return f"Changes from {branch1} to {branch2}:\n\n{result.stdout}"
    except subprocess.CalledProcessError as e:
        return f"Error comparing branches: {e.stderr}"

@mcp.tool(
    name="list_all_branches_with_notes",
    description="List all branches that have saved notes or context"
)
def list_all_branches_with_notes():
    if not BRANCH_DATA_DIR.exists():
        return "No branch data found"

    branches_with_data = []
    for branch_dir in BRANCH_DATA_DIR.iterdir():
        if branch_dir.is_dir():
            branch_name = branch_dir.name
            has_notes = (branch_dir / "notes.json").exists()
            has_context = (branch_dir / "context.txt").exists()

            if has_notes or has_context:
                branches_with_data.append({
                    "branch": branch_name,
                    "has_notes": has_notes,
                    "has_context": has_context
                })

    if not branches_with_data:
        return "No branches with saved data"

    output = ["📊 Branches with saved data:\n"]
    for item in branches_with_data:
        output.append(f"  • {item['branch']}")
        if item['has_notes']:
            output.append(f"    - Has notes")
        if item['has_context']:
            output.append(f"    - Has context")

    return "\n".join(output)

# ============================================================================
# RESOURCES - Data Claude can access
# ============================================================================

@mcp.resource("branch://current", mime_type="text/plain", name="Current Branch")
def get_current_branch_resource():
    """Get the name of the current git branch"""
    return get_current_branch()

@mcp.resource("branch://context", mime_type="text/plain", name="Current Branch Context")
def get_branch_context():
    """Get the context saved for the current branch"""
    branch = get_current_branch()
    context_file = get_branch_file(branch, "context.txt")

    if not context_file.exists():
        return f"No context saved for branch '{branch}'"

    with open(context_file) as f:
        return f.read()

@mcp.resource("branch://notes", mime_type="application/json", name="Current Branch Notes")
def get_branch_notes_resource():
    """Get all notes for the current branch as JSON"""
    branch = get_current_branch()
    notes_file = get_branch_file(branch, "notes.json")

    if not notes_file.exists():
        return json.dumps({"branch": branch, "notes": []})

    with open(notes_file) as f:
        notes = json.load(f)

    return json.dumps({"branch": branch, "notes": notes}, indent=2)

@mcp.resource("branch://list", mime_type="text/plain", name="All Git Branches")
def list_branches():
    """List all git branches"""
    try:
        result = subprocess.run(
            ["git", "branch", "-a"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error listing branches: {e.stderr}"

# ============================================================================
# PROMPTS - Pre-built workflows
# ============================================================================

@mcp.prompt(
    name="branch_summary",
    description="Generate a comprehensive summary of the current branch"
)
def branch_summary_prompt():
    """Generate a summary of the current branch's work"""
    branch = get_current_branch()
    return [base.UserMessage(f"""
Please create a comprehensive summary of branch '{branch}':

1. Check @branch://context for saved context
2. Check @branch://notes for saved notes
3. Use git diff to see what's changed from main
4. Summarize:
   - What this branch is for
   - Current status
   - Key changes made
   - Any blockers or TODOs
   - Next steps

Format as a clear, organized report.
""")]

@mcp.prompt(
    name="switch_branch",
    description="Prepare to switch to a different branch with full context"
)
def switch_branch_prompt(
    target_branch: str = Field(description="Branch to switch to")
):
    """Help switch branches with context preservation"""
    current = get_current_branch()
    return [base.UserMessage(f"""
I'm about to switch from '{current}' to '{target_branch}'.

Please help me:
1. Summarize current work on '{current}' (ask if I want to save context)
2. Show me the context for '{target_branch}' if it exists
3. Show me the notes for '{target_branch}' if they exist
4. Explain what '{target_branch}' is working on
5. Ask if I'm ready to switch

Don't actually switch branches - just prepare me with context.
""")]

@mcp.prompt(
    name="branch_compare",
    description="Compare current branch with another branch"
)
def branch_compare_prompt(
    other_branch: str = Field(description="Branch to compare with")
):
    """Compare branches and explain differences"""
    current = get_current_branch()
    return [base.UserMessage(f"""
Compare branch '{current}' with '{other_branch}':

1. Use compare_branches tool to see file changes
2. Check if both branches have saved context
3. Explain:
   - What's different
   - Which branch is ahead
   - Potential merge conflicts
   - Recommendations

Provide a clear comparison report.
""")]

# ============================================================================
# Server Entry Point
# ============================================================================

if __name__ == "__main__":
    mcp.run(transport="stdio")
